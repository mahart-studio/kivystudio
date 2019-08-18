from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivystudio.behaviors import HoverBehavior, HoverInfoBehavior

class IconLabel(HoverInfoBehavior, Label):
    
    def __init__(self, **k):
        super(IconLabel, self).__init__(**k)
        self.markup=True


class IconButtonLabel(ButtonBehavior, IconLabel):
    pass

class IconToggleLabel(ToggleButtonBehavior, IconLabel):
    pass