from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

MAX_LOG_LINES = 300

class ErrorLogger(BoxLayout):
    
    text = StringProperty()

    def log(self, msg):
        lines = self.text.splitlines()
        if len(lines) > MAX_LOG_LINES:    # clean previous logs
            self.text = '\n'.join(lines[int(MAX_LOG_LINES/2):])
        self.text += msg+'\n'

    def clear_logs(self):
        self.text = ''

class InternalErrorLogger(BoxLayout):
    
    text = StringProperty('Hello '*39)

Builder.load_string('''
<ErrorLogger>:
    ScrollView:
		bar_width: '8dp'
        Label:
            text: root.text
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
            valign: 'top'
            halign: 'left'
            color: .8,.8,.8,1
            markup: True
            font_size: '14sp'
''')