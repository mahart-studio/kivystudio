from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ListProperty, ObjectProperty
from kivy.utils import get_color_from_hex

from kivystudio.behaviors import HoverBehavior
from kivystudio.widgets.rightclick_drop import RightClickDrop

from .styles import NativeTweakStyle
from .codeinput import CodeInput
from .code_find import CodeInputFind
from .code_extra_behavior import CodeExtraBehavior

import os
from pygments import styles

class CodeInputDropDown(RightClickDrop):
    ''' DropDown widget show when mouse 
        is right clicked on CodeInput
        '''

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # so doesn't unfocus input
            FocusBehavior.ignored_touch.append(touch)
        return super(CodeInputDropDown,self).on_touch_down(touch)
    
    def open(self, code_input):
        self.codeinput = codeinput
        super(CodeInputDropDown,self).open()

    def copy(self):
        self.codeinput.copy()

    def paste(self):
        self.codeinput.paste()

    def cut(self):
        self.codeinput.cut()


class InnerCodeInput(HoverBehavior, CodeExtraBehavior, CodeInput):

    path = StringProperty('')
    '''Path of the current file
        `path` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''
    '''

    rightclick_dropdown = None
    ''' drop down menu that appears when the right click button is clicked
        `rightclick_dropdown` is an instance of .code_find.CodeInputFind
        '''
    code_finder = None
    '''  '''

    def __init__(self, **kwargs):
        super(InnerCodeInput, self).__init__(**kwargs)
        self.style_name = 'native'
        self.background_normal= ''
        self.background_active= ''

    def on_style_name(self, *args):
        self.style = NativeTweakStyle
        self.background_color = get_color_from_hex(self.style.background_color)
        self._trigger_refresh_text()

    def on_text(self, *args):
        if self.focus:
            self.parent.saved = False
            self.check_settings()

    def check_settings(self):
        from kivystudio.settings import settings_obj
        auto_save = settings_obj.auto_save
        auto_emulate = settings_obj.auto_emulate
        if auto_save:
            self.parent.parent.save_file(auto_save=True)
        if auto_emulate:
            from kivystudio.parser import emulate_file
            from kivystudio.components.emulator_area import get_emulator_area
            if get_emulator_area().emulation_file == self.parent.filename:
                emulate_file(self.parent.filename)

    def keyboard_on_textinput(self, window, text):
        'overiding the default textinput keyboard listener '
        if (text == '=' or text == '-') and 'ctrl' in Window.modifiers:
            return True
        super(InnerCodeInput,self).keyboard_on_textinput(window, text)

    def keyboard_on_key_down(self, keyboard, keycode, text, modifiers):
        'overiding the default keyboard listener '
        # print(keycode, modifiers)

        if keycode[1] == 'tab' and 'shift' in modifiers:  # unindentation [Shit-tab]
            self._do_reverse_indentation()

        elif keycode[1] == 'tab' and self.selection_text:  # multiple indentation [Tab]
            self.do_multiline_indent()

        elif keycode[1] == 'backspace' and 'ctrl' in modifiers:   # delete word left  [Ctrl-bsc]
            self.delete_word_left()

        elif keycode[1] == '/' and 'ctrl' in modifiers:     # a comment ctrl /
            self.do_comment()

        elif keycode[1] == 'enter':
            Clock.schedule_once(lambda dt: self.do_auto_indent())
            return super(CodeInput, self).keyboard_on_key_down(keyboard, keycode, text, modifiers)

        elif keycode[1] == 'f' and 'ctrl' in modifiers:     # ctrl f to open a search
            self.open_code_finder()

        elif keycode[0] == 27:     # on escape, do nothing
            return True

        else:
            # then return super for others
            return super(CodeInput, self).keyboard_on_key_down(keyboard, keycode, text, modifiers)
    
    def open_code_finder(self):
        ''' open the search finder 
            on the codeinput '''
        code_finder = InnerCodeInput.code_finder
        if code_finder:
            code_finder.open(self)
        else:
            InnerCodeInput.code_finder = CodeInputFind()
            InnerCodeInput.code_finder.open(self)
    
    def open_rightclick_dropdown(self):
        ''' open the dropdown right click 
            on the codeinput '''
        rightclick_dropdown = InnerCodeInput.rightclick_dropdown
        if rightclick_dropdown:
            rightclick_dropdown.open()
        else:
            InnerCodeInput.rightclick_dropdown = CodeInputDropDown()
            InnerCodeInput.rightclick_dropdown.open(self)

    def on_hover(self, *a):
        ''' changing the mouse cursor 
            on code input'''
        if self.hover:
            Window.set_system_cursor('ibeam')  # set cursor to ibeam
        else:
            Window.set_system_cursor('arrow')  # set cursor to arrow

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.open_rightclick_dropdown()
                FocusBehavior.ignored_touch.append(touch)
                return True

        if touch.button == 'left':
            return super(InnerCodeInput,self).on_touch_down(touch)


