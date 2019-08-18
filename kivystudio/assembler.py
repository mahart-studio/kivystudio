
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock, mainthread

import os
import sys
import traceback

from kivystudio.widgets.filemanager import filemanager
from kivystudio.parser import emulate_file

from kivystudio.components.screens import AndroidPhoneScreen
from kivystudio.components.topmenu import TopMenu
from kivystudio.components.codeplace import CodePlace
from kivystudio.components.sibebar import SideBar
from kivystudio.components.terminal import TerminalSpace
from kivystudio.components.emulator_area import emulator_area


class Assembly(BoxLayout):
    '''
    Widget to assemble and structure 
    all widgets
    '''

def add_new_tab(paths):
    for path in paths:
        code_place.add_code_tab(filename=path)

@mainthread
def open_project(paths):
    if paths:
        side_bar.ids.explorer_btn='down'
        side_bar.fileexplorer.load_directory(paths[0])

def main_key_handler(self, *args):
    '''' main keyboard and shortcut lisener '''
    if args[0] == 114 and args[3] == ['ctrl']:     # emulate file Ctrl+R
        Clock.schedule_once(lambda dt: emulate_file(emulator_area.emulation_file))

    elif args[0] == 107 and args[3] == ['ctrl']:    # Ctrl K pressed
        filemanager.choose_dir(path='/root',on_selection=open_project)

    elif args[0] == 111 and args[3] == ['ctrl']:    # open file Ctrl+O
        filemanager.open_file(path='/root',on_selection=add_new_tab)

    elif args[0] == 110 and args[3] == ['ctrl']:    # new file Ctrl+N
        code_place.add_code_tab(tab_type='new_file')

Window.bind(on_key_down=main_key_handler)


code_place = CodePlace()
# add welcoming tab
code_place.add_code_tab(tab_type='welcome')

emulator_area = emulator_area()
side_bar = SideBar()
Assembler = Assembly()

Assembler.ids.box.add_widget(side_bar)
Assembler.ids.box.add_widget(code_place)
Assembler.ids.box.add_widget(emulator_area)
