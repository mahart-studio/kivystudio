import os, sys
import traceback
from threading import Thread
from functools import partial
try:
    from importlib import reload
except:
    pass

from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.resources import resource_add_path, resource_remove_path

from kivystudio.components.emulator_area import emulator_area

def emulate_file(filename, threaded=False):
    root=None

    dirname=os.path.dirname(filename)
    sys.path.append(dirname)
    resource_add_path(dirname)

    emulator_area().screen_display.screen.clear_widgets()

    if threaded:
        Thread(target=partial(start_emulation, filename, threaded=threaded)).start()
    else:
        start_emulation(filename, threaded=threaded)

def start_emulation(filename, threaded=False):
    root = None
    if os.path.splitext(filename)[1] =='.kv':    # load the kivy file directly
        try:    # cahching error with kivy files
            Builder.unload_file(filename)
            root = Builder.load_file(filename)
        except:
            traceback.print_exc()
            print("You kivy file has a problem")

    elif os.path.splitext(filename)[1] =='.py':
        load_defualt_kv(filename)

        try:    # cahching error with python files
            root = load_py_file(filename)
        except:
            traceback.print_exc()        
            print("You python file has a problem")

    if root:
        if threaded:
            emulation_done(root, filename)
        else:
            emulator_area().screen_display.screen.add_widget(root)

    dirname=os.path.dirname(filename)
    sys.path.pop()
    resource_remove_path(dirname)

@mainthread
def emulation_done(root, filename):
    if root:
        emulator_area().screen_display.screen.add_widget(root)


def load_defualt_kv(filename):
    app_cls_name = get_app_cls_name(filename)
    if app_cls_name is None:
        return

    kv_name = app_cls_name.lower()
    if app_cls_name.endswith('App'):
        kv_name = app_cls_name[:len(app_cls_name)-3].lower()

    if app_cls_name:
        file_dir = os.path.dirname(filename)
        kv_filename = os.path.join(file_dir, kv_name+'.kv')

        if os.path.exists(kv_filename):
            try:    # cahching error with kivy files
                Builder.unload_file(kv_filename)
                root = Builder.load_file(kv_filename)
            except:
                traceback.print_exc()
                print("You kivy file has a problem")



def get_app_cls_name(filename):
    with open(filename) as fn:
        text =  fn.read()

    lines = text.splitlines()
    app_cls = get_import_as('from kivy.app import App', lines)

    def check_app_cls(line):
        line = line.strip()
        return line.startswith('class') and line.endswith('(%s):'%app_cls)

    found = list(filter(check_app_cls, lines))

    if found:
        line = found[0]
        cls_name = line.split('(')[0].split(' ')[1]
        return cls_name


def get_root_from_runTouch():
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


def load_py_file(filename):

    app_cls_name = get_app_cls_name(filename)
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
    
    line = list(filter(lambda line: line.strip().startswith(start), lines))
    if line:
        words = line[0].split(' ')
        import_word = words[len(words)-1]
        return import_word
    else:
        return

