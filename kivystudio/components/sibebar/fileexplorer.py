from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<FileExplorer>:
    size_hint_x: None
    width: '160dp'
    Label:
        text: 'File Explorer'
''')
 

class FileExplorer(Screen):
    pass
