from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivystudio.behaviors import HoverBehavior
from kivystudio.widgets.dropdown import DropDownBase
from kivystudio import tools

tools.load_kv(__file__,'dropmenu.kv')


class MenuButton(HoverBehavior, ButtonBehavior, BoxLayout):
    pass

class ToggleMenuButton(HoverBehavior, ToggleButtonBehavior, BoxLayout):
    pass

class FileTopMenu(DropDownBase):
    
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

    def new_file(self):
        tools.quicktools.open_new_file()

    def open_file(self):
        tools.quicktools.open_file()

    def open_folder(self):
        tools.quicktools.open_file()
    
    def open_recent(self):
        tools.quicktools.open_recent()

    def save(self):
        tools.quicktools.save()

    def save_all(self):
        tools.quicktools.save_all()

    def save_as(self):
        tools.quicktools.save_as()

    def exit_window(self):
        tools.quicktools.exit_window()


class EditTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

class ViewTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)

class HelpTopMenu(DropDownBase):
    def __init__(self, **k):
        super(FileTopMenu, self).__init__(**k)
