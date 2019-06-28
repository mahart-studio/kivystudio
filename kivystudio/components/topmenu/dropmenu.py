from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivystudio.behaviors import HoverBehavior
from kivystudio.widgets.dropdown import DropDownBase
from kivystudio.widgets.filemanager import filemanager
from kivystudio.tools import quicktools

import os
filepath = os.path.dirname(__file__)
Builder.load_file(os.path.join(filepath,'dropmenu.kv'))


class MenuButton(HoverBehavior, ButtonBehavior, BoxLayout):
    pass

class ToggleMenuButton(HoverBehavior, ToggleButtonBehavior, BoxLayout):
    pass

class FileTopMenu(DropDownBase):
    
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

    def new_file(self):
        quicktools.open_new_file()

    def open_file(self):
        quicktools.open_file()

    def open_folder(self):
        quicktools.open_file()
    
    def open_recent(self):
        quicktools.open_recent()

    def save(self):
        quicktools.save()

    def save_all(self):
        quicktools.save_all()

    def save_as(self):
        quicktools.save_as()

    def exit_window(self):
        quicktools.exit_window()


class EditTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

class ViewTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

class HelpTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)
