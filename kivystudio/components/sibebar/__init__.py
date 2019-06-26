from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import OptionProperty

from kivy.lang import Builder

from kivystudio.behaviors import HoverInfoBehavior

from .fileexplorer import FileExplorer
from .gitmanager import GitManager
from .generalsearch import GeneralSearch

import os
filepath = os.path.dirname(__file__)
Builder.load_file(os.path.join(filepath,'sidebar.kv'))


__all__ = ('SideBar',)

class SideBar(BoxLayout):

    def __init__(self, **k):
        super(SideBar, self).__init__(**k)
        self.fileexplorer = FileExplorer()
        self.gitmanager = GitManager()
        self.generalsearch = GeneralSearch()
    
    def toggle_bar(self, tab):
        if tab.state=='down':
            if len(self.children) > 1:
                self.remove_widget(self.children[0])
                self.width = '46dp'

            tab_bar = getattr(self, tab.tab_type)
            self.width += tab_bar.width
            self.add_widget(tab_bar)
        else:
            self.width = '46dp'
            if len(self.children) > 1:
                    self.remove_widget(self.children[0])
    

class SideButter(HoverInfoBehavior, ToggleButtonBehavior, Label):
    '''
    buttons on the sidebar
    '''
    def on_hover(self, *a):
        if self.hover:
            self.color = (1,1,1,1)
        elif not self.hover and self.state == 'normal':
            self.color = (.5,.5,.5,1)

        # return super(SideB)

class SideToggleBar(ScreenManager):
    '''ScreenManager of the sidebar
    '''

