![KivyStudio](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png)

[![Build Status](https://travis-ci.com/MichaelStott/KivMob.svg?branch=master)](https://travis-ci.com/MichaelStott/KivMob)
[![PyPI version](https://badge.fury.io/py/kivmob.svg)](https://badge.fury.io/py/kivmob)
[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Downloads](https://pepy.tech/badge/kivmob)](https://pepy.tech/project/kivmob)
[![Maintainability](https://api.codeclimate.com/v1/badges/add8cd9bd9600d898b79/maintainability)](https://codeclimate.com/github/MichaelStott/KivMob/maintainability)

A kivy software development environment targeted towards fast testing and interactive development.

  - Emulation can be done in real time
  - Supports multiple screen views for mobile devices
  - Supports orientation changes for mobile devices
  - Also supports outer window emulation for destop intended emulation and for full test for mobile devices

Status: Underdevelopment....
Release: 0


### Installation

You can download at.
```
https://mahartstudio.com/kivystudio
```

### Demo Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/resources/showcase/Screenshot(1).png">
</p>

### Quickstart

Create an new folder
open kivystudio.
on the top menu bar.
go to [file] - then click [open-folder],

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/resources/showcase/Screenshot(2).png">
</p>

then pick your folder

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/resources/showcase/Screenshot(3).png">
</p>

then enter [Ctrl-N] a new file will be opened for your


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

Finally, enter [Ctrl-S].
then, enter [Ctrl-R]. to see the output,
or you can set auto-emulation

<p align="center">
  <img src="https://raw.githubusercontent.com/mahart-studio/kivystudio/master/resources/showcase/Screenshot(4).png">
</p>

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
[KivyStudio]: <https://mahartstudio.com/kivystudio/>
[Google AdMob]: <https://www.google.com/admob/>
[Kivy]: <https://kivy.org/>
[Buildozer]: <https://github.com/kivy/buildozer>

<!-- App showcase author links -->
<p align="center">
    <a href='<https://mahartstudio.com>'> <b>Mahart Studio</b> </a>
</p>

[avour]: <https://github.com/avour>
[solomon]: <https://github.com/solomon1999>
[curiouspaul1]: <https://github.com/curiouspaul1>