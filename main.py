from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '730')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

import sys
import os
sys.path.append(os.pardir)
filepath = os.path.dirname(__file__)

# mimetypes.add_type('text/kv', '.kv')

from kivy.lang import Builder
Builder.load_file(os.path.join(filepath,'main.kv'))

from kivy.app import App
from kivystudio.assembler import Assembler

class KivyStudio(App):

    def build(self):
        return Assembler

if __name__ == "__main__":
    KivyStudio().run()