
import sys, os
sys.path.append(os.pardir)

from kivy.app import App
from kivystudio.assembler import Assembler

class KivyStudio(App):

    def build(self):
        return Assembler

if __name__ == "__main__":
    KivyStudio().run()
