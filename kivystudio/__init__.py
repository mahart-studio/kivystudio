from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '730')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

__version__ = '0.1.0.dev0'


def get_kivystudio_app():
     from .main import studio_app
     return studio_app

