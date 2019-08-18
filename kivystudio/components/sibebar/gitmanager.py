from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<GitManager>:
    size_hint_x: None
    width: '160dp'
    canvas.before:
        Color:
            rgba: .1,.1,.1,1
        Rectangle:
            size: self.size
    Label:
        text: 'Git'
''')


class GitManager(Screen):
    pass
