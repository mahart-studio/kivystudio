
from kivy.tests.common import GraphicUnitTest
from kivy.base import EventLoop

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

class EmulatorTest(GraphicUnitTest):

    def setUp(self):
        from kivystudio.parser import emulate_file
        from kivystudio.components.emulator_area import emulator_area
        EventLoop.ensure_window()
        self.emulate_file = emulate_file
        self.emulator_area = emulator_area

    def test_emulation(self):
        from kivy.uix.button import Button

        self.emulate_file('/root/Pictures/test.py')
        root_widget = self.emulator_area().screen_display.screen.root_widget
        self.assertEqual(isinstance(root_widget, Button), True)

    def test_changeScreen(self):
        from kivy.uix.button import Button

        self.emulate_file('/root/Pictures/test.py')
        root_widget = self.emulator_area().screen_display.screen.root_widget
        self.assertEqual(isinstance(root_widget, Button), True)

        # then change screen
        screen_display = self.emulator_area().screen_display
        screen_display.screen_name = 'IpadScreen'
        self.assertEqual(isinstance(root_widget, Button), True)

        # change screen again
        screen_display.screen_name = 'IphoneScreen'
        self.assertEqual(isinstance(root_widget, Button), True)

    def test_scaling(self):
        self.emulate_file('/root/Pictures/test.py')
        root_widget = self.emulator_area().screen_display.screen.root_widget



if __name__ == "__main__":
    import unittest
    unittest.main()
