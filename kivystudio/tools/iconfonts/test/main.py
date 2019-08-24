from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp
from kivy.lang import Builder

import os, json ,sys
from os.path import join, dirname
filepath = join(os.getcwd(), __file__) 
sys.path.append(dirname(dirname(__file__)))
from iconfonts import register, icon

font_file = join(dirname(__file__), 'font-awesome.fontd')
register('awesome_font', 'font-awesome.ttf',
     font_file)


with open(font_file, 'r') as f:
    fontd = json.loads(f.read())

class Boxer(BoxLayout):

	def search(self, text):
		add_icons(text)

root = Builder.load_string('''
Boxer:
	orientation: 'vertical'
	TextInput:
		size_hint_y: None
		height: '48dp'
		on_text: root.search(self.text)
	ScrollView:
		bar_width: '24dp'
		GridLayout:
			id: grid
			height: self.minimum_height
			size_hint_y: None
			cols: 1
''')

def add_icons(search=''):
	root.ids.grid.clear_widgets()
	keys = list(fontd.keys())
	keys.sort()
	for icon_name in keys:
		if search and icon_name.find(search)==-1:
			continue
		lb = Label(markup=True, size_hint_y=None)
		lb.text= '[color=3280ff]%s[/color] '%(icon(icon_name, 32)) + icon_name
		root.ids.grid.add_widget(lb)

add_icons()
runTouchApp(root)
