from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<GeneralSearch>:
    size_hint_x: None
    width: '160dp'
    Label:
        text: 'Search....'
''')

class GeneralSearch(Screen):
    pass

