from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivystudio.behaviors import HoverBehavior
from kivystudio.components.screens import AndroidPhoneScreen
from kivystudio.widgets.iconlabel import IconButtonLabel

__all__ = ('EmulatorArea')

class EmulatorArea(BoxLayout):

    screen_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EmulatorArea, self).__init__(**kwargs)
        self.screen_manager = EmulatorScreens()
        self.add_widget(self.screen_manager)
        self.screen_display = ScreenDisplay()
        self.add_widget(self.screen_display)
    
    def add_widget(self, widget):
        if len(self.children) > 1:
            self.screen_manager.add_widget(widget, widget.name)
            tab = EmulatorTab(text=widget.name)
            self.ids.tab_manager.add_widget(tab)

        else:
            super(EmulatorArea, self).add_widget(widget)

    def toggle_orientation(self):
        if self.screen_display.screen.orientation =='portrait': 
            self.screen_display.screen.orientation ='landscape'
        else:
            self.screen_display.screen.orientation ='portrait'


class ScreenTopMenu(BoxLayout):
    
    screen = ObjectProperty(None)


class EmulatorTab(HoverBehavior, ToggleButtonBehavior,Label):

    def on_hover(self, *args):
        if self.hover:
            self.color = 1,1,1,1
        else:
            if not self.bold:
                self.color = .5,.5,.5,1

    def on_state(self, *args):
        if self.state == 'down':
            self.bold=True
            if not self.text.startswith('[u]'):
                self.text = '[u]'+self.text+'[/u]'
        else:
            self.bold=False
            self.text = self.text.replace('[u]','').replace('[/u]','')



class EmulatorScreens(ScreenManager):
    
    def add_widget(self, widget, name):
        screen = Screen(name=name)
        screen.add_widget(widget)
        super(EmulatorScreens, self).add_widget(screen)



class ScreenDisplay(HoverBehavior, FloatLayout):
    
    screen = ObjectProperty(None)

    topmenu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenDisplay, self).__init__(**kwargs)
        self.scaler = ScreenTopMenu()
        self.screen = AndroidPhoneScreen()

    def on_hover(self, *args):
        pass
        # if self.hover:
        #     if self.scaler not in self.children:
        #         self.add_widget(self.scaler)
        # else:
        #     if self.scaler in self.children:
        #             Clock.schedule_once(
        #                 lambda dt: self.remove_widget(self.scaler), 0.5)

    def on_screen(self, obj, screen):
        if self.screen not in self.children:
            self.add_widget(screen)
            self.screen.bind(scale=lambda *args: setattr(self.screen, 'center', self.center))
            self.bind(center=self.screen.setter('center'))
            self.scaler.screen = screen



Builder.load_string('''

<EmulatorArea>:
    orientation: 'vertical'
    ScrollView:
        size_hint_y: None
        height: '36dp'
        canvas.before:
            Color:
                rgba: (0.12, 0.12, 0.12, 1)
            Rectangle:
                size: self.size
                pos: self.pos

        GridLayout:
            rows: 1
            id: tab_manager
            size_hint_x: None
            width: self.minimum_width

            Label:
                size_hint_x: None
                width: '106dp'
                text: 'main.py'
            IconButtonLabel:
                color: .8,.8,.8,1
                size_hint_x: None
                width: '36dp'
                text: icon('fa-search-minus')
                on_release:
                    if not root.screen_display.screen.scale < -100.0: root.screen_display.screen.scale -= 0.05
            IconButtonLabel:
                color: .8,.8,.8,1
                text: icon('fa-search-plus')
                size_hint_x: None
                width: '36dp'
                icon_source: 'images/scale2.png'
                on_release: root.screen_display.screen.scale += 0.05
            IconToggleLabel:
                color: .8,.8,.8,1
                text: icon('fa-tablet')
                size_hint_x: None
                width: '36dp'
                angle:0
                on_state:
                    root.toggle_orientation();
                    if self.state=='down': self.angle=90
                    else: self.angle=0
                canvas:
                    Clear
                    PushMatrix
                    Rotate:
                        angle: self.angle
                        origin: self.center_x , self.center_y
                    Rectangle:
                        size: self.texture_size
                        pos: self.center_x - 8, self.center_y - 8
                        texture: self.texture
                    PopMatrix
                    


<EmulatorTab>:
    size_hint_x: None
    width: '100dp'
    # allow_no_selection: False
    group: 'emulator_tab'
    font_size: '13.5dp'
    color: .5,.5,.5,1
    markup: True



<ScreenDisplay>:
    name: 'Emulator'
    canvas.before:
        Color:
            rgba: .5,.5,.5,1
        Rectangle:
            size: self.size
            pos: self.pos


''')
