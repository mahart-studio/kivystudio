from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '730')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

import sys
import os
sys.path.append(os.pardir)
filepath = os.path.dirname(__file__)


from kivy.lang import Builder
from kivystudio.tools import iconfonts
font_file = os.path.join(os.path.dirname(__file__), 'resources/font-awesome.fontd')
iconfonts.register('awesome_font', 'resources/font-awesome.ttf',
     font_file)

Builder.load_file(os.path.join(filepath,'main.kv'))

from kivy.app import App
from kivystudio.assembler import Assembler

class KivyStudio(App):
    # screen
    def build(self):
        # self.screen_manager = None
        return Assembler

if __name__ == "__main__":
    KivyStudio().run()
