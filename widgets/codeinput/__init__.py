
from kivy.properties import BooleanProperty, StringProperty, ListProperty, ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout

from pygments import styles

from .codeinput import CodeInput
from kivystudio.behaviors import HoverBehavior
from kivystudio.tools import set_auto_mouse_position
from kivystudio.widgets.rightclick_drop import RightClickDrop

class CodeInputDropDown(RightClickDrop):

    def __init__(self, codeinput, **kwargs):
        super(CodeInputDropDown, self).__init__(**kwargs)
        self.codeinput = codeinput

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # touch should not unfocus input
            FocusBehavior.ignored_touch.append(touch)
        return super(CodeInputDropDown,self).on_touch_down(touch)

    def copy(self):
        self.codeinput.copy()

    def paste(self):
        self.codeinput.paste()

    def cut(self):
        self.codeinput.cut()


class InnerCodeInput(HoverBehavior, CodeInput):

    path = StringProperty('')
    '''Path of the current file
        :data:`path` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''
    '''

    rightclick_dropdown = ObjectProperty(None)
    ''' drop down menu that appears when the right click buttun
        is clicked
        '''

    def __init__(self, **kwargs):
        super(InnerCodeInput, self).__init__(**kwargs)
        self.rightclick_dropdown = CodeInputDropDown(self)

        self.style_name = 'native_tweak'
        self.background_normal= ''
        self.background_active= ''

    def on_codeinput_theme(self, section, key, value, *args):
        self.style_name = value

    def on_style_name(self, *args):
        super(InnerCodeInput, self).on_style_name(*args)
        self.background_color = get_color_from_hex(self.style.background_color)
        self._trigger_refresh_text()

    def on_text(self, *args):
        if self.focus:
            self.parent.saved = False


    def on_focus(self, *a):
        if self.focus:
            Window.bind(on_keyboard=self._on_keyboard)
        else:
            Window.unbind(on_keyboard=self._on_keyboard)


    def _on_keyboard(self, instance, keyboard, *args):

        # a comment
        if args[0] == 61 and args[2] == ['ctrl']:
            self.do_comment()
        
        elif args[0] == 36:      # auto indentation
            Clock.schedule_once(lambda dt: self.do_auto_indent())


    def do_comment(self):
        if not self.selection_text:     # single line momment
            line = self._lines[self.cursor_row]
            self.do_one_line_comment(line)

        else:   # multiline comment
            i = self._selection_from
            j = self._selection_to

            check_lines = list(filter(lambda line: line != '', self.selection_text.splitlines()))
            lines = self.selection_text.splitlines()

            if j > i:
                # basically checking for lines that has a value

                # move the cursor position
                self.cursor = (0, self.cursor_row- len(lines))

                # check if there are no comments in the  lines
                if len(list(filter(lambda line: line.lstrip().startswith('#'), check_lines))) != len(check_lines):
                    self.do_multiline_comment(lines)
                else:
                    self.uncomment_multiline(lines)

            else:
                self.cursor = (0, self.cursor_row)

                # check if there are no comments in the  lines
                if len(list(filter(lambda line: line.lstrip().startswith('#'), check_lines))) != len(check_lines):
                    self.do_multiline_comment(lines)
                else:
                    self.uncomment_multiline(lines)


    def do_multiline_comment(self, lines):
        closest = self.get_closest_indentation(lines)
        y_cur = self.cursor[1]
        for i, line in enumerate(lines):
            if line:
                former_cur_x = self.cursor[0]

                self.cursor = (closest, y_cur+i)

                # if line already commented
                if line.lstrip().startswith('#'): continue

                self.insert_text('# ')
                self.cursor = (former_cur_x, self.cursor[1])

        # now cancel selection
        self.cancel_selection()


    def do_multiline_indent(self):
        lines = self.selection_text.splitlines()
        closest = self.get_closest_indentation(lines)
        y_cur = self.cursor[1]
        for i, line in enumerate(lines):
            if line:
                former_cur_x = self.cursor[0]

                self.cursor = (closest, y_cur-i-1)

                self.insert_text(' '*4)
                self.cursor = (former_cur_x, self.cursor[1])

        # now cancel selection
        self.cancel_selection()

    def uncomment_multiline(self, lines):
        '''uncomment multiple line when the user from
        the user selection'''

        y_cur = self.cursor[1]
        for i, line in enumerate(lines):
            if line:
                former_cur_x = self.cursor[0]

                find = line.find('#')
                self.cursor = (find, y_cur+i)

                if line.lstrip().startswith('# '):
                    offset = 2
                    substring = '# '

                elif line.lstrip().startswith('#'):
                    offset = 1
                    substring = '#'

                new_line = line[:find] + line[find+offset:]
                self._set_line_text(self.cursor_row, new_line)

                self._set_my_undo_redo(find, offset, substring)

                self._do_my_refresh(new_line)

                self.cursor = (former_cur_x, self.cursor[1])

        # now cancel selection
        self.cancel_selection()


    def do_one_line_comment(self, line):

        if line:
            if not line.lstrip().startswith('#'):    # then comment
                strip_line = line.strip()
                former_cur_x = self.cursor[0]
                self.cursor = (line.index(strip_line), self.cursor[1])
                self.insert_text('# ')
                self.cursor = (former_cur_x, self.cursor[1])

            else:   # uncomment line
                if line.lstrip().startswith('# '):
                    offset = 2
                    substring = '# '

                elif line.lstrip().startswith('#'):
                    offset = 1
                    substring = '#'

                find = line.find('#')

                new_line = line[:find] + line[find+offset:]
                self._set_line_text(self.cursor_row, new_line)
                self._set_my_undo_redo(find, offset, substring)

                self._do_my_refresh(new_line)


    def _do_my_refresh(self, new_text):
        'the internal kivy code used to refreash the textinput'
        # refresh just the current line instead of the whole text
        start, finish, lines, lineflags, len_lines =\
            self._get_line_from_cursor(self.cursor_row, new_text)
        # avoid trigger refresh, leads to issue with
        # keys/text send rapidly through code.

        self._refresh_text_from_property('del', start, finish, lines,
                                         lineflags, len_lines)

    def _set_my_undo_redo(self, find, offset, substring):
        if self.cursor_row > 0:
            old_index = len('\n'.join(self._lines[:self.cursor_row])) + find - 1
            new_index = old_index + offset
        else:
            old_index = find
            new_index = old_index

        # handle undo and redo
        self._set_undo_redo_bkspc(
            old_index,
            new_index,
            substring, False)


    def do_auto_indent(self):
        ''' and i guess your are thinking doesn't kivy already has an auto indent,
            this func just check if the line endswith a ':' so it would indent it to the
            next line
        '''
        line = self._lines[self.cursor_row-1].strip()   # get the previos line then strip it
        if line.endswith(':'):
            self.insert_text('\t')
            

    def get_closest_indentation(self, lines):
        counter = []
        for line in lines:
            count = 0

            for char in line:
                if char != ' ':
                    counter.append(count)
                    if count == 0:  # if we found an indent at 0 then look no further
                        break
                    break
                count += 1
            else:
                if line:
                    counter.append(len(line))
        return min(counter)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        'overiding the default keyboard listener '
        # print(keycode)

        if keycode[0] == 9 and modifiers == ['shift']:      # unindentation
            self._do_reverse_indentation()

        elif keycode[0] == 9 and self.selection_text:     # multiple indentation
            self.do_multiline_indent()

        elif keycode[0] == 8 and modifiers == ['ctrl']:     # delete word left
            self.delete_word_left()

        elif keycode[0] == 27:     # on escape, do nothing
            return True
        else:
            return super(CodeInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def _do_reverse_indentation(self):
        if not self.selection_text and self._lines[self.cursor_row]:

            line = self._lines[self.cursor_row].replace('\t', '    ')
            indent = self.get_closest_indentation([line])

            if indent != 0:
                next_indent = indent - 4
                new_line = line[:next_indent] + line[indent:]

                self._set_line_text(self.cursor_row, new_line)

                self._set_my_undo_redo(next_indent-2, 4, '    ')

                self._do_my_refresh(new_line)
                self.cursor = (next_indent, self.cursor_row)

        if self.selection_text:
            i = self._selection_from
            j = self._selection_to

            lines = self.selection_text.splitlines()

            if j > i:
                self.cursor = (0, self.cursor_row- len(lines))
            else:
                self.cursor = (0, self.cursor_row)

            self._multi_unindent(lines)

            # now cancel selection for the main time
            self.cancel_selection()
        
    def _multi_unindent(self, lines):
        y_cur = self.cursor[1]
        for i, line in enumerate(lines):
            if line:
                former_cur_x = self.cursor[0]

                self.cursor = (0, y_cur+i)

                line = line.replace('\t', '    ')

                indent = self.get_closest_indentation([line])

                if indent != 0:
                    next_indent = indent - 4
                    new_line = line[:next_indent] + line[indent:]

                    self._set_line_text(self.cursor_row, new_line)

                    self._set_my_undo_redo(next_indent-2, 4, '    ')

                    self._do_my_refresh(new_line)

                    self.cursor = (next_indent, self.cursor_row)

    def delete_word_left(self):
        '''
        Delete text left of the cursor to the beginning of word'''

        if self._selection:
            return None

        line = self._lines[self.cursor[1]]
        if self.cursor[0]==0 and line=='':
            return None


        former_cursor_x = self.cursor[0]
        old_index = self.cursor_index()

        self.do_cursor_movement('cursor_left', control=True)
        new_index = self.cursor_index()
        end_cursor = self.cursor

        if self.cursor[0] != former_cursor_x:
            new_line = line[:self.cursor[0]] + line[former_cursor_x:]
            self._set_line_text(self.cursor_row, new_line)

            substring = line[self.cursor[0]:former_cursor_x]

            self._set_undo_redo_bkspc(
                old_index,
                new_index,
                substring, False)

            self._do_my_refresh(new_line)
            self._set_cursor(pos=end_cursor)


    def _split_smart(self, text):
        ''' turns out this function isn't really smart
        so had to override it, basically for horizontal line continuation'''
        lines = text.split(u'\n')
        lines_flags = [0] + [0x01] * (len(lines) - 1)
        return lines, lines_flags

    def on_hover(self, *a):
        if self.hover:
            Window.set_system_cursor('ibeam')
        else:
            Window.set_system_cursor('arrow')

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.rightclick_dropdown.open()
                FocusBehavior.ignored_touch.append(touch)
                return True

        if touch.button == 'left':
            return super(InnerCodeInput,self).on_touch_down(touch)


from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

import os

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

    code_background = ListProperty([0,0,0,1])

    code_input = ObjectProperty(None)

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
            checked_list = list(filter(lambda chd: chd != child, ToggleButtonBehavior.get_widgets(child.group)))
            map(lambda child: setattr(child, 'state', 'normal'), checked_list)



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
