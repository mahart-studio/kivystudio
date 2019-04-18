
''' A quick implementation of mouse hovering 
    just fires one event called 'on_hover'
    when the mouse hover on a widget the inhenrites from this
    behavior
    Ex:
    class HoverButton(HoverBehavior, Button):

        def on_hover(self, *args):
            if self.hover:
                self.text = 'Yeah!!'
            else:
                self.text =''
'''

from kivy.core.window import Window
from kivy.properties import ObjectProperty

class HoverBehavior(object):

    hover = ObjectProperty(False)
    ''' indicate is mouse if over the widget
    defaults to False'''


    def on_parent(self, *args):
        if self.parent:
            Window.bind(mouse_pos=self.on_mouse_move)
        else:
            Window.unbind(mouse_pos=self.on_mouse_move)


    def on_mouse_move(self, win, pos):

        if self.collide_point(*pos):
            self.hover = True
        else:
            self.hover = False


if __name__ == "__main__":
    from kivy.base import runTouchApp as app
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout

    class HoverButton(HoverBehavior, Button):

        def on_hover(self, *args):
            if self.is_hover:
                self.text = 'Yeah!!'
            else:
                self.text =''
    box=BoxLayout()
    box.add_widget(HoverButton())
    box.add_widget(Button(text='Hello'))
    app(box)