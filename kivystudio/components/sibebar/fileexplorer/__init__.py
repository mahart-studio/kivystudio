from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

import os
from os.path import join

from .filewidgets import *

Builder.load_string('''
<FileExplorer>:
    canvas.before:
        Color:
            rgba: .1,.1,.1,1
        Rectangle:
            size: self.size
    size_hint_x: None
    width: '160dp'
    GridLayout:
        cols: 1
        Label:
            text: 'Explorer!'
            font_size: '16dp'
            size_hint_y: None
            height: '32dp'
        ScrollView:
            GridLayout:
                id: grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height

''')
 

class FileExplorer(Screen):
    
    def __init__(self, **k):
        super(FileExplorer, self).__init__(**k)
        direct = '.'
        for node in os.listdir(direct):
            dr = join(direct, node)
            if os.path.isfile(dr):
                self.ids.grid.add_widget(FileWidget(file_path=dr))
            elif os.path.isdir(join(dr)):
                self.ids.grid.add_widget(DirWidget(file_path=dr))
