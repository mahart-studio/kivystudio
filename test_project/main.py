from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder

class Btn(Button):
	pass

class MainApp(App):
	def build(self):
		return Btn(text='sdsd',font_size=30,bold=True)