class NumberingGrid(ScrollView):

    def on_touch_down(self, touch):
        if self.collide_point( *touch.pos):
            FocusBehavior.ignored_touch.append(touch)
            super(NumberingGrid, self).on_touch_down(touch)

class ScrollingBar(ScrollView):

    def on_touch_down(self, touch):
        if self.collide_point( *touch.pos):
            FocusBehavior.ignored_touch.append(touch)
            super(ScrollingBar, self).on_touch_down(touch)


class FullCodeInput(GridLayout):

    _do_cursor_scroll =BooleanProperty(True)

    code_input = ObjectProperty(None)

    tab = ObjectProperty(None)

    tab_type = StringProperty('code')

    filename = StringProperty('')
    ''' name current file in the input 
            :data:`filename` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''
    '''

    saved = BooleanProperty(True)
    '''Indicates if the current file is saved or not
        :data:`saved` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True
    '''

    def __init__(self, **kwargs):
        super(FullCodeInput, self).__init__(**kwargs)
        Clock.schedule_once(self.first_number)
        self._former_line_lenght = 1
        self.first_time = True


    def first_number(self, dt):
        label = Numbers_(height=dp(self.ids.code_input.line_height), text=str(1))
        Clock.schedule_once(lambda dt: setattr(label, 'state', 'down'))
        label.fbind('on_press', self._number_pressed)
        self.ids.numbering.add_widget(label)
        self._former_line_lenght = 1


    def _number_pressed(self, lb):
        self.ids.code_input.cursor = (self.ids.code_input.cursor[0], int(lb.text)-1)


    def change_scroll_y(self, txt, scroll):
        if self._do_cursor_scroll:

            lines_lenght = len(txt._lines)
            line_pos = txt.cursor_row +1

            norm_y = float(line_pos) / lines_lenght
            scroll.scroll_y  = abs(norm_y-1)
            if line_pos == 1:
                scroll.scroll_y  = 1

        # scroll scroll numbers
        line_num =  txt.cursor_row + 1
        children = self.ids.numbering.children[::-1]
        if children:
            child = children[line_num-1]
            self.ids.number_scroll.scroll_to(child, dp(5))

            Clock.schedule_once(lambda dt: setattr(child, 'state', 'down'))
            def toggle(chd):
                if chd!=child:
                    chd.state='normal'
            map(lambda child: toggle, ToggleButtonBehavior.get_widgets(child.group))


    def do_bar_scroll(self, txt, scroll):
        lines_lenght = len(txt._lines)
        line_pos = int(abs(scroll.scroll_y-1) * lines_lenght)
        cursor_y = abs(line_pos)

        txt.cursor = (txt.cursor_col, cursor_y)

    def number_me(self, txt, scroll):
        lines_lenght = len(txt._lines)
        line_pos = txt.cursor_row +2

        if not(lines_lenght <= 1) or not(self.first_time):

            if lines_lenght >= self._former_line_lenght:

                if line_pos == lines_lenght:
                    self.do_new_line(txt, scroll)
                else:
                    self.do_new_line(txt, scroll)

            else:
                self.remove_line_numbering(txt, scroll)
            
            self._former_line_lenght = lines_lenght
        self.first_time = False

    def do_new_line(self, txt, scroll):
        lines_lenght = len(txt._lines)

        for line_num in range(self._former_line_lenght+1, lines_lenght+1):

            label = Numbers_(height=dp(self.ids.code_input.line_height), text=str(line_num))
            label.fbind('on_press', self._number_pressed)
            self.ids.numbering.add_widget(label)
        
    def remove_line_numbering(self, txt, scroll):
        lines_lenght = len(txt._lines)

        for line_num in range(lines_lenght+1, self._former_line_lenght+1):
            child = self.ids.numbering.children[0]
            self.ids.numbering.remove_widget(child)
        

class Numbers_(ToggleButtonBehavior, Label):

    selected_color = ListProperty([1,1,1,1])
    ' color of the number when selected'

    normal_color = ListProperty([.5,.5,.5,1])
    ' color of the number when selected'
    
    def on_state(self, *args):

        if self.state == 'down':
            self.color = self.selected_color
            self.canvas_color = self.normal_color[:3]+[.3]
        else:
            self.color = self.normal_color
            self.canvas_color = [0,0,0,0]



Builder.load_file(os.path.join(os.path.dirname(__file__),'codeinput.kv'))



if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(FullCodeInput())


    'rrt, xcode, friendly, algol'
