from kivystudio.widgets.dropdown import DropDownBase

class ScreenDrop(DropDownBase):

    def open(self, widget, screen_display):
        self.screen_display = screen_display
        super(ScreenDrop, self).open(widget)