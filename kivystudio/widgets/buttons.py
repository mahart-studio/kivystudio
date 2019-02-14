
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import (StringProperty, NumericProperty, ObjectProperty,
							 ListProperty, BooleanProperty)
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.animation import Animation

from kivy.graphics import Line, Color, Ellipse, Rectangle, RoundedRectangle
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.logger import Logger

from kivy.base import runTouchApp


__all__ = ('NormalButton','IconButton','Effects', 'AlertPopup')


class NormalButton(Button):
	'''Root Button with special features
	most of the other buttons inherites from this guy'''

	shape = StringProperty('rounded_rectangle')
	'''determine the shape of the button
		available shapes are 
		['rectangle', 'rounded_rectangle', 'Ellipse']  
		shape is a string property and defualts to 'rounded_rectangle' '''
	

	def __init__(self, **kwargs):
		self.register_canvas()
		super(NormalButton, self).__init__(**kwargs)

	def on_shape(self, instance, value):
		Factory.unregister('ButtonShape')	 # unregister before calling again
		self.register_canvas()

	def register_canvas(self):
		if self.shape == 'rounded_rectangle':
			Factory.register('ButtonShape', RoundedRectangle)

		elif self.shape == 'rectangle':
			Factory.register('ButtonShape', Rectangle)

		elif self.shape == 'ellipse':
			Factory.register('ButtonShape', Ellipse)
		else:
			Logger.error("MahartStudio: Invalid option %s for NormalButton" % ''.join(self.shape))
	

class IconButton(NormalButton):
	icon_source = StringProperty('')


class IconToggle(ToggleButtonBehavior, Image):
	normal_source = StringProperty('')
	down_source = StringProperty('')


class RetainButton(TouchRippleButtonBehavior, Label):

	retain = BooleanProperty(False)
	ripple_duration_in = .3
	touch = BooleanProperty(False)
	check_touched = BooleanProperty(True)
	ripple_fade_from_alpha = .5
	ripple_fade_to_alpha = .4
	ripple_color = ListProperty((0, 0, 0, 1))
	background_color = ListProperty((1, 1, 1, 1))

	def __init__(self, **kwargs):
		super(RetainButton, self).__init__(**kwargs)
		self.register_event_type('on_retain_touch')
		self.register_event_type('on_touched')
		
	def on_retain_touch(self, *largs):
		pass

	def on_touched(self, *largs):
		pass
	
	def change_state(self, dt):
		self.check_touched = False

		self.retain = not self.retain
		self.dispatch('on_retain_touch')

	def on_touch_down(self, touch):
		collide_point = self.collide_point(touch.x, touch.y)

		if collide_point:
			Clock.schedule_once(self.change_state, .4)
			touch.grab(self)
			self.ripple_show(touch)
			return True
		return False

	def on_touch_up(self, touch):
		if touch.grab_current is self:

			if self.check_touched:
					self.touch = not self.touch
					self.dispatch('on_touched')
			else:
				self.check_touched = True

			Clock.unschedule(self.change_state)
			touch.ungrab(self)
			self.ripple_fade()
			return True
		return False


class LeftIconButton(NormalButton):

	icon_width = NumericProperty(40)
	'''width of the icon defualts to 32dp
	icon_width is a Numeric Property'''
	
	icon_source= StringProperty('')
	'''source image of icon'''
	
	text_color = ListProperty([0,0,0,1])
	'''color for the text, *Note LeftIconButton doesn't accept
	the color property'''


class RightIconButton(NormalButton):

	icon_width = NumericProperty(40)
	'''width of the icon defualts to 32dp
	icon_width is a Numeric Property'''
	
	icon_source= StringProperty('')
	'''source image of icon'''

	text_color = ListProperty([0,0,0,1])
	'''color for the text, *Note RightIconButton doesn't accept
	the color property'''


