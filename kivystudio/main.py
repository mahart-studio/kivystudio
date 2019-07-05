
import sys, os
sys.path.append(os.pardir)

from kivy.config import Config
Config.set('modules', 'monitor', '')

from kivy.storage.jsonstore import JsonStore

from kivy.app import App
from os.path import dirname, join
from kivystudio.tools import iconfonts
from kivy.lang import Builder


filepath = dirname(__file__)
iconfonts.register('awesome_font',
    join(filepath,'resources/font-awesome.ttf'),
    join(filepath, 'resources/font-awesome.fontd'))

Builder.load_file(join(filepath,'main.kv'))

from kivystudio.assembler import Assembler

class KivyStudio(App):

    def __init__(self,**k):
        super(KivyStudio,self).__init__(**k)
        self.user_settings = JsonStore(os.path.join(self.user_data_dir, 'user_settings.json'))
        if not self.user_settings.exists('file-settings'):
            self.fill_config_settiigs()

    def build(self):
        return Assembler

    def fill_config_settiigs(self):
        put = self.user_settings.put
        put('file-settings', auto_save=False)
        put('emulator-settings', auto_emulate=False)

studio_app = KivyStudio()
def main():
    studio_app.run()

if __name__ == "__main__":
    studio_app.run()
