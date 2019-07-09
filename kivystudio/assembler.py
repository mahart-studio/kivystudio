from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

import os
import sys
import traceback

from kivy.logger import Logger
try:
    from plyer import filechooser as filemanager
except:
    from kivystudio.widgets.filemanager import filemanager
    Logger.warning("plyer isn't installed")

from kivystudio.parser import emulate_file

from kivystudio.components.screens import AndroidPhoneScreen
from kivystudio.components.topmenu import TopMenu
from kivystudio.components.codeplace import CodePlace
from kivystudio.components.sibebar import SideBar
from kivystudio.components.terminal import TerminalSpace
from kivystudio.components.emulator_area import emulator_area


class Assembly(BoxLayout):
    pass

def add_new_tab(paths):
    for path in paths:
        code_place.add_code_tab(filename=path)

def open_folder(*a):
    print(a)


def key_down(self, *args):
    if args[0] == 114 and args[3] == ['ctrl']:     # emulate file Ctrl+R
        Clock.schedule_once(lambda dt: emulate_file(emulator_area.emulation_file))

    elif args[0] == 107 and args[3] == ['ctrl']:    # Ctrl K pressed
        pass

    elif args[0] == 111 and args[3] == ['ctrl']:    # open file Ctrl+O
        filemanager.open_file(path='/root',on_selection=add_new_tab)

    elif args[0] == 110 and args[3] == ['ctrl']:    # new file Ctrl+N
        code_place.add_code_tab(tab_type='new_file')



Window.bind(on_key_down=key_down)


code_place = CodePlace()
code_place.add_code_tab(tab_type='welcome')

emulator_area = emulator_area()
Assembler = Assembly()

Assembler.ids.box.add_widget(SideBar())
Assembler.ids.box.add_widget(code_place)
Assembler.ids.box.add_widget(emulator_area)
