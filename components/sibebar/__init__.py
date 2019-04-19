from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screen import ScreenManager


from .fileexplorer import FileExplorer
from .gitmanager import GitManager
from .generalsearch import GeneralSearch


__all__ = ('SideBar',)

class SideBar(FloatLayout):
    pass

class SideButter(ToggleButtonBehavior, Image):
    pass


class SideToggleBar(ScreenManager):
    pass

