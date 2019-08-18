from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

from kivystudio.widgets.searchinput import SearchInput

class CodeInputFind(BoxLayout):
    '''Widget responsible for searches in Code Input
    '''

    query = StringProperty('')
    '''Search query
    :data:`query` is a :class:`~kivy.properties.StringProperty`
    '''

    txt_query = ObjectProperty(None)
    '''Search query TextInput
    :data:`txt_query` is a :class:`~kivy.properties.ObjectProperty`
    '''

    use_regex = BooleanProperty(False)
    '''Filter search with regex
        :data:`use_regex` is a :class:`~kivy.properties.BooleanProperty`
    '''

    case_sensitive = BooleanProperty(False)
    '''Filter search with case sensitive text
        :data:`case_sensitive` is a :class:`~kivy.properties.BooleanProperty`
    '''

    code_input = ObjectProperty(None)

    def on_touch_down(self, touch):
        '''Enable touche
        '''
        if self.collide_point(*touch.pos):
            super(CodeInputFind, self).on_touch_down(touch)
            return True

    def find_next(self, search):
        '''Find the next occurrence of the string according to the cursor
        position
        '''
        code_input = self.code_input
        use_regex = self.use_regex
        case = self.case_sensitive

        text = code_input.text
        if not case:
            text = text.upper()
            search = search.upper()
        lines = text.splitlines()

        col = code_input.cursor_col
        row = code_input.cursor_row

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
                    code_input.cursor = (found, i)
                    break
            size += len(line)

        if found != -1:
            pos = text.find(line) + found
            code_input.select_text(pos, pos + search_size)
            return True
        else:
            return False

    def find_prev(self, search):
        '''Find the previous occurrence of the string according to the cursor
        position
        '''
        code_input = self.code_input
        use_regex = self.use_regex
        case = self.case_sensitive

        code_input = self.code_input
        text = code_input.text
        if not case:
            text = text.upper()
            search = search.upper()
        lines = text.splitlines()

        col = code_input.cursor_col
        row = code_input.cursor_row
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
                code_input.cursor = (found, i)
                break

        if found != -1:
            pos = text.find(line) + found
            code_input.select_text(pos, pos + search_size)
            return True
        else:
            return False
    
    def find(self,search):
        if not self.find_next(search):
            self.find_prev(search)
        Clock.schedule_once(lambda *args: setattr(self.ids.input, 'focus', True))

    def open(self,code_input):
        self.code_input=code_input
        self.ids.input.focus=True
        if not self.parent:
            Window.add_widget(self)
            self.top = code_input.top
            self.right= code_input.right
            code_input.bind(top=self.setter('top'))
            code_input.bind(right=self.setter('right'))

    def dismiss(self):
        if self.parent:
            self.parent.remove_widget(self)
