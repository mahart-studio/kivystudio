from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.base import runTouchApp as app
from kivy.lang import Builder

class Root(FloatLayout):

    text='Hello '
    def on_touch_down(self, touch):
        self.info = InfoLabel(text='Hello ')
        self.text += 'Hello ctrl l'
        self.info.text += self.text
        self.add_widget(self.info)

    def on_touch_up(self, touch):
        self.remove_widget(self.info)

class InfoLabel(Label):
    pass




Builder.load_string('''
<InfoLabel>:
    pos_hint: {'center_y': .5, 'center_x': .5}
    size_hint: None,None
    text_size: self.width, None
    valign: 'middle'
    halign:'left' 
    width:  '200dp'
    height: self.texture_size[1]+10
    color: 1,1,1,1
    padding: '4dp', '4dp'

    canvas.before:
        Color:
            rgba: 0,0,0,1
        RoundedRectangle:
            size: self.size
            pos: self.pos
<Root>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size


''')
app(Root())
