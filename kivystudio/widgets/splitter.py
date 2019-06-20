from kivy.uix.splitter import Splitter, SplitterStrip
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from behaviors.hoverbehavior import HoverBehavior

Builder.load_string('''
#: import Factory kivy.factory.Factory

<StudioSplitter>:
    strip_cls: Factory.StudioSplitterStrip
    strip_size: '4dp'

<StudioSplitterStrip>
    background_down: ''
    background_normal: ''
    background_color: 0,0,0,0

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
                self.moving = False


    def on_press(self):
        self.moving = True

    def on_touch_up(self, touch):
        if self.moving:
            Window.set_system_cursor('arrow')
            self.moving = False
        
        return False

root = Builder.load_string('''
BoxLayout:
    Button:
        id: w1
        size_hint_x: None
    StudioSplitter:
        on_right: self.right=root.right; w1.width = root.width-self.width
        Button:
            text: 'Spit'
''')

if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(root)
