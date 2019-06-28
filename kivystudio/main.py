
import sys, os
sys.path.append(os.pardir)

from kivy.storage.jsonstore import JsonStore

from kivy.app import App
from kivystudio.assembler import Assembler

class KivyStudio(App):

    def build(self):
        self.user_settings = JsonStore(os.path.join(self.user_data_dir, 'user_settings.json'))
        if not self.user_settings.exists('file-settings'):
            self.fill_config_settiigs()
        return Assembler

    def fill_config_settiigs(self):
        put = self.user_settings.put
        put('file-settings', auto_save=False)
        put('emulator-settings', auto_emulate=False)


if __name__ == "__main__":
    KivyStudio().run()