class DropButton(ToggleButtonBehavior, BoxLayout):
	main_widget= ObjectProperty()
	drop_widget = ObjectProperty()
	add_now = BooleanProperty(False)
	background_color= ListProperty([.95,.95,.95,1])
	canvas_color= ListProperty([.95,.95,.95,1])

	drop_anim = StringProperty('in_quad')
	'animation type used to when the button drops'

	fold_anim = StringProperty('out_quad')
	'''animation type used to when the button folds 
	  	back to it's normal state'''

	canvas_shape = StringProperty('RoundedRectangle')

	def __init__(self, **kwargs):
		self.register_canvas()
		super(DropButton, self).__init__(**kwargs)

	def on_canvas_shape(self, *args):
		Factory.unregister('DropCanvas')
		self.register_canvas()

	def register_canvas(self):
		if self.canvas_shape == 'RoundedRectangle':
			Factory.register('DropCanvas', RoundedRectangle)
		else:
			Factory.register('DropCanvas', Rectangle)

	def on_state(self, l, state):
		self.canvas_color = [.5,.5,.5,1]
		anim_color =Animation(canvas_color=self.background_color,d=.1)
		anim_color.start(self)
		if self.state=='down':
			anim_height = Animation(height=self.height+self.drop_widget.height,d=0.1,t=self.drop_anim)
			anim_height.start(self)
			self.add_now =True
			self.add_widget(self.drop_widget)
		else:
			if self.drop_widget in self.children[:]:
				anim_height = Animation(height=self.height-self.drop_widget.height,d=0.1,t=self.fold_anim)
				anim_height.start(self)
				self.remove_widget(self.drop_widget)
				self.add_now =False

	def add_widget(self, widget):
		if len(self.children) == 1 and not self.add_now:
			self.drop_widget = widget
		elif len(self.children) == 1 and self.add_now:
			super(DropButton, self).add_widget(widget)

		elif len(self.children) == 0:
			super(DropButton, self).add_widget(widget)
			self.main_widget = widget

		elif len(self.children)==2:
			raise Exception(
				'Can\'t add more than two widgets'
				'directly to DropButton')



Builder.load_string('''
<NormalButton>:
	color: 0,0,0,1
	shape: root.shape
	background_normal: ''
	background_down: ''
    background_color: 0,0,0,0
	down_color: (.8,.8,.8,1)
	normal_color: (1,1,1,1)
	canvas.before:
		Color: 
			rgba: self.normal_color if self.state == 'normal' else self.down_color
		ButtonShape:
			source: self.background_normal if self.state is 'normal' else self.background_down
			size: self.size
			pos: self.pos

<IconButton>:
    icon_source: root.icon_source
    color: (1, 1, 1, 0)
    Image:
        size: root.size
        pos: root.pos
        source: root.icon_source

<IconToggle>:
	source: root.normal_source
	on_state:
		if self.state == 'down': self.source = self.down_source
		else: self.source = self.normal_source

<LeftIconButton>:
	icon_width: root.icon_width
	icon_source: root.icon_source
	padding: dp(root.icon_width + 20), 0
	text_size: self.size
	valign: 'middle'
	halign: 'left'

	BoxLayout:
		size: root.size
		pos: root.pos
		Image:
			size_hint_x: None
			width: root.icon_width
			source: root.icon_source
		Label:

<RightIconButton>:
	icon_pos: root.icon_source
	icon_width: root.icon_width
	icon_source: root.icon_source
	padding: '20dp', 0
	text_size: self.size
	valign: 'middle'
	halign: 'left'

	BoxLayout:
		size: root.size
		pos: root.pos
		Label:
		Image:
			size_hint_x: None
			width: root.icon_width
			source: root.icon_source
			

<RetainButton>:
    background_color: root.background_color
    canvas.before:
        Color: 
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.pos


<DropButton>:
    background_color: [.95,.95,.95,1]
    canvas_color: root.background_color
    canvas.before:
        Color:
            rgba: root.canvas_color 
        DropCanvas:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    size_hint_y: None
    height: '50dp'
    group: 'same group'
''')



def test(*largs):
	print(largs)

if __name__ == '__main__':

	# Alert popup example
	from functools import partial	
	popup = AlertPopup(title='Alert', message='You system Contains a virus', comfirm=partial(test, 'avour', 'Developer', 'Musician'))
	btn = Button(text='Press me')
	btn.bind(on_release=lambda a: popup.open())
	runTouchApp(btn)

	rbtn = RightIconButton(size_hint=(None,None), width=300, height=60, pos=(20, 40), icon_source='/root/croped.jpg', text='IconButton')
	Effects().add_shadow(rbtn)
	runTouchApp(rbtn)

#	runTouchApp(IconButton(size_hint=(None,None), width=70, height=70, pos=(20, 40), icon_source='/root/croped.jpg', shape='ellipse'))

#	button = NormalButton(text='Normal Button',shape='ellipse', size_hint=(None,None), width=60, height=60, pos=(20, 40), font_size='10dp', color=(1,0,1,1))
#	runTouchApp(button)

	# AutoCarousel Example
	import os
	caro = AutoCarousel(slide_direction='left', slide_duration=2)
	dirs = '/root/Desktop/Podcasts/X-Force/pics'
	for i in os.listdir(dirs):
		caro.add_widget(Image(source=os.path.join(dirs, i)))
	runTouchApp(caro)
