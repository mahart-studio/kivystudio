from kivy.lang import Builder
from kivy.base import runTouchApp as app
from __init__ import *

app(
Builder.load_string('''

BoxLayout:
    Carousel:
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                size: self.size
                pos: self.pos
        FloatLayout:
            IpadScreen:
                on_scale: self.center=root.center
                center: root.center
                id: screen
                Button:
                    text: 'Hello'
                    font_size: '17dp'

            BoxLayout:
                pos_hint: {'y': .01, 'center_x': .5}
                size_hint: None,None
                size: '120dp', '60dp'
                Button:
                    text: '-'
                    bold: True
                    on_release:
                        if not(screen.scale < -100.0) : screen.scale -= 0.05
                Button:
                    text: '+'
                    bold: True
                    on_release:
                    if not(screen.scale > 4.0): screen.scale += 0.05

# Carousel:
#     AndroidPhoneScreen:
#         Button:
#             text: 'Hello'
#     IphoneScreen:
#         Button:
#             text: 'Hello'
#     IpadScreen:
#         Button:
#             text: 'Hello'
#     AndriodTabScreen:
#         Button:
#             text: 'Hello'

''')
)
