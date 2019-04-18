import os

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder 
from kivy.base import runTouchApp as app
from kivy.properties import ObjectProperty
from kivy.uix.scatter import Scatter

# module resources
from kivy.resources import resource_add_path
resource_add_path(os.path.dirname(os.path.realpath(__file__)))

__all__ = ('IphoneScreen', 'IpadScreen', 'AndroidPhoneScreen', 'AndriodTabScreen', )

class ScreenScatter(Scatter):
	
    container = ObjectProperty(None)

    def add_widget(self, widget):
        if len(self.children) > 0:
            self.container.add_widget(widget)
        else:
            super(ScreenScatter, self).add_widget(widget)

    def clear_widgets(self):
        self.container.clear_widgets()


class ScreenContainer(RelativeLayout):
    pass


class IphoneScreen(ScreenScatter):
    pass

class IpadScreen(ScreenScatter):
    pass

class AndriodTabScreen(ScreenScatter):
    pass

class AndroidPhoneScreen(ScreenScatter):
    pass

build = Builder.load_string('''
#: import Window kivy.core.window.Window

BoxLayout:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                size: self.size
                pos: self.pos
        AndroidPhoneScreen:
            id: screen
            Button:
                text: 'Hello'
                font_size: '17dp'

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

        BoxLayout:
            pos_hint: {'y': .01, 'center_x': .5}
            size_hint: None,None
            size: '120dp', '60dp'
            Button:
                text: '-'
                bold: True
                on_release:
                    if not screen.scale < -100.0: screen.scale -= 0.05
            Button:
                text: '+'
                bold: True
                on_release: screen.scale += 0.05





# 398 804
<AndroidPhoneScreen>:
    size: container.size
    container: container
    scale: 0.75
    ScreenContainer:
        id: container
        # size: ('230dp', '420dp')
        size: '320dp', '610dp'
        size_hint: None, None
        pos_hint: {'center_y': .5, 'center_x': .5}
        canvas.before:
            BorderImage:
                source: 'images/android_lolipop1.png'
                # border: (0, 0,0,0)
                size:(root.width + dp(33), root.height + dp(152))
                pos: (-dp(16), -dp(85.5))

# 380 743
<IphoneScreen>:
    size: container.size
    container: container
    ScreenContainer:
        id: container
        size: ('220dp', '390dp')
        size_hint: None, None
        pos_hint: {'center_y': .5, 'center_x': .5}
        canvas.before:
            BorderImage:
                source: 'iphone.png'
                size:(root.width + dp(42), root.height + dp(210))
                pos: (-dp(21), -dp(105))

#1271 992
<IpadScreen>:
    size: container.size
    container: container
    ScreenContainer:
        id: container
        size: ('500dp', '320dp')
        size_hint: None, None
        pos_hint: {'center_y': .5, 'center_x': .5}
        canvas.before:
            BorderImage:
                source: 'ipad.png'
                size:(root.width + dp(118), root.height + dp(102))
                pos: (-dp(59), -dp(51))

# 953 612
<AndriodTabScreen>:
    size: container.size
    container: container
    ScreenContainer:
        id: container
        size: ('500dp', '280dp')
        size_hint: None, None
        pos_hint: {'center_y': .5, 'center_x': .5}
        canvas.before:
            BorderImage:
                source: 'android_tab.png'
                size:(root.width + dp(70), root.height + dp(102))
                pos: (-dp(35), -dp(51))

<ScreenScatter>:
    do_rotation: False
    do_scale: False
    do_translation: False
    # scale_min: 1
    size_hint: None, None
    auto_bring_to_front: False


''')



if __name__ == "__main__":
    app(build)
