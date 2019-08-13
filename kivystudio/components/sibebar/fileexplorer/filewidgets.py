from kivy.uix.treeview import TreeViewNode
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, BooleanProperty

from kivystudio.tools.iconfonts import icon
from kivystudio.behaviors import HoverBehavior

import os

class TreeViewFile(HoverBehavior, TreeViewNode, BoxLayout):

    hover_color = ListProperty([.15,.15,.15,0])
    ' default color when the mouse hovers over the widget'

    path = StringProperty('')
    ' path to the file or directory '

    display_name = StringProperty('')
    ' name displayed for the file or directory '

    display_icon = StringProperty('')
    ''' icon displayed on the right side of the file
    or directory '''

    def __init__(self, **k):
        super(TreeViewFile, self).__init__(**k)

    def on_hover(self, *a):
        if self.hover:
            self.hover_color = (.14,.14,.14,.8)
        else:
            self.hover_color = (.15,.15,.15,0)

    def on_path(self, *a):
        if os.path.isdir(self.path):
            self.display_icon = icon('fa-caret-right',16)
        elif os.path.isfile(self.path):
            self.display_icon = icon('fa-file-code-o', 16)

        self.display_name = os.path.split(self.path)[1]



Builder.load_string('''
#: import icon kivystudio.tools.iconfonts.icon

<TreeViewFile>:
    size_hint_y: None
    height: '24dp'
    canvas.before:
        Clear
        Color:
            rgba: self.hover_color
        Rectangle:
            size: self.size
            pos: self.pos
    canvas.after:
        Clear
    IconLabel:
        size_hint_x: None
        width: '24dp'
        text: root.display_icon
        color: .2,.5,1,1
    Label:
        text: root.display_name
''')
