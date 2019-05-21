
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, ScreenManagerException
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior, FocusBehavior
from kivy.properties import (ObjectProperty,
                            NumericProperty)
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.extras.highlight import KivyLexer

from kivystudio.widgets.codeinput import FullCodeInput
from .codetab import TabToggleButton

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
        Clock.schedule_once(lambda dt: self.open_file(widget),1)       # open the file
        super(CodeScreenManager, self).add_widget(screen)

    def open_file(self, code_input):
        if os.path.exists(code_input.filename):
            with open(code_input.filename, 'r') as f:
                code_input.code_input.focus = False    
                code_input.code_input.text = f.read()

    def get_children_with_filename(self, filename):
        try:
            child = filter(lambda child: child.name==filename, self.children)[0]
            return child
        except IndexError:
            raise Exception('code manager as no child with such filename {}'.format(filename))

class CodeScreen(Screen):
    
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
        
        if args[0] == 115 and args[3] == ['ctrl']:  # save file Ctrl+S
            self.save_file()

            return False


#switching

class CodePlace(BoxLayout):
    
    code_manager = ObjectProperty(None)

    tab_manager = ObjectProperty(None)

    new_empty_tab = NumericProperty(0)
    '''count of empty tabs that has been opened
    '''

    def __init__(self, **kwargs):
        super(CodePlace, self).__init__(**kwargs)
        self.code_manager = CodeScreenManager()
        self.add_widget(self.code_manager)
        Window.bind(on_key_down=self.keyboard_down)
        Window.bind(on_dropfile=self.file_droped)

    def file_droped(self, window, filename, *args):
        if self.collide_point(*window.mouse_pos):
            print('File droped on code input')
            if filename:
                self.add_code_tab(filename=filename)

    def add_widget(self, widget):
        if len(self.children) > 1:
            self.code_manager.add_widget(widget, widget.filename)
            tab = TabToggleButton(text=os.path.split(widget.filename)[1],
                                 filename=widget.filename)
            tab.bind(state=self.change_screen)
            print(tab.text)
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

        if args[0] == 119 and args[3] == ['ctrl']:   # close tab
            filename = self.code_manager.get_screen(self.code_manager.current).children[0].filename
            tab = get_tab_from_group(filename)
            self.remove_code_tab(tab)

    def remove_code_tab(self, tab):
        self.tab_manager.remove_widget(tab)
        codeinput=self.code_manager.get_children_with_filename(tab.filename)
        self.code_manager.remove_widget(codeinput)

        print(tab.filename)
        if tab.filename.startswith('Untitled-') and not os.path.exists(tab.filename):
            self.new_empty_tab -= 1

    def add_code_tab(self, filename=''):
        if filename:
            try:
                self.code_manager.get_screen(filename)
            except ScreenManagerException:   # then it is not added
                self.add_widget(FullCodeInput(filename=filename))
        else:   # a new tab
            self.new_empty_tab += 1
            while True:
                try:
                    self.code_manager.get_screen(filename)
                except ScreenManagerException:   # then it is not added
                    filename = 'Untitled-{}'.format(self.new_empty_tab)
                    self.add_widget(FullCodeInput(filename=filename))
                    return
                self.new_empty_tab += 1



class CodeTabsContainer(ScrollView):
    '''horizontal scrollview where the small tab 
        buttons lay'''

    def on_touch_down(self, touch):
        FocusBehavior.ignored_touch.append(touch)
        return super(CodeTabsContainer, self).on_touch_down(touch)

Builder.load_file(os.path.join(os.path.dirname(__file__), 'code.kv'))
