![Screenshot](https://github.com/jeysonmc/garden.iconfonts/blob/master/screenshot.png "Scrennshot")


Kivy-iconfonts
==============

Simple helper functions to make easier to use icon fonts in Labels and derived widgets

Usage
=====

Once you have a .fontd file (see below) for your ttf iconfont generated you can use it like this:

In your main.py register your font:
```python
    iconfonts.register('default_font', 'iconfont_sample.ttf', 'iconfont_sample.fontd')
```

In your kv file or string:
```yaml
    #: import icon kivy.garden.iconfonts.icon
    Button:
        markup: True # Always turn markup on
        text: "%s"%(icon('icon-comment'))
```
See __init__.py for another example.

Generating a fontd file
=====================

A .fontd file is just a python dictionary filled with icon_code: unicode_value entries. This information is extracted from a css file (all iconfonts packages I've seen have one).

**Example with Font-Awesome**

1. Download Font-Awesome (http://fortawesome.github.io/Font-Awesome/)
2. Copy both the TTF and CSS files (fonts/fontawesome-webfont.ttf and css/font-awesome.css) to your project
3. Create and execute a python script to generate your fontd file:
```python
iconfonts.create_fontdict_file('font-awesome.css', 'font-awesome.fontd')
```
4. If everything went well your font dictionary file exists. You can delete the css file (font-awesome.css)


More IconFonts
==============
- http://fortawesome.github.io/Font-Awesome/
- http://fontello.com/
- https://icomoon.io

LICENSE
=======

MIT (except sample font that I got from http://fontello.com)


Credits
=======

Author: Jeyson Molina <jeyson.mco@gmail.com>
