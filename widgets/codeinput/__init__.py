from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '700')


import re

from kivy import Config
from kivy.properties import BooleanProperty, StringProperty, ListProperty, ObjectProperty
from kivy.utils import get_color_from_hex
from pygments import styles

from .codeinput import CodeInput


class InnerCodeInput(CodeInput):
    '''A subclass of CodeInput to be used for KivyDesigner.
       It has copy, cut and paste functions, which otherwise are accessible
       only using Keyboard.
       It emits on_show_edit event whenever clicked, this is catched
       to show EditContView;
    '''

    __events__ = ('on_show_edit',)

    error = BooleanProperty(False)
    '''Indicates if the current file contains any type of error
        :data:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False
    '''

    path = StringProperty('')
    '''Path of the current file
        :data:`path` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''
    '''

    clicked = BooleanProperty(False)
    '''If clicked is True, then it confirms that this widget has been clicked.
       The one checking this property, should set it to False.
       :data:`clicked` is a :class:`~kivy.properties.BooleanProperty`
    '''

            
    def __init__(self, **kwargs):
        super(InnerCodeInput, self).__init__(**kwargs)
        parser = Config.get_configparser('DesignerSettings')
        self.style_name = 'native'

        # if parser:
            # parser.add_callback(self.on_codeinput_theme,
                                # 'global', 'code_input_theme')
            # self.style_name = parser.getdefault('global', 'code_input_theme',
                                                # 'emacs')

    def on_codeinput_theme(self, section, key, value, *args):
        # if not value in styles.get_all_styles():
        #     pass
        #     # show_alert("Error", "This theme is not available")
        # else:
        self.style_name = value

    def on_style_name(self, *args):
        super(InnerCodeInput, self).on_style_name(*args)
        self.background_color = get_color_from_hex(self.style.background_color)
        self._trigger_refresh_text()
        
    def on_show_edit(self, *args):
        pass

    def on_touch_down(self, touch):
        '''Override of CodeInput's on_touch_down event.
           Used to emit on_show_edit
        '''
        if self.collide_point(*touch.pos):
            self.clicked = True
            self.dispatch('on_show_edit')

        return super(InnerCodeInput, self).on_touch_down(touch)

    def do_focus(self, *args):
        '''Force the focus on this widget
        '''
        self.focus = True

    def do_select_all(self, *args):
        '''Function to select all text
        '''
        self.select_all()


    def find_next(self, search, use_regex=False, case=False):
        '''Find the next occurrence of the string according to the cursor
        position
        '''
        text = self.text
        if not case:
            text = text.upper()
            search = search.upper()
        lines = text.splitlines()

        col = self.cursor_col
        row = self.cursor_row

        found = -1
        size = 0  # size of string before selection
        line = None
        search_size = len(search)

        for i, line in enumerate(lines):
            if i >= row:
                if use_regex:
                    if i == row:
                        line_find = line[col + 1:]
                    else:
                        line_find = line[:]
                    found = re.search(search, line_find)
                    if found:
                        search_size = len(found.group(0))
                        found = found.start()
                    else:
                        found = -1
                else:
                    # if on current line, consider col
                    if i == row:
                        found = line.find(search, col + 1)
                    else:
                        found = line.find(search)
                # has found the string. found variable indicates the initial po
                if found != -1:
                    self.cursor = (found, i)
                    break
            size += len(line)

        if found != -1:
            pos = text.find(line) + found
            self.select_text(pos, pos + search_size)

    def find_prev(self, search, use_regex=False, case=False):
        '''Find the previous occurrence of the string according to the cursor
        position
        '''
        text = self.text
        if not case:
            text = text.upper()
            search = search.upper()
        lines = text.splitlines()

        col = self.cursor_col
        row = self.cursor_row
        lines = lines[:row + 1]
        lines.reverse()
        line_number = len(lines)

        found = -1
        line = None
        search_size = len(search)

        for i, line in enumerate(lines):
            i = line_number - i - 1
            if use_regex:
                if i == row:
                    line_find = line[:col]
                else:
                    line_find = line[:]
                found = re.search(search, line_find)
                if found:
                    search_size = len(found.group(0))
                    found = found.start()
                else:
                    found = -1
            else:
                # if on current line, consider col
                if i == row:
                    found = line[:col].find(search)
                else:
                    found = line.find(search)
            # has found the string. found variable indicates the initial po
            if found != -1:
                self.cursor = (found, i)
                break

        if found != -1:
            pos = text.find(line) + found
            self.select_text(pos, pos + search_size)

    def on_text(self, *args):
        '''Listen text changes
        '''
        if self.focus:
            self.parent.saved = False


    def on_focus(self, *a):
        '''
        if not self.focus:
            style_list = list(styles.get_all_styles())
            try:
                self.style_name = style_list[style_list.index(self.style_name)+1]
            except IndexError:
                self.style_name = style_list[0]
            print(self.style_name)
        '''
        if self.focus:
            Window.bind(on_keyboard=self._on_keyboard)
        else:
            Window.unbind(on_keyboard=self._on_keyboard)


    def _on_keyboard(self, instance, keyboard, *args):

        # a comment
        if args[0] == 61 and args[2] == ['ctrl']:     # comment
            self.do_comment()
        
        elif args[0] == 36:      # 
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

        elif keycode[0] == 115 and modifiers == ['ctrl']:
            # with open('CodeInputer/kivy_text.kv', 'w') as f:
            #     f.write(self.text)

            return super(CodeInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

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
            return

        line = self._lines[self.cursor[1]]
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


from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

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

        # with open('FilePicker/main.kv', 'r') as f:
        #     self.ids.code_input.text = f.read()

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

    normal_color = ListProperty([.6,.6,.6,1])
    ' color of the number when selected'
    
    def on_state(self, *args):

        if self.state == 'down':
            self.color = self.selected_color
        else:
            self.color = self.normal_color



build = Builder.load_string('''
#: import KivyLexer kivy.extras.highlight.KivyLexer
#: import Python3Lexer pygments.lexers.python.PythonLexer
<FullCodeInput>:
    cols: 3
    code_input: code_input
    NumberingGrid:
        id: number_scroll
        size_hint_x: None
        width: '50dp'
        bar_color: 1,0,0,0
        bar_inactive_color: self.bar_color
        scroll_type: ['bars']
        bar_width: 0
        canvas.before:
            Color:
                rgba: (0.12549019607843137, 0.12549019607843137, 0.12549019607843137, 1)
            Rectangle:
                size: self.size
                pos: self.pos

        GridLayout:
            cols: 1
            id: numbering
            size_hint_y: None
            height: self.minimum_height
            padding: [0, '6dp', 0, '6dp']

    InnerCodeInput:
        id: code_input
        auto_indent: True
        size_hint_y: 1
        height: scroll.height
        cursor_color: 1,1,1,1
        on_cursor_row: root.change_scroll_y(code_input, scroll)
        _line_lenght: len(self._lines)
        on__line_lenght: root.number_me(self, scroll)
        selection_color: .8,.8,.8,.4
        # lexer: KivyLexer()
        # lexer: Python3Lexer()
        font_size: '13dp'
        line_highlight_color: 1,1,.8,.1
        on_selection_text:
            if self.selection_text: self.line_highlight_color = 0,0,0,0
            else: self.line_highlight_color = 1,1,.8,.1 
        on_focus:
            if not self.focus: self.line_highlight_color = 0,0,0,0
            else: self.line_highlight_color = 1,1,.8,.1 

        # canvas to show highlighted line
        canvas.after:
            Color:
                rgba: self.line_highlight_color
            Rectangle:
                size: self.width, self.line_height + dp(3)
                pos: self.x, self.cursor_pos[1] -  self.line_height -dp(1.5)


    ScrollingBar:
        bar_width: '12dp'
        scroll_type: ['bars', 'content']
        bar_color: 1,1,1,.5
        bar_inactive_color: self.bar_color
        id: scroll
        kv_lang_area: code_input
        size_hint_x: None
        width: '12dp'
        on_scroll_start: root._do_cursor_scroll==False
        on_scroll_move: root.do_bar_scroll(code_input, self)
        on_scroll_stop: root._do_cursor_scroll==True

        canvas.before:
            Color:
                rgba: code_input.background_color
            Rectangle:
                size: self.size
                pos: self.pos

        Widget:
            size_hint_y: None
            height: code_input.minimum_height


<Numbers_>:
    font_size: '13dp'
    size_hint_y: None
    color: self.normal_color
    group: '_line_numbers_'
    allow_no_selection: False
''')



if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(FullCodeInput())


'rrt, xcode, friendly, algol'
