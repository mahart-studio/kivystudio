# -*- coding: utf-8 -*-
"""
    pygments.styles.native
    ~~~~~~~~~~~~~~~~~~~~~~

    pygments version of my "native" vim theme.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Token, Whitespace, Punctuation


class NativeTweakStyle(Style):
    """
    Pygments version of the "native" vim theme.
    """

    background_color = '#202020'
    highlight_color = '#404040'

    styles = {
        Token:              '#d0d0d0',
        Whitespace:         '#666666',

        Comment:            'italic #777777',
        Comment.Preproc:    'noitalic bold #cd2828',
        Comment.Special:    'noitalic bold #e50808 bg:#520000',

        Keyword:            'bold #CC6600',
        Keyword.Pseudo:     'nobold',
        Operator.Word:      'bold #CC6600',
        Operator:           '#CC6600',

        String:             '#FFCC00',
        String.Other:       '#ffa500',
        
        Number:             '#3677a9',

        Name.Builtin:       '#24909d',
        Name.Variable:      '#40ffff',
        Name.Constant:      '#40ffff',
        Name.Class:         'underline #447fcf',
        Name.Function:      '#447fcf',
        Name.Namespace:     'underline #447fcf',
        Name.Exception:     '#33CCFF',
        Name.Tag:           'bold #CC6600',
        Name.Attribute:     '#bbbbbb',
        Name.Decorator:     '#ffa500',
        Name.Builtin.Pseudo:  '#33CCFF',


        Generic.Heading:    'bold #ffffff',
        Generic.Subheading: 'underline #ffffff',
        Generic.Deleted:    '#d22323',
        Generic.Inserted:   '#589819',
        Generic.Error:      '#d22323',
        Generic.Emph:       'italic',
        Generic.Strong:     'bold',
        Generic.Prompt:     '#aaaaaa',
        Generic.Output:     '#cccccc',
        Generic.Traceback:  '#d22323',

        Error:              'bg:#FFFFFF #FFFFFF'
    }
