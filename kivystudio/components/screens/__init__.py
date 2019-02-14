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

    source = StringProperty('')

    def __init__(self, **k):
        super(ScreenScatter, self).__init__(**k)
        self.bind(pos=self.set_border)
        self.bind(size=self.set_border)

    def add_widget(self, widget):
        if len(self.children) > 0:
            self.container.add_widget(widget)
        else:
            super(ScreenScatter, self).add_widget(widget)

    def clear_widgets(self):
        self.container.clear_widgets()

    def on_orientation(self, *a):
        if self.orientation == 'portrait':
            self.angle = 0
            self.container.size = (self.height,self.width)
        elif self.orientation == 'landscape':
            self.angle = -90
            self.container.size = (self.height,self.width)

        self.set_border(from_orientation=True)

    def set_border(self, *a, **k):
        if self.orientation == 'portrait':
            self.border_pos = self.set_pos 
            self.border_size = self.set_size
        elif self.orientation == 'landscape':
            self.border_pos = self.set_pos

        try:
            from_orientation = k.pop('from_orientation')
        except KeyError:
            from_orientation = False

        if from_orientation:
            self.center = self.parent.center

    def on_parent(self,*a):
        if self.parent:
            self.set_border()
            self.center = self.parent.center

    @property
    def set_pos(self):
        pass

    @property
    def set_size(self):
        pass

    

class ScreenContainer(RelativeLayout):
    pass


class IphoneScreen(ScreenScatter):

    @property
    def set_pos(self):
        if self.orientation == 'landscape':
            return (-self.container.height-21, -dp(138))
        return (-dp(21), -dp(138))

    @property
    def set_size(self):
        return (self.width + dp(42), self.height + dp(280))

class IpadScreen(ScreenScatter):
    @property
    def set_pos(self):
        if self.orientation == 'landscape':
            return (-self.container.height-99, -dp(51))
        return (-dp(99), -dp(51))

    @property
    def set_size(self):
        return (self.width + dp(118), self.height + dp(102))
        
class AndriodTabScreen(ScreenScatter):
    @property
    def set_pos(self):
        if self.orientation == 'landscape':
            return (-self.container.height-35, -dp(51))
        return (-dp(35), -dp(51))

    @property
    def set_size(self):
        return (self.width + dp(70), self.height + dp(102))

class AndroidPhoneScreen(ScreenScatter):
    @property
    def set_pos(self):
        if self.orientation == 'landscape':
            return (-self.container.height-16.5, -dp(85.5))
        return (-dp(16.5), -dp(85.5))

    @property
    def set_size(self):
        return (self.container.width + dp(32), self.container.height + dp(152))


Builder.load_file('screen.kv')



if __name__ == "__main__":
    app(build)
