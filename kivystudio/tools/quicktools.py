from kivy.logger import Logger
import sys
from kivystudio.widgets.filemanager import filemanager


def open_new_file():
    from kivystudio.assembler import code_place
    code_place.add_code_tab(tab_type='new_file')

def open_file():
    from kivystudio.assembler import add_new_tab
    filemanager.open_file(path='/root',on_selection=add_new_tab)

def open_folder():
    from kivystudio.assembler import add_new_tab
    filemanager.open_folder(path='/root',on_selection=None)

def open_recent():
    pass

def save():
    from kivystudio.assembler import code_place
    code_place.code_manager.save_current_tab()

def save_all():
    from kivystudio.assembler import code_place
    code_place.code_manager.save_all_tabs()

def save_as():
    pass

def exit_window():
    exit()

import string
def is_binary(filename):
    s = open(filename).read(512)
    text_char = ''.join( list(map(chr, range(32,127))) + list('\n\r\t\b') )
    if sys.version_info[0] == 3:
        _null_trans = str.maketrans("","")
    else:
        _null_trans = string.maketrans('', '')

    if not s: # empty files are considered text files
        return False
    
    if '\0' in s:
        # file with null bytes are likely binary
        return True

    # t = s.translate(_null_trans, text_char)
    # text = s.translate(str.maketrans('', '', string.punctuation))
    t = s.translate(str.maketrans('', '', text_char))
    # if more than 30% are non-text charaters 
    # then it is considered binary
    if float(len(t))/float(len(s)) > 0.30:
        return True
    return False
