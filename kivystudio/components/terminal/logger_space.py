from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

class ErrorLogger(BoxLayout):
    
    text = StringProperty('Hello '*39)

class InternalErrorLogger(BoxLayout):
    
    text = StringProperty('Hello '*39)

Builder.load_string('''
<ErrorLogger>:
    ScrollView:
        Label:
            text: root.text
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
            valign: 'top'
            halign: 'right'
''')