from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from .filewidgets import TreeViewFile
import os
from os.path import join, split, dirname

class FileView(TreeView):
    def on_touch_down(self, touch):
        node = self.get_node_at_pos(touch.pos)
        if not node:
            return
        if node.disabled:
            return
        # toggle node or selection ?
        self.toggle_node(node)
        self.select_node(node)
        # node.dispatch('on_touch_down', touch)
        return True



class FileExplorer(Screen):
    tree_view = ObjectProperty(None)

    def __init__(self, **k):
        super(FileExplorer, self).__init__(**k)
        # self.load_directory('widgets')  #test

    def load_directory(self, directory):
        '''
        load a directory all it files and subdirectory
        on the the tree view '''
        tree_view = self.tree_view
        for node in tree_view.iterate_all_nodes(node=None):
            tree_view.remove_node(node)
        dir_nodes = {}
        for dirpath, dirnames, filenames in os.walk(directory):
            try:
                top= dir_nodes[dirname(dirpath)]
            except KeyError:
                top=None

            parent = tree_view.add_node(TreeViewLabel(text=split(dirpath)[1]), top)
            dir_nodes[dirpath] = parent

            for file in filenames:
                tree_view.add_node(TreeViewFile(text=file,path=join(dirpath,file)),
                        parent)


Builder.load_string('''
<TreeViewLabel>:
    width: self.texture_size[0]
    shorten_from: 'right'
    shorten: True
    height: dp(24)
    text_size: self.width, None

<FileExplorer>:
    tree_view: tree_view
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
            id: tree_scroll
            bar_width: 10
            scroll_type: ['bars', 'content']
            FileView:
                id: tree_view
                indent_level: '12dp'
                indent_start: '16dp'
                size_hint: 1, None
                height: max(tree_scroll.height, self.minimum_height)

''')
