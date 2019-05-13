from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (StringProperty,
                            ObjectProperty,
                            BooleanProperty)
from kivy.uix.boxlayout import BoxLayout

from kivystudio.behaviors import HoverBehavior
from kivystudio.tools import infolabel

class TabToggleButton(HoverBehavior, ToggleButtonBehavior, BoxLayout):

    filename = StringProperty('')

    saved = BooleanProperty(True)

    text = StringProperty('')

    rightclick_dropdown = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TabToggleButton, self).__init__(**kwargs)
        self.rightclick_dropdown = None

    def on_saved(self, *args):
        if self.saved:
            self.ids.indicator.source ='images/invisible.png'
        elif not self.saved and self.state=='down':
            self.ids.indicator.source = 'images/dot.png'

    def on_state(self, *args):
        if self.state=='down' and not self.saved:
            self.ids.indicator.source ='images/dot.png'
        elif self.state=='down' and self.saved:
            self.ids.indicator.source ='images/cancel.png'
        elif self.state=='normal':
            self.ids.indicator.source ='images/invisible.png'
        
    def on_parent(self, *a):
        infolabel.remove_info_on_mouse()

    def on_hover(self, *a):
        if self.hover:
            Clock.schedule_once(self.show_label_info,1)
        else:
            Clock.unschedule(self.show_label_info)
            infolabel.remove_info_on_mouse()

    def show_label_info(self,dt):
        infolabel.show_info_on_mouse('/root/kivy/kivystudio/main.py')

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                pass

        if touch.button == 'left':
            super(TabToggleButton, self).on_touch_down(touch)
