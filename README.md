#### KivyStudio
<!-- ![KivyStudio](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png) -->

[![Build Status](https://travis-ci.com/MichaelStott/KivMob.svg?branch=master)](https://travis-ci.com/MichaelStott/KivMob)
[![Python](https://img.shields.io/badge/python-2-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Python](https://img.shields.io/badge/python-3-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Downloads](https://pepy.tech/badge/kivmob)](https://pepy.tech/project/kivmob)
[![Maintainability](https://api.codeclimate.com/v1/badges/add8cd9bd9600d898b79/maintainability)](https://codeclimate.com/github/MichaelStott/KivMob/maintainability)

A kivy software development environment targeted towards fast testing and interactive development.
* #### Features
  - Emulation can be done in real time
  - Supports multiple screen views for mobile devices
  - Supports orientation changes for mobile devices
  - Supports outer window emulation for desktop intended emulation and for full test on mobile devices

* **Status**: under development...
* **Release**: 0


### Installation

Package file for various platform will be available on first release


### Demo Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(1).png">
</p>

### Quickstart

* Create a new folder
* Open **kivystudio**.
* On the top menu bar. go to **File** option
* Click **Open Folder**,

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(2).png">
</p>

* Choose your folder

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(3).png">
</p>

* Press <kbd>Ctrl</kbd> + <kbd>N</kbd> : a new file will open-up


Copy the following code into the editor provided.
```python
from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
	def build(self):
		return Button(text='Welcome to KivyStudio!!')

if __name__ == '__main__':
	MyApp().run()
```

* To save the code, press <kbd>Ctrl</kbd> + <kbd>S</kbd>.
* Right click on **File** tab
* Choose **Set for Emulation**, or press <kbd>Ctrl</kbd> + <kbd>E</kbd> to select the file for emulation
* Then, press <kbd>Ctrl</kbd> + <kbd>R</kbd> to see the output, *OR* you can also set auto-emulation from **File** tab
* To switch screens, use the <kbd>Ctrl</kbd> + <kbd>Tab</kbd> combination
* To open and close terminal panel, press <kbd>Ctrl</kbd> + <kbd>`</kbd>

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/showcase/Screenshot(4).png">
</p>

### Contributions
To contribute to this project
* Fork the repository
* Clone it
``` git clone https://github.com/mahart-studio/kivystudio.git``` 
* Start by solving an issue or fixing a known bug
* Create a **Pull Request**
* PR would be merged after review.
