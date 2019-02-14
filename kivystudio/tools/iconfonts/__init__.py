"""
Kivy-iconfonts
==============

Simple helper functions to make easier to use icon fonts in Labels and derived
widgets.
"""
from .iconfonts import *


if __name__ == '__main__':
    from kivy.lang import Builder
    from kivy.base import runTouchApp
    from kivy.animation import Animation
    from os.path import join, dirname

    kv = """
#: import icon iconfonts.icon
BoxLayout:
    Button:
        markup: True
        text: "%s"%(icon('icon-comment', 32))
    Button:
        markup: True
        text: "%s"%(icon('icon-emo-happy', 64))

    Button:
        markup: True
        text: "%s Text"%(icon('icon-plus-circled', 24))

    Button:
        markup: True
        text: "%s"%(icon('icon-doc-text-inv', 64, 'ff3333'))

    Label:
        id: _anim
        markup: True
        text: "%s"%(icon('icon-spin6', 32))
        font_color: 1, 0, 0, 1
        p: 0
        canvas:
            Clear
            PushMatrix
            Rotate:
                angle: -self.p
                origin: self.center_x , self.center_y
            Rectangle:
                size: (32, 32)
                pos: self.center_x - 16, self.center_y - 16
                texture: self.texture
            PopMatrix
    """

    register('default_font', 'iconfont_sample.ttf',
             join(dirname(__file__), 'iconfont_sample.fontd'))

    root = Builder.load_string(kv)
    an = Animation(p=360, duration=2) + Animation(p=0, duration=0)
    an.repeat = True
    an.start(root.ids['_anim'])
    runTouchApp(root)
