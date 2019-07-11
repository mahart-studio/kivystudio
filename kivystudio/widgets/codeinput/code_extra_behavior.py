
class CodeExtraBehavior(object):

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
        if self.cursor[0]==0:
            return None

        if line.strip()=='':
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
