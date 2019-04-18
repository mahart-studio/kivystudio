from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from kivy.core.window import Window


class TestBtn(Button):
	pass

class MainApp(App):
	def build(self):
		return TestBtn(text='Showing')