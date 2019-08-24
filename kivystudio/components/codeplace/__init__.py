
from .codeplace import CodePlace

from kivystudio.widgets.splitter import StudioSplitter
from kivystudio.components.terminal import TerminalSpace

class CodeContainer(StudioSplitter):
    pass
code_container = CodeContainer()
container = code_container.ids.container


code_place = CodePlace()
code_place.add_code_tab(tab_type='welcome')  # add welcoming tab

terminal = TerminalSpace()

container.add_widget(code_place)
container.add_widget(terminal)
