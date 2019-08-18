from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import (TabbedPanel,
            TabbedPanelContent, TabbedPanelHeader)


class StudioPanelItem(TabbedPanelHeader):
    ''' Kivy Studio Panel Item for easy use,
    acts exactly like the defualt kivy panelitem
    just just has a custom header class so you can 
    specify you costume header class 
    '''

    header_cls = ObjectProperty(None)

    content = ObjectProperty(FloatLayout())

    def __init__(self, **kwargs):
        super(StudioPanelItem, self).__init__(**kwargs)

    def add_widget(self, widget):
        self.content.add_widget(widget)

    def remove_widget(self, widget):
        self.content.remove_widget(widget)
