from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '730')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from os.path import dirname, join
filepath = dirname(__file__)


from kivy.lang import Builder
from kivystudio.tools import iconfonts
font_file = join(dirname(__file__), 'resources/font-awesome.fontd')
iconfonts.register('awesome_font', join(dirname(__file__),'resources/font-awesome.ttf'),
     font_file)

Builder.load_file(join(filepath,'main.kv'))
from kivystudio.assembler import Assembler

