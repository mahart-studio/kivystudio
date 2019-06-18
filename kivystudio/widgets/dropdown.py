from kivystudio.behaviors import HoverBehavior
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder


Builder.load_string('''
<MenuDropDownBase>:
    canvas.after:
        Color:
            rgba: 0,0,0,.6
        Line:
            rectangle: [self.x, self.y, self.width, self.height]
    canvas.before:
        BorderImage:
            source: 'shadow32.png'
            border: (26, 26, 26, 26)
            size:(root.width + 68, root.height + 68)
            pos: (root.x-36, root.y-36)
''')

class DropDownBase(HoverBehavior, DropDown):
    
    is_open = ObjectProperty(False)
    
    auto_touch_dismiss = BooleanProperty(True)

    def on_open(self):
        self.is_open = True

    def on_dismiss(self):
        self.is_open = False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.auto_touch_dismiss:
                self.dismiss()
        
        return super(DropDownBase,self).on_touch_up(touch)

