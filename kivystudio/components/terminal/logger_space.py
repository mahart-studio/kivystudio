from kivy.uix.boxlayout import BoxLayout
from kivy import properties as prop
from kivy.lang import Builder
from kivy.factory import Factory

MAX_LOG_LINES = 260


class ErrorLogger(BoxLayout):
    
    text = prop.StringProperty()
    ''' property where the logs are stored '''

    top_pannel_items = prop.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        clearbtn = Factory.TopPanelButton(icon='fa-trash-o')
        clearbtn.bind(on_release=self.clear_logs)
        self.top_pannel_items.append(clearbtn)


    def log(self, msg):
        lines = self.text.splitlines()
        if len(lines) > MAX_LOG_LINES:    # clean previous logs
            self.text = '\n'.join(lines[int(MAX_LOG_LINES/2):])
        self.text += msg+'\n'
        self.ids.scroll.scroll_y = 0

    def clear_logs(self, *args):
        self.text = ''


class InternalErrorLogger(BoxLayout):
    
    text = prop.StringProperty('Hello '*39)

Builder.load_string('''
<ErrorLogger>:
    ScrollView:
        id: scroll
		bar_width: '10dp'
        scroll_type: ['bars', 'content']
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