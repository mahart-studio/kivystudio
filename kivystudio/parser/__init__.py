import os, sys
import traceback
from threading import Thread
from functools import partial
try:
    from importlib import reload
except:      # for py 2 compatibility
    pass

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.widget import Widget
from kivy.resources import resource_add_path, resource_remove_path

from kivystudio.components.emulator_area import get_emulator_area
from kivystudio.tools.logger import Logger

def emulate_file(filename, threaded=False):
    if not filename:
        Logger.error("KivyStudio: No file selected press Ctrl-E to select file for emulation")
        return

    Logger.info("Emulator: Starting Emulation on file '{}'".format(filename))
    root=None
    if not os.path.exists(filename):
        Logger.error("KivyStudio: file {} not found".format(filename))
        return

    with open(filename) as fn:
        file_content =  fn.read()

    if app_not_run_properly(file_content):
        Logger.error("Emulator: App not run properly 'try running under if __name__ == '__main__':")
        return

    dirname=os.path.dirname(filename)
    sys.path.append(dirname)
    os.chdir(dirname)
    resource_add_path(dirname)

    get_emulator_area().screen_display.screen.clear_widgets()
    if threaded:
        Thread(target=partial(start_emulation, filename,
                            file_content, threaded=threaded)).start()
    else:
        start_emulation(filename, file_content, threaded=threaded)

def start_emulation(filename, file_content, threaded=False):
    root = None
    has_error = False
    if os.path.splitext(filename)[1] =='.kv':    # load the kivy file directly
        try:    # cacthing error with kivy files
            Builder.unload_file(filename)
            root = Builder.load_file(filename)
        except:
            has_error = True
            trace = traceback.format_exc()
            Logger.error("Emulator: {}".format(trace))

    elif os.path.splitext(filename)[1] =='.py':
        load_defualt_kv(filename, file_content)
        try:    # cahching error with python files
            root = load_py_file(filename, file_content)
        except:
            has_error = True
            trace = traceback.format_exc()
            Logger.error("Emulator: {}".format(trace))
    else:
        Logger.warning("KivyStudio: can't emulate file type {}".format(filename))

    if not root and not has_error:
        Logger.error('Emulator: No root widget found.')
    elif not isinstance(root,Widget) and not has_error:
        Logger.error("KivyStudio: root instance found = '{}' and is not a widget".format(root))
    elif root:
        if threaded:
            emulation_done(root, filename)
        else:
            get_emulator_area().screen_display.screen.add_widget(root)

    dirname=os.path.dirname(filename)
    sys.path.pop()
    resource_remove_path(dirname)

@mainthread
def emulation_done(root, filename):
    ' add root on the main thread '
    if root:
        get_emulator_area().screen_display.screen.add_widget(root)


def load_defualt_kv(filename, file_content):
    ''' load the default kivy file
        associated the the python file,
        usaully lowercase of the app class
    '''
    app_cls_name = get_app_cls_name(file_content)
    if app_cls_name is None:
        return

    kv_name = app_cls_name.lower()
    if app_cls_name.endswith('App'):
        kv_name = app_cls_name[:len(app_cls_name)-3].lower()

    if app_cls_name:
        file_dir = os.path.dirname(filename)
        kv_filename = os.path.join(file_dir, kv_name+'.kv')

        if os.path.exists(kv_filename):
            try:    # cacthing error with kivy files
                Builder.unload_file(kv_filename)
                root = Builder.load_file(kv_filename)
            except:
                trace = traceback.format_exc()
                Logger.error("KivyStudio: You kivy file has a problem")
                Logger.error("KivyStudio: {}".format(trace))


def get_app_cls_name(file_content):

    lines = file_content.splitlines()
    app_cls = get_import_as('from kivy.app import App', lines)
    if not app_cls:
    	app_cls = get_import_as('from kivymd.app import MDApp', lines)

    def check_app_cls(line):
        line = line.strip()
        return line.startswith('class') and line.endswith('(%s):'%app_cls)

    found = list(filter(check_app_cls, lines))
    if found:
        line = found[0]
        cls_name = line.split('(')[0].split(' ')[1]
        return cls_name


def get_root_from_runTouch(filename):
    with open(filename) as fn:
        text =  fn.read()

    lines = text.splitlines()
    run_touch = get_import_as('from kivy.base import runTouchApp', lines)

    def check_run_touch(line):
        line = line.strip()
        return line.startswith('%s(' % run_touch)

    found = list(filter(check_run_touch, lines))

    if found:
        line = found[0]
        root_name = line.strip().split('(')[1].split(')')[0]

        root_file = import_from_dir(filename)
        root = getattr(reload(root_file), root_name)
        return root


def load_py_file(filename, file_content):

    app_cls_name = get_app_cls_name(file_content)
    if app_cls_name:

        root_file = import_from_dir(filename)
        app_cls = getattr(reload(root_file), app_cls_name)
        root = app_cls().build()
        return root
    
    run_root = get_root_from_runTouch(filename)
    if run_root:
        return run_root


def import_from_dir(filename):
    ''' force python to import this file
    from the project_ dir'''

    dirname, file = os.path.split(filename)
    sys.path = [dirname] + sys.path

    import_word = os.path.splitext(file)[0]
    imported = __import__(import_word)
    return imported


def get_import_as(start, lines):
    ''' get the variable used by user when importing as.
        Ex: from kivy import platform
            it will return plaform
        Ex: from kivy import platform as plt
            it will return plt
    '''
    line = list(filter(lambda line: line.strip().startswith(start), lines))
    if line:
        words = line[0].split(' ')
        import_word = words[len(words)-1]
        return import_word

def app_not_run_properly(file_content):
    
    lines = file_content.splitlines()
    run_touch = get_import_as('from kivy.base import runTouchApp', lines)

    def check_run_touch(line):
        return line.startswith('%s(' % run_touch)
    found1 = list(filter(check_run_touch, lines))

    def check_run_app(line):
        app_name = get_app_cls_name(file_content)
        return line.endswith('run()') and line.startswith(app_name)
    found2 = list(filter(check_run_app, lines))

    return found1 or found2
