from kivystudio.widgets.iconlabel import IconLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from os.path import join, dirname
Builder.load_file(join(dirname(__file__), 'welcome.kv'))

class WelcomeTab(BoxLayout):
    pass
