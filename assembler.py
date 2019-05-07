from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

import os
import sys
import traceback


from kivystudio.screens import AndroidPhoneScreen
from kivystudio.parser import load_defualt_kv, load_py_file
from kivystudio.widgets.codeinput import FullCodeInput
from kivystudio.widgets.filemanager import FileManager

from kivystudio.components.topmenu import TopMenu
from kivystudio.components.emulator_area import EmulatorArea
from kivystudio.components.codeplace import CodePlace
from kivystudio.components.sibebar import SideBar

class Assembly(BoxLayout):
    pass

def add_new_tab(obj, path):
    code_place.add_widget(FullCodeInput(filename=path))

file=FileManager()
file.bind(on_finished=add_new_tab)


def key_down(self, *args):
    # print(args)
    if args[0] == 115 and args[3] == ['ctrl']:
        Clock.schedule_once(lambda dt: emulate())

    elif args[0] == 111 and args[3] == ['ctrl']:
        if not file.parent:
            file.open()

    elif args[0] == 110 and args[3] == ['ctrl']:
        print('added')
        add_new_tab(None, 'Untitled-1')

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
code_place.add_widget(FullCodeInput(filename=main_file))
code_place.add_widget(FullCodeInput(filename=kv_file))

emulator_area = EmulatorArea(size_hint_x=.45)
Assembler = Assembly()

Assembler.ids.box.add_widget(SideBar())
Assembler.ids.box.add_widget(code_place)
Assembler.ids.box.add_widget(emulator_area)
