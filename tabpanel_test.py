from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
# from widgets.tabbedpanel import StudioHeader

Builder.load_string("""
<StipLayout>:
    padding: 0
    spacing: 0


<StudioHeader@TabbedPanelItem>:
    background_down: ''
    background_normal: ''
    background_color: 0,0,0,0
    canvas.before:
        Clear
        Color:
            rgba: 1,.4,.4,1
        Rectangle:
            size: self.size
            pos: self.pos
<Test>:
    # tab_pos: 'top_mid'
    size_hint: .5, .5
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False
    padding: 0
    spacing: 0
    on_current_tab: print(self.cols)
    StudioHeader:
        text: 'first tab'
        Label:
            text: 'First tab content area'
    StudioHeader:
        text: 'tab2'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'
    StudioHeader:
        text: 'tab3'
        RstDocument:
            text:
                '\\n'.join(("Hello world", "-----------",
                "You are in the third tab."))
""")
class Test(TabbedPanel):
    pass

class TabbedPanelApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    TabbedPanelApp().run()