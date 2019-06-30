#### KivyStudio
<!-- ![KivyStudio](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png) -->

[![Build Status](https://travis-ci.com/MichaelStott/KivMob.svg?branch=master)](https://travis-ci.com/MichaelStott/KivMob)
[![Python](https://img.shields.io/badge/python-2-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Python](https://img.shields.io/badge/python-3-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Downloads](https://pepy.tech/badge/kivmob)](https://pepy.tech/project/kivmob)
[![Maintainability](https://api.codeclimate.com/v1/badges/add8cd9bd9600d898b79/maintainability)](https://codeclimate.com/github/MichaelStott/KivMob/maintainability)

A kivy software development environment targeted towards fast testing and interactive development.

  - Emulation can be done in real time
  - Supports multiple screen views for mobile devices
  - Supports orientation changes for mobile devices
  - Also supports outer window emulation for destop intended emulation and for full test for mobile devices

* Status: under development...
* Release: 0


### Installation

Package file for various platform will be available on first release


### Demo Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(1).png">
</p>

### Quickstart

* Create an new folder
* open kivystudio.
* on the top menu bar. go to [file]
* then click [open-folder],

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(2).png">
</p>

* pick your folder

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(3).png">
</p>

* Then enter [Ctrl-N] a new file will be opened for your


Copy the following into the file tab.
```python
from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
	def build(self):
		return Button(text='Welcome to KivyStudio!!')

if __name__ == '__main__':
	MyApp().run()
```

* Finally, enter [Ctrl-S].
* Right click on file tab
* clcik set for emulation
* then, enter [Ctrl-R]. to see the output, or you can set auto-emulation
* To switch screen use the [Ctrl] + [Tab] to do so

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(4).png">
</p>

##
### Contributions
To contribute to this project
* you just fork the repository
* Clone it
``` git clone https://github.com/mahart-studio/kivystudio.git``` 
* Then start, by solving an issue or fixing a known bug
* Then you send a pull request
* Then we review and merge
