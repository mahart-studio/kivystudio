from kivy.uix.splitter import Splitter, SplitterStrip
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from kivystudio.behaviors import HoverBehavior

Builder.load_string('''
#: import Factory kivy.factory.Factory

<StudioSplitter>:
    strip_cls: Factory.StudioSplitterStrip
    strip_size: '4dp'

<StudioSplitterStrip>
    background_down: ''
    background_normal: ''
    background_color: .12,.12,.12,1

 ''')

class StudioSplitter(Splitter):
    pass

class StudioSplitterStrip(HoverBehavior, SplitterStrip):

    moving = BooleanProperty(False)

    def on_hover(self, *args):
        if self.hover:
            Window.set_system_cursor('size_we')
        else:
            if not self.moving:
                Window.set_system_cursor('arrow')

    def on_press(self):
        self.moving = True

    def on_touch_up(self, touch):
        if self.moving:
            Window.set_system_cursor('arrow')
            self.moving = False
        
        return super(StudioSplitterStrip, self).on_touch_up(touch)


if __name__ == "__main__":
    root = Builder.load_string('''
    BoxLayout:
        Button:
            id: w1
            size_hint_x: None
            width: 200
        StudioSplitter:
            min_size: self.parent.width-200
            max_size: max(self.parent.width*0.8, dp(130))
            on_right: self.right=root.right; w1.width = root.width-self.width
            Button:
                text: 'Spit'
    ''')
    from kivy.base import runTouchApp
    runTouchApp(root)
