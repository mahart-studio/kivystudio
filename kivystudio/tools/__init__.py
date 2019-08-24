import os
from kivy.lang import Builder
from kivy.core.window import Window

def set_auto_mouse_position(widget):
    ''' functions trys to position widget
    automaticaly on the mouse pos'''

    if Window.mouse_pos[0]+widget.width > Window.width:
        widget.x = Window.mouse_pos[0]

    else:
        widget.x = Window.mouse_pos[0]
    
    if (Window.mouse_pos[1]+widget.height > Window.height):
        widget.top = Window.mouse_pos[1]-16
    else:
        widget.top = Window.mouse_pos[1]-16

def load_kv(filepath, file):
	''' load a kivy file from the current
		directory of the file calling this func
		where filepath is __file__ and file is a kv file''' 
	filepath = os.path.dirname(filepath)
	Builder.load_file(os.path.join(filepath, file))
    