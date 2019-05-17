from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import (StringProperty,
                            ObjectProperty,
                            BooleanProperty)

from kivystudio.behaviors import HoverBehavior
from kivystudio.tools import infolabel
from kivystudio.tools import set_auto_mouse_position

class TabToggleButton(HoverBehavior, ToggleButtonBehavior, BoxLayout):

    filename = StringProperty('')

    saved = BooleanProperty(True)

    text = StringProperty('')

    rightclick_dropdown = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TabToggleButton, self).__init__(**kwargs)
        self.rightclick_dropdown = CodeTabDropDown(self)

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
        print(self.hover)
        if self.hover:
            Clock.schedule_once(self.show_label_info,1)
        else:
            Clock.unschedule(self.show_label_info)
            infolabel.remove_info_on_mouse()

    def show_label_info(self,dt):
        print(self.filename)
        infolabel.show_info_on_mouse('sdsdgsdfgsdg')

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.show_right_click_info()
                FocusBehavior.ignored_touch.append(touch)
                return True

        if touch.button == 'left':
            super(TabToggleButton, self).on_touch_down(touch)

    def show_right_click_info(self):
        if self.rightclick_dropdown in Window.children:
           return
        else:
            set_auto_mouse_position(self.rightclick_dropdown)
            Window.add_widget(self.rightclick_dropdown) 

class CodeTabDropDown(BoxLayout):

    def __init__(self, codeinput, **kwargs):
        super(CodeTabDropDown, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # touch should not unfocus input
            FocusBehavior.ignored_touch.append(touch)
        return super(CodeTabDropDown,self).on_touch_down(touch)

    def set_for_emulation(self):
        pass


class TabPannelIndicator(HoverBehavior, ButtonBehavior, Image):
        
    def on_hover(self, *a):
        if self.hover:
            self.source='images/cancel.png'
        elif not self.hover and not self.parent.saved:
            self.source='images/dot.png'
        elif not self.hover and self.parent.saved and self.parent.state=='normal':
            self.source='images/invisible.png'
        elif not self.hover and self.parent.saved and self.parent.state=='down':
            self.source='images/cancel.png'
