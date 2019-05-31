from kivy.uix.image import Image
from kivy.base import runTouchApp as app


class Imager(Image):

    def on_touch_down(self, touch):
        print(touch.button)

app(Imager(source='java.png'))

