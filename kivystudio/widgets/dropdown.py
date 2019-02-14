from kivystudio.behaviors import HoverBehavior
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_string('''
<MenuDropDownBase>:
    canvas.after:
        Color:
            rgba: 0,0,0,.6
        Line:
            rectangle: [self.x, self.y, self.width, self.height]
''')

class DropDownBase(HoverBehavior, DropDown):
    
    is_open = ObjectProperty(False)

    def on_open(self):
        self.is_open = True

    def on_dismiss(self):
        self.is_open = False
