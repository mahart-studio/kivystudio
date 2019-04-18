import os
import sys
import traceback

from kivy.lang import Builder
from kivy.resources import resource_add_path

project_dir = 'test_project'
main_file = 'main.py'
sys.path.append(project_dir)
resource_add_path(project_dir)



def load_defualt_kv():
    app_cls_name = get_app_cls_name()
    kv_name = app_cls_name.lower()
    if app_cls_name.endswith('App'):
        kv_name = app_cls_name[:len(app_cls_name)-3].lower()
    print(kv_name)    
    if app_cls_name:
        kv_filename = os.path.join(project_dir, kv_name+'.kv')
        print(kv_filename)
        if os.path.exists(kv_filename):

            try:    # cahching error with kivy files
                Builder.unload_file(kv_filename)
                root = Builder.load_file(kv_filename)
            except:
                traceback.print_exc()
                print("You kivy file has a problem")



def get_app_cls_name():
    with open(os.path.join(project_dir, main_file)) as fn:
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
    with open(file) as fn:
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


        root_file = import_from_project_dir(main_file)
        root = getattr(reload(root_file), root_name)
        
        return root


def load_py_file():

    app_cls_name = get_app_cls_name()
    if app_cls_name:

        root_file = import_from_project_dir(main_file)
        print(root_file)
        app_cls = getattr(reload(root_file), app_cls_name)
        root = app_cls().build()

        return root
    
    run_root = get_root_from_runTouch
    if run_root:
        return run_root


def import_from_project_dir(filename):
    ''' force python to import this file
    from the project_ dir'''

    # first clear the sys path
    former_path = sys.path
    sys.path = []
    sys.path.append(project_dir)

    import_word = os.path.splitext(filename)[0]
    return __import__(import_word)

    sys.path = []
    sys.path = former_path



def get_import_as(start, lines):
    
    line = list(filter(lambda line: line.strip().startswith(start), lines))
    if line:
        words = line[0].split(' ')
        import_word = words[len(words)-1]
        return import_word
    else:
        return

