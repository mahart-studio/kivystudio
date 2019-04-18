from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivystudio.behaviors import HoverBehavior
from kivystudio.screens import AndroidPhoneScreen

__all__ = ('EmulatorArea')

class EmulatorArea(TabbedPanel):
    pass


class ScreenScaler(BoxLayout):
    
    screen = ObjectProperty(None)


class ScreenDisplay(HoverBehavior, FloatLayout):
    
    screen = ObjectProperty(None)

    scaler = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenDisplay, self).__init__(**kwargs)
        self.scaler = ScreenScaler()
        self.screen = AndroidPhoneScreen()

    def on_hover(self, *args):
        if self.hover:
            if self.scaler not in self.children:
                self.add_widget(self.scaler)
        else:
            if self.scaler in self.children:
                    Clock.schedule_once(
                        lambda dt: self.remove_widget(self.scaler), 0.5)

    def on_screen(self, obj, screen):
        if self.screen not in self.children:
            self.add_widget(screen)
            self.screen.bind(scale=lambda *args: setattr(self.screen, 'center', self.center))
            self.bind(center=self.screen.setter('center'))
            self.scaler.screen = screen



Builder.load_string('''

<EmulatorArea>:
    # size_hint_x: .45
    do_default_tab: False
    EmulatorTabItem:
        text: 'Emulator'
        ScreenDisplay:
    EmulatorTabItem:
        text: 'Problems  4'
    EmulatorTabItem:
        text: 'Terminal'
    EmulatorTabItem:
        text: 'Debug'



<ScreenDisplay>:
    canvas.before:
        Color:
            rgba: .6,.6,.6,1
        Rectangle:
            size: self.size
            pos: self.pos


<ScreenScaler>:
    pos_hint: {'y': .01, 'center_x': .5}
    size_hint: None,None
    size: '110dp', '46dp'
    Button:
        text: '-'
        bold: True
        on_release:
            if not root.screen.scale < -100.0: root.screen.scale -= 0.05
    Button:
        text: '+'
        bold: True
        on_release: root.screen.scale += 0.05

<EmulatorTabItem@TabbedPanelItem>:
    # background_down: ''
    # background_normal: ''
    # background_color: 0,0,0,0
    # canvas.before:
    #     Clear
    #     Color:
    #         rgba: 1,.4,.4,1
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos

''')
