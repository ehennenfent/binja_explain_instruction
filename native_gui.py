from __future__ import print_function
from binaryninja import show_message_box
from util import *
import cgi

mlil_tooltip = """Often, several assembly instructions make up one MLIL instruction.
The MLIL instruction shown may not correspond to this instruction
alone, or this instruction may not have a direct MLIL equivalent."""

html_template = """
<html>
<body>
<h3>Instruction:</h3>
<div style="font-family: monospace">{window.instruction}</div>
<hr>
<h3>Short Form:</h3>
{window.short_form}
<hr>
<h3>Description:</h3>
{window.description}
<hr>
<h3>Equivalent LLIL:</h3>
<div style="font-family: monospace">{window.llil}</div>
<hr>
<h3>Equivalent MLIL:</h3>
<div style="font-family: monospace">{window.mlil}</div>
<hr>
<h3>Flag Operations:</h3>
<div>{window.flags}</div>
<hr>
<h3>Instruction State:</h3>
<div style="font-family: monospace">{window.state}</div>
</body>
</html>
"""

def __None__(*args):
    return [("No documentation available", "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md")]

window = None

class ExplanationWindow(object):
    """ Displays a brief explanation of what an instruction does """
    def __init__(self):
        super(ExplanationWindow, self).__init__()
        self._instruction = ""
        self._shortForm = ""
        self._description = ""
        self._LLIL = ""
        self._MLIL = ""
        self._stateDisplay = ""
        self._flags = ""

        self.newline = '<br>'
        self.get_doc_url = __None__

    def show(self):
        rendered = html_template.format(window=window)
        show_message_box('Explain Instruction', rendered)

    @property
    def instruction(self):
        return self._instruction

    @property
    def description(self):
        return self._description

    @property
    def short_form(self):
        return self._shortForm

    @property
    def llil(self):
        return self._LLIL

    @property
    def mlil(self):
        return self._MLIL

    @property
    def state(self):
        return self._stateDisplay

    @property
    def flags(self):
        return self._flags

    @instruction.setter
    def instruction(self, instr):
        i, s = parse_instruction(self, instr)
        self._instruction = i
        self._shortForm = s

    @description.setter
    def description(self, desc_list):
        self._description = parse_description(self, desc_list)

    @llil.setter
    def llil(self, llil_list):
        self._LLIL = parse_llil(self, llil_list)

    @mlil.setter
    def mlil(self, mlil_list):
        self._MLIL = parse_mlil(self, mlil_list)

    @state.setter
    def state(self, state_list):
        self._stateDisplay = parse_state(self, state_list)

    @flags.setter
    def flags(self, tuple_list_list):
        self._flags = parse_flags(self, tuple_list_list)

    def escape(self, in_str):
        return cgi.escape(in_str)

def explain_window():
    global window
    # Creates a new window if it doesn't already exist
    if window is None:
        window = ExplanationWindow()
    return window
