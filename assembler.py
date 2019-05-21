from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

import os
import sys
import traceback


from kivystudio.parser import load_defualt_kv, load_py_file
from kivystudio.widgets.filemanager import FileManager

from kivystudio.components.screens import AndroidPhoneScreen
from kivystudio.components.topmenu import TopMenu
from kivystudio.components.emulator_area import EmulatorArea
from kivystudio.components.codeplace import CodePlace
from kivystudio.components.sibebar import SideBar
from kivystudio.components.terminal import TerminalSpace

class Assembly(BoxLayout):
    pass

def add_new_tab(obj, path):
    print(path)
    code_place.add_code_tab(filename=path)

def open_folder(*a):
    print(a)

filechooser=FileManager()
filechooser.bind(on_finished=add_new_tab)


def key_down(self, *args):
    if args[0] == 114 and args[3] == ['ctrl']:     # emulate file Ctrl+R
        Clock.schedule_once(lambda dt: emulate())

    elif args[0] == 107 and args[3] == ['ctrl']:    # Ctrl K pressed
        pass

    elif args[0] == 111 and args[3] == ['ctrl']:    # open file Ctrl+O
        filechooser.open_file(dir='/root',callback=add_new_tab)

    elif args[0] == 110 and args[3] == ['ctrl']:    # new file Ctrl+N
        code_place.add_code_tab()


def emulate():
    emulator_area.screen_display.screen.clear_widgets()
    
    load_defualt_kv()

    try:    # cahching error with python files
        root = load_py_file()
        print(root)
        emulator_area.screen_display.screen.add_widget(root)
    except:
        traceback.print_exc()
        print("You python file has a problem")


Window.bind(on_key_down=key_down)


project_dir = 'test_project'
main_file = os.path.join(project_dir, 'main.py')
kv_file = os.path.join(project_dir, 'main.kv')

sys.path.append(project_dir)

code_place = CodePlace()
# code_place.add_code_tab(filename=main_file)
# code_place.add_code_tab(filename=kv_file)

emulator_area = EmulatorArea(size_hint_x=.45)
Assembler = Assembly()

from kivystudio.components.welcome import WelcomeTab

Assembler.ids.box.add_widget(SideBar())
Assembler.ids.box.add_widget(WelcomeTab())
Assembler.ids.box.add_widget(emulator_area)
