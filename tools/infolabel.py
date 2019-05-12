from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window

from __init__ import set_auto_mouse_position

def show_info_on_mouse(message=''):
    if message:
        if info_label in Window.children:
            Window.remove_widget(info_label)

        info_label.text = ''
        info_label.text = message
        set_auto_mouse_position(info_label)
        Window.add_widget(info_label)


def remove_info_on_mouse():
    if info_label in Window.children:
        Window.remove_widget(info_label)



class InfoLabel(Label):
    pass


Builder.load_string('''
<InfoLabel>:
    size_hint: None,None
    text_size: None, self.height
    valign: 'middle'
    halign:'left'
    width:  self.texture_size[0]+10
    height: '30dp'
    color: 1,1,1,1
    padding: '4dp', '4dp'
    canvas.before:
        Color:
            rgba: 0,0,0,.9
        RoundedRectangle:
            size: self.size
            pos: self.pos
''')
info_label = InfoLabel()