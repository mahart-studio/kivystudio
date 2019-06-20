================
FileManager
================

A comprehensive file chooser intensively designed for the for desktop platform
The widget was originaly design and used for **kivy Studios **but is now available on kivy garden

#### KivyStudio
<!-- ![KivyStudio](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png) -->

[![Build Status](https://travis-ci.com/MichaelStott/KivMob.svg?branch=master)](https://travis-ci.com/MichaelStott/KivMob)
[![PyPI version](https://badge.fury.io/py/kivmob.svg)](https://badge.fury.io/py/kivmob)
[![Python](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Downloads](https://pepy.tech/badge/kivmob)](https://pepy.tech/project/kivmob)
[![Maintainability](https://api.codeclimate.com/v1/badges/add8cd9bd9600d898b79/maintainability)](https://codeclimate.com/github/MichaelStott/KivMob/maintainability)

Simple method

```python
filemanager.open_file(path='.', callback=callback)

filemanager.save_file(path='.', callback=callback)

filemanager.choose_dir(path='.', callback=callback)
```

### Installation

```
garden install garden.filemanager
```


### Quickstart


```python
from kivy.uix.button import Button
from kivy.garden.filemanager import filemanager

def callback(path):
  (path)

def open_file(*a):
  filemanager.open_file(path='.', callback=callback)

btn = Button(text='Push Me')
btn.bind(on_release=open_file)

if __name__ == '__main__':
	MyApp().run()
```

### FileManager being used in Kivy Studio
<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/resources/showcase/Screenshot(3).png">
</p>

### FileManager Showcase

_Please contact us via pull request or project issue if you would like your app featured in this README and the documentation._


### Other

<!-- Links pertinent to README -->
[Kivy]: <https://kivy.org/>
[KivyStudio]: <https://mahartstudio.com/kivystudio/>
[Buildozer]: <https://github.com/kivy/buildozer>

<!-- App showcase author links -->
<p align="center">
    <a href='<https://mahartstudio.com>'> <b>Mahart Studio</b> </a>
</p>

[avour]: <https://github.com/avour>