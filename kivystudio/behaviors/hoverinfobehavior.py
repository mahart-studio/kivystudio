'''
Mixin behavior widget that inherits from kivystudio.behavior.HoverBehavior
used on a widget, to show extra infomation on what the widgets does
by hovering on it

Simple usages:

class MyButton(HoverInfoBehavior, Button):

    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.info_text = 'Click me'

        # or if the info text might change you, could bind it to an atrr
        self.mytext = 'somthing'
        self.info_text_attr = 'mytext'



'''
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivystudio.tools import infolabel

from .hoverbehavior import HoverBehavior

class HoverInfoBehavior(HoverBehavior):

    info_text = StringProperty('')
    
    info_text_attr = StringProperty('')

    def on_parent(self, *a):
        if self.parent is None:
            infolabel.remove_info_on_mouse()
        return super(HoverInfoBehavior, self).on_parent(*a)

    def on_hover(self, *a):
        if self.hover:
            Clock.schedule_once(self.show_label_info,1)
        else:
            Clock.unschedule(self.show_label_info)
            infolabel.remove_info_on_mouse()

    def show_label_info(self,dt):
        info_text = self.info_text
        if self.info_text_attr:
            info_text = getattr(self, self.info_text_attr)

        # if info_text:
        infolabel.show_info_on_mouse(info_text)
