from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import (StringProperty,
                            ObjectProperty,
                            BooleanProperty)

from kivystudio.behaviors import HoverBehavior
from kivystudio.widgets.iconlabel import HoverIconButtonLabel
from kivystudio.widgets.rightclick_drop import RightClickDrop
from kivystudio.tools import infolabel
from kivystudio.tools import set_auto_mouse_position
from kivystudio.tools.iconfonts import icon
from kivystudio.components.emulator_area import emulator_area


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
            self.ids.indicator.text =''
        elif not self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-circle'))
            self.ids.indicator.font_size = '12dp'

    def on_state(self, *args):
        if self.state=='down' and not self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-circle'))
            self.ids.indicator.font_size = '12dp'
        elif self.state=='down' and self.saved:
            self.ids.indicator.text = '%s' % (icon('fa-close'))
            self.ids.indicator.font_size = '16dp'
        elif self.state=='normal':
            self.ids.indicator.source =''
 
    def on_parent(self, *a):
        if self.parent is None:
            infolabel.remove_info_on_mouse()
        return super(TabToggleButton, self).on_parent(*a)

    def on_hover(self, *a):
        if self.hover:
            Clock.schedule_once(self.show_label_info,1)
        else:
            Clock.unschedule(self.show_label_info)
            infolabel.remove_info_on_mouse()

    def show_label_info(self,dt):
        infolabel.show_info_on_mouse(self.filename)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.rightclick_dropdown.open()
                FocusBehavior.ignored_touch.append(touch)
                return True

        if touch.button == 'left':
            super(TabToggleButton, self).on_touch_down(touch)


class CodeTabDropDown(RightClickDrop):

    def __init__(self, tab, **kwargs):
        super(CodeTabDropDown, self).__init__(**kwargs)
        self.tab = tab

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # touch should not unfocus input
            FocusBehavior.ignored_touch.append(touch)
        return super(CodeTabDropDown,self).on_touch_down(touch)

    def set_for_emulation(self):
        print(self.tab.filename)
        emulator_area().emulation_file=self.tab.filename


class TabPannelIndicator(HoverIconButtonLabel):
        
    def on_hover(self, *a):
        if self.hover:
            self.text = '%s' % (icon('fa-close'))
            self.font_size = '16dp'
        if not self.hover and not self.parent.saved:
            self.text = '%s' % (icon('fa-circle'))
            self.font_size = '12dp'
        if not self.hover and self.parent.saved and self.parent.state=='normal':
            self.text = ''
        if not self.hover and self.parent.saved and self.parent.state=='down':
            self.text = '%s' % (icon('fa-close'))
            self.font_size = '16dp'
