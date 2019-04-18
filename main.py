from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '740')

import os
import sys
sys.path.append(os.pardir)
import traceback



from kivy.uix.floatlayout import FloatLayout
from kivy.base import runTouchApp as app
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock


from kivystudio.screens import AndroidPhoneScreen
from kivystudio.parser import load_defualt_kv, load_py_file
from kivystudio.widgets.codeinput import FullCodeInput 
from kivystudio.components.topmenu import TopMenu
from kivystudio.widgets.filemanager import FileManager

from kivystudio.components.emulator_area import EmulatorArea
from kivystudio.components.codeplace import CodePlace


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
    build.ids.display_screen.clear_widgets()
    
    load_defualt_kv()

    try:    # cahching error with python files
        root = load_py_file()
        build.ids.display_screen.add_widget(root)
    except:
        traceback.print_exc()
        print("You python file has a problem")


Window.bind(on_key_down=key_down)


build = Builder.load_string('''

BoxLayout:
    orientation: 'vertical'
    TopMenu:
    BoxLayout:
        id: box
        FloatLayout:
            size_hint_x: .45
            canvas.before:
                Color:
                    rgba: .6,.6,.6,1
                Rectangle:
                    size: self.size
                    pos: self.pos
            EmulatorArea:

            # FloatLayout:
            #     AndroidPhoneScreen:
            #         id: display_screen
            #         Button:
            #             text: 'Hello World!!'
            #     BoxLayout:
            #         pos_hint: {'y': .01, 'center_x': .5}
            #         size_hint: None,None
            #         size: '110dp', '46dp'
            #         Button:
            #             text: '-'
            #             bold: True
            #             on_release:
            #                 if not display_screen.scale < -100.0: display_screen.scale -= 0.05
            #         Button:
            #             text: '+'
            #             bold: True
            #             on_release: display_screen.scale += 0.05

''')

project_dir = 'test_project'
main_file = os.path.join(project_dir, 'main.py')
kv_file = os.path.join(project_dir, 'main.kv')

sys.path.append(project_dir)

code_place = CodePlace()
code_place.add_widget(FullCodeInput(filename=main_file))
code_place.add_widget(FullCodeInput(filename=kv_file))

build.ids.box.add_widget(code_place)
app(build)