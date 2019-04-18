import kivy


def __init__(self, **kwargs):
	super(DesignerCodeInput, self).__init__(**kwargs)
	parser = Config.get_configparser('DesignerSettings')
	self.style_name = 'native_tweak'


def on_style_name(self, *args):
    super(DesignerCodeInput, self).on_style_name(*args)
    # self.style = NativeStyle()
    self.background_color = get_color_from_hex(self.style.background_color)
    self._trigger_refresh_text()
    

def on_style_name(self, *args):
    super(DesignerCodeInput, self).on_style_name(*args)
    # self.style = NativeStyle()
    self.background_color = get_color_from_hex(self.style.background_color)
    self._trigger_refresh_text()

def on_style_name(self, *args):
    super(DesignerCodeInput, self).on_style_name(*args)
    # self.style = NativeStyle()
    self.background_color = get_color_from_hex(self.style.background_color)
    self._trigger_refresh_text()
    
def on_show_edit(self, *args):
    pass

def on_touch_down(self, touch):
    '''Override of CodeInput's on_touch_down event.
       Used to emit on_show_edit
    '''
    if self.collide_point(*touch.pos):
        self.clicked = True
        self.dispatch('on_show_edit')

    	return super(DesignerCodeInput, self).on_touch_down(touch)

