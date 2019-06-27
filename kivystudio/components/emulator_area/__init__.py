from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock

from kivystudio.behaviors import HoverBehavior
from kivystudio.components import screens
from kivystudio.widgets.iconlabel import IconButtonLabel

from .screen_drop import ScreenDrop

import os
__all__ = ('get_emulator',)
filepath = os.path.dirname(__file__)
Builder.load_file(os.path.join(filepath,'emulator.kv'))

class EmulatorArea(BoxLayout):

    screen_display = ObjectProperty(None)

    emulation_file = StringProperty('')

    def __init__(self, **kwargs):
        super(EmulatorArea, self).__init__(**kwargs)
        self.screen_manager = EmulatorScreens()
        self.add_widget(self.screen_manager)
        self.screen_display = ScreenDisplay()
        self.screen_manager.add_widget(self.screen_display)
    
    def add_widget(self, widget):
        super(EmulatorArea, self).add_widget(widget)

    def toggle_orientation(self):
        if self.screen_display.screen.orientation =='portrait': 
            self.screen_display.screen.orientation ='landscape'
        else:
            self.screen_display.screen.orientation ='portrait'

    def open_screen_drop(self,widget):
        ScreenDrop().open(widget, self.screen_display)


class ScreenTopMenu(BoxLayout):
    
    screen = ObjectProperty(None)



class EmulatorScreens(ScreenManager):
    
    def add_widget(self, widget):
        screen = Screen()
        screen.add_widget(widget)
        super(EmulatorScreens, self).add_widget(screen)



class ScreenDisplay(HoverBehavior, FloatLayout):
    
    screen = ObjectProperty(None)

    topmenu = ObjectProperty(None)

    screen_name = StringProperty('')

    def __init__(self, **kwargs):
        super(ScreenDisplay, self).__init__(**kwargs)
        self.scaler = ScreenTopMenu()
        self.screen_name = 'AndroidPhoneScreen'

    def on_hover(self, *args):
        pass

    def on_screen_name(self, obj, screen):
        self.screen = getattr(screens, self.screen_name)()

    def on_screen(self, obj, screen):
        children = self.children[0].container.children if self.children else None
        child = children[0] if children else None
        if child:
            self.children[0].container.remove_widget(child)
            screen.add_widget(child)

        self.clear_widgets()
        self.add_widget(screen)
        self.screen.bind(scale=lambda *args: setattr(self.screen, 'center', self.center))
        self.bind(center=self.screen.setter('center'))
        self.scaler.screen = screen

instatance=[]


def emulator_area():
    if instatance:
        return instatance[0]
    else:
        emulator_area = EmulatorArea(size_hint_x=.45)
        instatance.append(emulator_area)
        return emulator_area
