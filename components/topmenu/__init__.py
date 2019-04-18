
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty

from kivystudio.behaviors import HoverBehavior
import dropmenu

__all__ = ('TopMenu',)


class TopMenu(GridLayout):
    drop_on_hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(**kwargs)

    def drop(self, btn, hover):
        if hover and not self.dropdown.parent:
            self.dropdown.drop_list=btn.drop_list
            self.dropdown.open(btn)
        else:
            Clock.schedule_once(self.decide_drop)
    
    def decide_drop(self, dt):
        if not self.dropdown.hover:
            self.dropdown.dismiss()

    def drop_menu(self, menu_name, index):
        menu = getattr(dropmenu, menu_name)()
        menu.open(self.children[index])



class TopMenuItem(HoverBehavior, ButtonBehavior, Label):

    def on_hover(self, *args):
        if self.hover:
            self.text = "[u]" + self.text + "[/u]"
            self.color = (1,.9,.9,1)
                
        else:
            self.text = self.text.replace('[u]','').replace('[/u]','')
            self.color = (.9,.9,.9,1)
            

class DropMenu(DropDown):
    pass

class DropMenuItem(Button):
    pass


Builder.load_string('''

<TopMenu>:
    size_hint_y: None
    height: '40dp'
    rows: 1
    canvas.before:
        Color:
            rgba: .2,.2,.2,1
        Rectangle:
            size: self.size
            pos: self.pos
    TopMenuItem:
        text: 'File'
        on_release:
            root.drop_on_hover=False;
            root.drop_menu('FileTopMenu', 2)

    TopMenuItem:
        text: 'Selection'
        on_release:
            root.drop_on_hover=False;
            root.drop_menu('FileTopMenu', 1)

    TopMenuItem:
        text: 'Edit'
        on_release:
            root.drop_on_hover=False;
            root.drop_menu('FileTopMenu', 0)


<TopMenuItem>:
    size_hint_x: None
    width: '60dp'
    markup: True

<DropMenu>:
    Button:
        text: 'My first Item'
        size_hint_y: None
        height: 40
        on_release: root.select('item1')
    Label:
        text: 'Unselectable item'
        size_hint_y: None
        height: 40
    Button:
        text: 'My second Item'
        size_hint_y: None
        height: 40
        on_release: root.select('item2')

<DropMenuItem>:
    size_hint_y: None
    height: 40

''')