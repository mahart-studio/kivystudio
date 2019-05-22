from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder

from kivystudio.tools import set_auto_mouse_position

class RightClickDrop(BoxLayout):

    def __init__(self, **kwargs):
        super(RightClickDrop, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # touch should not unfocus input
            pass
        else:
            self.dismiss()

        return super(RightClickDrop,self).on_touch_down(touch)

    def on_parent(self, *a):
        if self.parent:
            Window.bind(on_keyboard=self._on_keyboard)
        else:
            Window.unbind(on_keyboard=self._on_keyboard)

    def _on_keyboard(self, instance, keycode, *args):

        print(keycode)
        if keycode[0] == 27:     # on escape
            self.dismiss()
            return True

    def open(self):
        if self not in Window.children:
            set_auto_mouse_position(self)
            Window.add_widget(self)

    def dismiss(self):
        if self in Window.children:
            Window.remove_widget(self)



Builder.load_string('''
<RightClickDrop>:
    orientation: 'vertical'
    size: '260dp',self.minimum_height
    size_hint: None,None
    canvas.before:
        BorderImage:
            source: 'shadow32.png'
            border: (26, 26, 26, 26)
            size:(root.width + 50, root.height + 50)
            pos: (root.x-25, root.y-25)
''')
