from kivystudio.widgets.filemanager import filemanager
def open_new_file():
    from kivystudio.assembler import code_place
    code_place.add_code_tab(tab_type='new_file')

def open_file():
    from kivystudio.assembler import add_new_tab
    filemanager.open_file(path='/root',callback=add_new_tab)

def open_folder():
    from kivystudio.assembler import add_new_tab
    filemanager.open_folder(path='/root',callback=None)

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
