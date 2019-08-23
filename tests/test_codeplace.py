
from kivy.tests.common import GraphicUnitTest
from kivy.base import EventLoop

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


class CodePlaceTest(GraphicUnitTest):

    def test_tabState(self):
        from kivystudio.components.codeplace import CodePlace, get_tab_from_group

        code_place = CodePlace()
        filename1 = 'test_codeplace.py'
        filename2 = 'test_codeplace1.py'
        code_place.add_code_tab(filename=filename1)
        code_place.add_code_tab(filename=filename2)
        self.render(code_place)

        # ensure widow safely
        EventLoop.ensure_window()

        tab1 = get_tab_from_group(filename1)
        tab2 = get_tab_from_group(filename2)

        self.assertEqual(tab1.state, 'normal')
        self.assertEqual(tab2.state, 'down')


if __name__ == "__main__":
    import unittest
    unittest.main()
