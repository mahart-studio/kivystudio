
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty

from kivystudio.behaviors import HoverBehavior
from . import dropmenu

__all__ = ('TopMenu',)


class TopMenu(GridLayout):
    
    drop_on_hover = BooleanProperty(False)
    menu = ObjectProperty()

    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(**kwargs)

    # def drop(self, btn, hover):
    #     if hover and not self.dropdown.parent:
    #         self.dropdown.drop_list=btn.drop_list
    #         self.dropdown.open(btn)
    #     else:
    #         Clock.schedule_once(self.decide_drop)
    
    # def decide_drop(self, dt):
    #     if not self.dropdown.hover:
    #         self.dropdown.dismiss()

        
    def open_menu(self, widget):
        if self.menu:   
            x = self.menu.dismiss()
        menu_name = self.remove_underscore(widget.text) + 'TopMenu'
        setattr(self, 'menu_name', getattr(dropmenu, menu_name)())
        self.menu = getattr(self, 'menu_name')
        self.menu.open(self.children[widget.index])
    
    def remove_underscore(self, text):
        return  text.replace('[u]','').replace('[/u]','')

    def add_underscore(self,text):
        return "[u]" + text + "[/u]"


class TopMenuItem(HoverBehavior, ButtonBehavior, Label):

    def on_hover(self, *args):
        widget, hover = args
        if hover:
            widget.text = self.parent.add_underscore(widget.text)
            widget.color = (.1,.5,.1,1)
        else:
            widget.text = self.parent.remove_underscore(widget.text)
            widget.color = (0,0,0,1)
    

Builder.load_string('''

<TopMenu>:
    size_hint_y: None
    height: '24dp'
    rows: 1
    canvas.before:
        Color:
            rgba: .85,.85,.85,1
        Rectangle:
            size: self.size
            pos: self.pos
    TopMenuItem:
        text: 'File'
        index:4
        on_release: root.open_menu(self)

    TopMenuItem:
        text: 'Edit'
        index:3
        on_release: root.open_menu(self)

    TopMenuItem:
        text: 'View'
        index:2
        on_release: root.open_menu(self)
    
    TopMenuItem:
        text: 'Selection'
        index:1
        on_release: root.open_menu(self)
    
    TopMenuItem:
        text: 'Help'
        index:0
        on_release: root.open_menu(self)

<TopMenuItem>:
    size_hint_x: None
    width: '60dp'
    markup: True
    color: (0,0,0,1)



''')
