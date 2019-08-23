from kivy.uix.textinput import TextInput
from kivy.lang import Builder

class SearchInput(TextInput):
    pass

Builder.load_string('''
<SearchInput>:
    canvas.after:
        Color:
            rgba: self.line_color
        Line:
            rectangle: [self.x,self.y,self.width,self.height]
    foreground_color: 1,1,1,1
    background_color: .1,.1,.12,1
    line_color: .8,.8,.8,0
    hint_text_color: .6,.6,.6,1
    cursor_color: 1,1,1,1
    size_hint_y: None
    height: self.minimum_height
    on_focus:
        if self.focus: self.line_color=.8,.8,.8,1
        else: line_color=.8,.8,.8,0
    
''')