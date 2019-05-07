![KivyStudio](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png)

[![Build Status](https://travis-ci.com/MichaelStott/KivMob.svg?branch=master)](https://travis-ci.com/MichaelStott/KivMob)
[![PyPI version](https://badge.fury.io/py/kivmob.svg)](https://badge.fury.io/py/kivmob)
[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Downloads](https://pepy.tech/badge/kivmob)](https://pepy.tech/project/kivmob)
[![Maintainability](https://api.codeclimate.com/v1/badges/add8cd9bd9600d898b79/maintainability)](https://codeclimate.com/github/MichaelStott/KivMob/maintainability)

Allows developers test and emulate their [kivy] project.

  - Emulation can e done on real time
  - Supports multiple screen views for mobile devices
  - Also support outer window emulation for destop intended emulation of for real test of mobile devices


### Installation

You can install KivMob with the following command.
```sh
$ pip install kivmob
```

### Demo Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/demo_screenshotv2.png">
</p>

### Quickstart

Create an new folder
open kivystudio then on the top menu bar.
go to [file] - then click [open-folder], then pick your folder
then enter [Ctrl-O] a new file ta will be opened for your

Copy the following into the file tab.
```python
from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    
    def build(self):
        return Button(text='Welcome to KivyStudio')

MyApp.run()
```

Finally, enter [Ctrl-r].
or you can set auto-emulation


### kivy Studio Showcase

_Please contact us via pull request or project issue if you would like your app featured in this README and the documentation._

<!-- List alphabetically please.  -->
| App | Play Store Link | Author |
| ------ | ------ | ------ |
| Learn Python Offline | https://play.google.com/store/apps/details?id=com.prog.ders.eng | [Yunus Ceyhan] |
| Gloworld | https://play.google.com/store/apps/details?id=com.worldglowfree.dom.com.world.glowfree | Prozee Games, [thegameguy] |
| MIUI Hidden Settings | https://play.google.com/store/apps/details?id=com.ceyhan.sets | [Yunus Ceyhan] |
| Themes for MIUI | https://play.google.com/store/apps/details?id=com.ceyhan.tema | [Yunus Ceyhan] |

### Other 


<!-- Links pertinent to README -->
[Google AdMob]: <https://www.google.com/admob/>
[Kivy]: <https://kivy.org/>
[Buildozer]: <https://github.com/kivy/buildozer>

<!-- App showcase author links -->
[thegameguy]: <https://github.com/thegameguy>
[Yunus Ceyhan]: <https://github.com/yunus-ceyhan>
