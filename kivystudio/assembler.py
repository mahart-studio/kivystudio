
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import mainthread

from kivystudio.widgets.filemanager import filemanager
from kivystudio.parser import emulate_file

from kivystudio.components.topmenu import TopMenu
from kivystudio.components.codeplace import code_place, code_container
from kivystudio.components.sibebar import SideBar
from kivystudio.components.terminal import TerminalSpace
from kivystudio.components.emulator_area import get_emulator_area
from kivystudio.settings import settings_obj

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

def main_key_handler(win, *args):
    '''' main keyboard and shortcut lisener '''
    # print(args)
    if args[0] == 114 and  'ctrl' in args[3]:     # emulate file Ctrl+R
        emulate_file(emulator_area.emulation_file)

    elif args[0] == 107 and 'ctrl' in args[3]:    # Open folder Ctrl+K
        filemanager.choose_dir(path='.',on_selection=open_project)

    elif args[0] == 111 and 'ctrl' in args[3]:    # Open file Ctrl+O
        filemanager.open_file(path='.',on_selection=add_new_tab)

    elif args[0] == 110 and 'ctrl' in args[3]:    # New file Ctrl+N
        code_place.add_code_tab(tab_type='new_file')

    elif args[0] == 96 and 'ctrl' in args[3]:    # Toggle terminal  Ctrl+`
        from kivystudio.components.codeplace import terminal
        terminal.toggle_state()

    elif args[0] == 45 and 'ctrl' in args[3]:    # Zoom out Ctrl -
        if settings_obj.dpi_scale > 0.8:
            settings_obj.dpi_scale -= 0.1

    elif args[0] == 61 and 'ctrl' in args[3]:    # Zoom in Ctrl +
        if settings_obj.dpi_scale < 1.4:
            settings_obj.dpi_scale += 0.1

Window.bind(on_key_down=main_key_handler)


emulator_area = get_emulator_area()
side_bar = SideBar()
Assembler = Assembly()

box = Assembler.ids.box
box.add_widget(side_bar)
box.add_widget(code_container)
box.add_widget(emulator_area)
