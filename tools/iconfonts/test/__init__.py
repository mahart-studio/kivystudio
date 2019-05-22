from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp

import os
from os.path import join, dirname
import json
import sys
filepath = join(os.getcwd(), __file__) 

sys.path.append(dirname(dirname(filepath)))
from iconfonts import register, icon

font_file = join(dirname(__file__), 'font-awesome.fontd')

register('awesome_font', 'font-awesome.ttf',
     font_file)


with open(font_file, 'r') as f:
    fontd = json.loads(f.read())

scroll = ScrollView(bar_width='24dp')
grid = GridLayout(cols=1,size_hint_y=None, height='40dp')
grid.bind(minimum_height=grid.setter('height'))
scroll.add_widget(grid)

keys = fontd.keys()
keys.sort()
for icon_name in keys:
	lb = Label(markup=True, size_hint_y=None, color=(1,0,0))
	lb.text= '%s '%(icon(icon_name, 32)) + icon_name
	grid.add_widget(lb)

runTouchApp(scroll)
	

