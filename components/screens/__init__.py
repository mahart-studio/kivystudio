import os

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.base import runTouchApp as app
from kivy.properties import ObjectProperty
from kivy.uix.scatter import Scatter
from kivy.lang import Builder 

# module resources
from kivy.resources import resource_add_path
resource_add_path(os.path.dirname(os.path.realpath(__file__)))

__all__ = ('IphoneScreen', 'IpadScreen', 'AndroidPhoneScreen', 'AndriodTabScreen', )

class ScreenScatter(Scatter):
	
    container = ObjectProperty(None)

    def add_widget(self, widget):
        if len(self.children) > 0:
            self.container.add_widget(widget)
        else:
            super(ScreenScatter, self).add_widget(widget)

    def clear_widgets(self):
        self.container.clear_widgets()


class ScreenContainer(RelativeLayout):
    pass


class IphoneScreen(ScreenScatter):
    pass

class IpadScreen(ScreenScatter):
    pass

class AndriodTabScreen(ScreenScatter):
    pass

class AndroidPhoneScreen(ScreenScatter):
    pass


Builder.load_file('screen.kv')



if __name__ == "__main__":
    app(build)
