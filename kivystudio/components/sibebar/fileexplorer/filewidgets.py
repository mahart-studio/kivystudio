from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, BooleanProperty

from kivystudio.tools.iconfonts import icon
from kivystudio.behaviors import HoverBehavior

import os

class FileWidgetBase(HoverBehavior, BoxLayout):

    hover_color = ListProperty([.15,.15,.15,0])

    file_path = StringProperty('')

    display_name = StringProperty('')

    def __init__(self, **k):
        super(FileWidgetBase, self).__init__(**k)

    def on_hover(self, *a):
        if self.hover:
            self.hover_color = (.14,.14,.14,.8)
        else: 
            self.hover_color = (.15,.15,.15,0)

    def on_file_path(self, *a):
        self.display_name = os.path.split(self.file_path)[1]


class FileWidget(FileWidgetBase):

    file_icon = StringProperty(icon('fa-code', 16))

class DirWidget(FileWidgetBase):

    is_open = BooleanProperty(False)


Builder.load_string('''
#: import icon kivystudio.tools.iconfonts.icon

<FileWidgetBase>:
    size_hint_y: None
    height: '24dp'
    canvas.before:
        Color:
            rgba: self.hover_color
        Rectangle:
            size: self.size
            pos: self.pos

<FileWidget>:
    IconLabel:
        size_hint_x: None
        width: '48dp'
        text: root.file_icon
        color: .2,.5,1,1
    Label:
        text: root.display_name

<DirWidget>:
    IconLabel:
        size_hint_x: None
        width: '32dp'
        text: icon('fa-caret-right', 16)
    Label:
        text: root.display_name
''')
