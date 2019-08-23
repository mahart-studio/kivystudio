from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from kivy.lang import Builder

from .problem_space import ProblemSpace

class TerminalSpace(BoxLayout):

    manager = ObjectProperty(None)
    ''' Instance of screen manager used '''

    tab_container = ObjectProperty(None)
    ''' instance of a gridlayout where tha tab lays'''

    def __init__(self, **k):
        super(TerminalSpace, self).__init__(**k)
        self.add_widget(ProblemSpace(), title='PROBLEMS')

    def add_widget(self, widget, title=''):
        if len(self.children) > 1:
            tab = TerminalTab()
            tab.text=title
            tab.bind(state=self.tab_state)
            self.tab_container.add_widget(tab)
            screen = Screen(name=title)
            screen.add_widget(widget)
            self.manager.add_widget(screen)
        else:
            super(TerminalSpace, self).add_widget(widget)

    def tab_state(self, tab, state):
        if state=='down':
            manager.current = tab.text 

class TerminalTab(ToggleButtonBehavior, Label):

    def on_state(self, *a):
        if self.state=='down':
            self.text = "[u]" + self.text + "[/u]"
            self.color = (1,1,1,1)
        else:
            self.text = self.text.replace('[u]','').replace('[/u]','')
            self.color = (.5,.5,.5,1)

Builder.load_string('''
<TerminalSpace>:
    tab_container: tab_container
    manager: manager
    orientation: 'vertical'

    ScrollView:
        size_hint_y: None
        height: '28dp'
        GridLayout:
            id: tab_container
            rows: 1
            size_hint_x: None
            width: self.minimum_width

    ScreenManager:
        id: manager

<TerminalTab>:
    allow_no_selection: False
    size_hint_x: None
    width: '180dp'

''')