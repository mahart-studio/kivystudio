import os

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
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

    root_widget = ObjectProperty(None, allow_none=True)

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
            self.root_widget = widget
            if widget.parent:
                widget.parent.remove_widget(widget)
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


class IphoneScreen(ScreenScatter):
    @property
    def set_pos(self):
        pos = (-25, -dp(133))
        if self.orientation == 'landscape':
            return (-self.container.height+pos[0], pos[1])
        return pos

    @property
    def set_size(self):

        return (self.width + dp(50), self.height + dp(270))

class IpadScreen(ScreenScatter):
    @property
    def set_pos(self):
        pos = (-dp(95), -dp(77))
        if self.orientation == 'landscape':
            return (-self.container.height+pos[0], pos[1])
        return pos

    @property
    def set_size(self):
        return (self.width + dp(190), self.height + dp(154))

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


class ScreenContainer(FloatLayout):

    # overide
    def add_widget(self,widget):
        if len(self.children) > 1:
            screen = self.ids.inner_container.get_screen('container')
            screen.add_widget(widget)
            # self.ids.inner_container.add_widget(screen)
        else:
            super(ScreenContainer,self).add_widget(widget)

    # overide
    def clear_widgets(self):
        screen = self.ids.inner_container.get_screen('container')
        screen.clear_widgets()

Builder.load_file('screen.kv')



if __name__ == "__main__":
    from kivy.base import runTouchApp as app
    app(build)
