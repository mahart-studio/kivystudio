
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import (BooleanProperty, ObjectProperty, 
                ListProperty, OptionProperty, NumericProperty)
from kivy.base import runTouchApp
from kivy.graphics import InstructionGroup, Color, Rectangle, RoundedRectangle, Callback
from kivy.uix.behaviors import FocusBehavior
from kivy.clock import Clock
from kivy.event import EventDispatcher

from kivy.core.window import Window, Keyboard

__all__ = ('HighlightBehavior', )

class HighlightBehavior(object):

    current_highlighted_child = ObjectProperty(None, allownone=True)
    ''' current highlighted child
        on ObjectProperty and defualts to None '''

    highlighted_color = ListProperty([.2,.5,1,.5])
    ''' color that show highlighted widget
        a ListProperty defualts to [.2,.5,1.5] make sure it transparent
        because it's drawn over the widget '''

    auto_scroll_to = BooleanProperty(False)
    ''' automatically scroll to the widget when widget is out of focus 
    note* parent most be a scrollview to enable the property'''

    highlighted_shape = OptionProperty('rectangle', options=['rounded_rectangle','rectangle'])


    highlight_orientation = OptionProperty('vertical', options=['vertical',
                                'horizontal', 'grid'])
    ''' Orientation in which the highlighting will take place if
    grid grid len must be set'''

    instruction_canvas = ObjectProperty(InstructionGroup())
    ''' internal instruction group used to draw the canvas on the
        currently highlighted child '''

    grid_len = NumericProperty(0)


    def __init__(self, **kwargs):
        super(HighlightBehavior, self).__init__(**kwargs)


    def set_first_child(self, dt):
        if len(self.children) >= 1:
            self.set_highlighted(self.children[0])


    def on_highlighted_color(self, *args):
        self.redraw_canvas()

    def redraw_canvas(self, *args):
        if self.current_highlighted_child:
            self.instruction_canvas.clear()
            self.instruction_canvas.add(Color(*self.highlighted_color))

            if self.highlighted_shape =='rectangle':
                self.instruction_canvas.add(Rectangle(pos=self.current_highlighted_child.pos, size=self.current_highlighted_child.size))
            elif self.highlighted_shape =='rounded_rectangle':
                self.instruction_canvas.add(RoundedRectangle(pos=self.current_highlighted_child.pos, size=self.current_highlighted_child.size))
            else:
                raise Exception('Invalid highlighted shape {}'.format(self.highlighted_shape))

    def on_focus(self, arg, focus):
        if focus:
            Window.bind(on_key_down=self.handle_key)
            if self.current_highlighted_child is None:
                Clock.schedule_once(self.set_first_child)
        else:
            Window.unbind(on_key_down=self.handle_key)


    def on_children(self, *args):
        if len(self.children) == 1:
            self.set_highlighted(self.children[0])


    def set_highlighted(self, child):
        if not (child == self.current_highlighted_child):
            if self.current_highlighted_child: # remove the canvas from the previosly highlighted child
                self.current_highlighted_child.canvas.after.remove(self.instruction_canvas)

            child.canvas.after.add(self.instruction_canvas)
            self.current_highlighted_child = child
            with child.canvas:
                Callback(self.redraw_canvas)

    def handle_key(self, keyboard, key, codepoint, text, modifier, *args):

        key_str = Keyboard.keycode_to_string(Window._system_keyboard, key)
        modifier.sort()
        if modifier:
            value = '_'.join(modifier) + '_' + key_str
        else:
            value = key_str
        
        callable_method = 'do_' + value

        try:
            func = getattr(self, callable_method)
        except AttributeError:
            pass
        else:
            func()

    def _moving(self):
        if self.auto_scroll_to:
            self.parent.scroll_to(self.current_highlighted_child)


    def do_up(self):
        if self.highlight_orientation == 'vertical':
            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index >= len(children)-1):
                self.set_highlighted(children[(index)+1])
                self._moving()
        
        elif self.highlight_orientation == 'horizontal':
            pass
        
        elif self.highlight_orientation == 'grid':
            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index+self.grid_len >= len(children)):
                self.set_highlighted(children[(index)+self.grid_len])
                self._moving()

        else:
            raise Exception('invalid highlight_orientation %s'%self.highlight_orientation)

    def do_down(self):
        if self.highlight_orientation == 'vertical':
            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index < 1):
                self.set_highlighted(children[(index)-1])
                self._moving()

        elif self.highlight_orientation == 'horizontal':
            pass
        
        elif self.highlight_orientation == 'grid':
            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index+self.grid_len < 1):
                self.set_highlighted(children[(index)-self.grid_len])
                self._moving()
        else:
            raise Exception('invalid highlight_orientation %s'%self.highlight_orientation)

    def do_right(self):
        if self.highlight_orientation == 'vertical':
            pass

        elif self.highlight_orientation == 'horizontal' or self.highlight_orientation == 'grid':

            self._moving()
            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index < 1):
                self.set_highlighted(children[(index)-1])
                self._moving()
        else:
            raise Exception('invalid highlight_orientation %s'%self.highlight_orientation)

    def do_left(self):

        if self.highlight_orientation == 'vertical':
            pass

        elif self.highlight_orientation == 'horizontal' or self.highlight_orientation == 'grid':

            children = self.children[:]
            index = children.index(self.current_highlighted_child)
            if not(index >= len(children)-1):
                self.set_highlighted(children[(index)+1])
                self._moving()

        else:
            raise Exception('invalid highlight_orientation %s'%self.highlight_orientation)

    def do_ctrl_up(self):
        pass

    def do_shift_up(self):
        pass
    def do_shift_down(self):
        pass
    def do_shift_left(self):
        pass
    def do_shift_up(self):
        pass

'''
        if value :
            self.map.get(value)[0]()
            return True
'''
class What(HighlightBehavior, FocusBehavior, GridLayout):
    pass

if __name__ == "__main__":
    what = What(cols=3, grid_len=3, highlight_orientation='grid')

    for btn in range(12):
        what.add_widget(Button(text=str(btn)))

    runTouchApp(what)
