import os

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.base import runTouchApp as app
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.scatter import Scatter
from kivy.lang import Builder 
from kivy.metrics import dp

# module resources
from kivy.resources import resource_add_path
resource_add_path(os.path.dirname(os.path.realpath(__file__)))

__all__ = ('IphoneScreen', 'IpadScreen', 'AndroidPhoneScreen', 'AndriodTabScreen', )

class ScreenScatter(Scatter):
    ''' base widget for screens'''

    angle = NumericProperty(0)

    orientation = StringProperty('portrait')
	
    container = ObjectProperty(None)

    border_size =ListProperty([0,0])

    border_pos =ListProperty([0,0])

    def __init__(self, **k):
        super(ScreenScatter, self).__init__(**k)
        self.bind(pos=self.set_border)
        self.bind(size=self.set_border)

    def set_border(self, *a):
        # overide to set borderimage valuese
        pass

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

    def on_orientation(self, *a):
        if self.orientation == 'portrait':
            self.angle = 0
            self.container.size = (self.height,self.width)
        elif self.orientation == 'landscape':
            self.angle = -90
            self.container.size = (self.height,self.width)

        self.set_border(from_orientation=True)

    # overiding
    def set_border(self, *a, **k):
        if self.orientation == 'portrait':
            self.border_pos = (-dp(16.5), -dp(85.5))
            self.border_size = (self.container.width + dp(32), self.container.height + dp(152))
        elif self.orientation == 'landscape':
            self.border_pos = (-self.container.height-16.5, -dp(85.5))

        try:
            from_orientation = k.pop('from_orientation')
        except KeyError:
            from_orientation = False

        if from_orientation:
            self.center = self.parent.center
        

Builder.load_file('screen.kv')



if __name__ == "__main__":
    app(build)
