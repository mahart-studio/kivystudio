from kivy.logger import Logger
import sys
from kivystudio.widgets.filemanager import filemanager


def open_new_file():
    ''' open a new file on
        the CodeInput '''
    from kivystudio.assembler import code_place
    code_place.add_code_tab(tab_type='new_file')

def open_file():    
    ''' open a file (existing file) on
        the CodeInput '''
    from kivystudio.assembler import add_new_tab
    filemanager.open_file(path='/root',on_selection=add_new_tab)

def open_folder():
    ''' open a folder '''
    from kivystudio.assembler import add_new_tab
    filemanager.open_folder(path='/root',on_selection=None)

def open_recent():
    pass

def save():
    ''' save the current opened
        file '''
    from kivystudio.assembler import code_place
    code_place.code_manager.save_current_tab()

def save_all():
    ''' save all file currently opened '''
    from kivystudio.assembler import code_place
    code_place.code_manager.save_all_tabs()

def save_as():
    pass

def exit_window():
    exit()

import string
def is_binary(filename):
    ''' checks if a file is a binary file or not 
        used to validate file before opening them in
        the studio '''
    s = open(filename, 'rb').read(512)
    def func(num):
        return bytes(chr(num).encode('utf-8'))

    text_char = b''.join( list(map(func, range(32,127))) ) #+ list('\n\r\t\b') )
    if sys.version_info[0] == 3:
        _null_trans = b''.maketrans(b"",b"")
    else:
        _null_trans = string.maketrans('', '')

    if not s: # empty files are considered text files
        return False
    
    if b'\0' in s:
        # file with null bytes are likely binary
        return True

    t = s.translate(_null_trans, delete=text_char)
    # if more than 30% are non-text charaters 
    # then it is considered binary
    if float(len(t))/float(len(s)) > 0.30:
        return True
    return False
