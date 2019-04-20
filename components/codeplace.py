
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.extras.highlight import KivyLexer

from kivystudio.behaviors import HoverBehavior

import os

def get_tab_from_group(filename):
    all_tabs = ToggleButtonBehavior.get_widgets('__tabed_btn__')
    if all_tabs:
        for tab in all_tabs:
            if tab.filename == filename:
                return tab
                break


class CodeScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(CodeScreenManager, self).__init__(**kwargs)
        self.transition = NoTransition()

    def add_widget(self, widget, name):
        if os.path.splitext(widget.filename)[1] == '.kv':
            widget.code_input.lexer = KivyLexer()

        screen = CodeScreen(name=name)
        screen.add_widget(widget)
        Clock.schedule_once(lambda dt: self.open_file(widget))       # open the file
        super(CodeScreenManager, self).add_widget(screen)


    def open_file(self, code_input):
        if os.path.exists(code_input.filename):
            with open(code_input.filename, 'r') as f:
                code_input.code_input.focus = False    
                code_input.code_input.text = f.read()


class CodeScreen(HoverBehavior, Screen):
    
    code_field = ObjectProperty(None)

    def on_pre_enter(self):
        self.code_field.code_input.focus = True
        Window.bind(on_key_down=self.keyboard_down)

        tab = get_tab_from_group(self.name)
        if tab:
            Clock.schedule_once(lambda dt: setattr(tab, 'state', 'down'))
            checked_list = list(filter(lambda child: child != tab, ToggleButtonBehavior.get_widgets(tab.group)))
            Clock.schedule_once(lambda dt: map(lambda child: setattr(child, 'state', 'normal'), checked_list))

    def on_pre_leave(self):
        Window.unbind(on_key_down=self.keyboard_down)

    def on_enter(self):
        self.code_field.code_input.focus = True


    def save_file(self):
        with open(self.name, 'w') as fn:
            fn.write(self.code_field.code_input.text)

        self.code_field.saved = True

    def add_widget(self, widget):
        self.code_field = widget
        super(CodeScreen, self).add_widget(widget)
        self.code_field.bind(saved=self.saving_file)

    def saving_file(self, ins, saved):
        tab = get_tab_from_group(self.name)
        tab.saved = saved       

    def keyboard_down(self, window, *args):
        # print(args)
        
        if args[0] == 115 and args[3] == ['ctrl']:
            self.save_file()

            return False

    def on_hover(self, *a):
        if self.hover:
            Window.set_system_cursor('ibeam')
        else:
            Window.set_system_cursor('arrow')


class TabToggleButton(ToggleButtonBehavior, Label):

    filename = StringProperty('')

    saved = BooleanProperty(True)

    def on_saved(self, *args):
        if not self.saved:
            self.text += ' *'
        else:
            if self.text.endswith(' *'):
                self.text = self.text[:len(self.text)-2]

#switching

class CodePlace(BoxLayout):
    
    code_manager = ObjectProperty(None)

    tab_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CodePlace, self).__init__(**kwargs)
        self.code_manager = CodeScreenManager()
        self.add_widget(self.code_manager)
        Window.bind(on_key_down=self.keyboard_down)

    def add_widget(self, widget):
        if len(self.children) > 1:
            self.code_manager.add_widget(widget, widget.filename)
            tab = TabToggleButton(text=os.path.split(widget.filename)[1],
                                 filename=widget.filename)
            tab.bind(state=self.change_screen)
            self.tab_manager.add_widget(tab)
            Clock.schedule_once(lambda dt: setattr(tab, 'state', 'down'))

        else:
            super(CodePlace, self).add_widget(widget)


    def change_screen(self, tab, state):
        if state == 'down':
            self.code_manager.current = tab.filename


    def keyboard_down(self, window, *args):

        if args[0] == 9 and args[3] == ['ctrl']:   # switching screen with ctrl tab
            self.code_manager.current = self.code_manager.next()

            return True


Builder.load_string('''
<CodePlace>:
    tab_manager: tab_manager
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


<TabToggleButton>:
    size_hint_x: None
    width: '100dp'
    canvas_color: (0.12, 0.12, 0.12, 1)
    allow_no_selection: False
    group: '__tabed_btn__'
    font_size: '13.5dp'
    on_state:
        if self.state == 'down': self.canvas_color= (.2,.2,.2,1)
        else: self.canvas_color= (0.12, 0.12, 0.12, 1)
    canvas.before:
        Color:
            rgba: self.canvas_color
        Rectangle:
            size: self.size
            pos: self.pos

''')
