import re

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
