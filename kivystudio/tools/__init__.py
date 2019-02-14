from kivy.core.window import Window

def set_auto_mouse_position(widget):
    ''' functions trys to position widget
    automaticaly on the mouse pos'''

    if Window.mouse_pos[0]+widget.width > Window.width:
        widget.right = Window.mouse_pos[0]

    else:
        widget.x = Window.mouse_pos[0]
    
    if (Window.mouse_pos[1]+widget.height > Window.height):
        widget.top = Window.mouse_pos[1]
    else:
        widget.top = Window.mouse_pos[1]
