from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivystudio.behaviors import HoverBehavior

class IconLabel(Label):
    
    def __init__(self, **k):
        super(IconLabel, self).__init__(**k)
        self.markup=True


class IconButtonLabel(ButtonBehavior, IconLabel):
    pass

class IconToggleLabel(ToggleButtonBehavior, IconLabel):
    pass

class HoverIconLabel(HoverBehavior, IconLabel):
    pass
    
class HoverIconButtonLabel(HoverBehavior, IconButtonLabel):
    pass

class HoverIconToggleLabel(HoverBehavior, IconToggleLabel):
    pass