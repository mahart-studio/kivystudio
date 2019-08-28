'''
KivyStudio main.py
entry point for the Application
'''

import sys, os
sys.path = [os.pardir] + sys.path

# from kivy.config import Config
# Config.set('modules', 'monitor', '')

from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivystudio import tools

filepath = dirname(__file__)
tools.load_kv(__file__,'main.kv')

# registering custom icons
tools.iconfonts.register('awesome_font',
    join(filepath,'resources/font-awesome.ttf'),
    join(filepath, 'resources/font-awesome.fontd'))

from kivystudio.assembler import Assembler


class KivyStudio(App):

    def build(self):
        return Assembler
    
    def run(self):
        super(KivyStudio, self).run()


studio_app = KivyStudio()

def main():
    studio_app.run()

if __name__ == "__main__":
    main()
