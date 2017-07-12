from __future__ import print_function
from binaryninja import show_message_box

mlil_tooltip = """Often, several assembly instructions make up one MLIL instruction.
The MLIL instruction shown may not correspond to this instruction
alone, or this instruction may not have a direct MLIL equivalent."""

html_template = """
<html>
<body>
<h3>Instruction:</h3>
{window.instruction}
<hr>
<h3>Short Form:</h3>
{window.short_form}
<hr>
<h3>Description:</h3>
{window.description}
<hr>
<h3>Equivalent LLIL:</h3>
{window.llil}
<hr>
<h3>Equivalent MLIL:</h3>
{window.mlil}
<hr>
<h3>Instruction State:</h3>
{window.state}
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

        self.get_doc_url = __None__

    def show(self):
        rendered = html_template.format(window=window)
        print(rendered)
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

    @instruction.setter
    def instruction(self, instr):
        print("Setting Instruction")
        if instr is not None:
            docs = self.get_doc_url(instr.split(' '))
            self._instruction = instr.replace('    ', ' ')
            self._shortForm = '<br>'.join("<a href=\"{href}\">{form}</a>".format(href=url, form=short_form) for short_form, url in docs)
        else:
            self._instruction = 'None'
            self._shortForm = 'None'

    @description.setter
    def description(self, desc_list):
        self._description = '<br>'.join(new_description for new_description in desc_list)

    @llil.setter
    def llil(self, llil_list):
        print("Setting LLIL")
        newText = ""
        for llil in llil_list:
            if llil is not None:
                tokens = llil.deref_tokens if hasattr(llil, 'deref_tokens') else llil.tokens
                newText += "{}: ".format(llil.instr_index)
                newText += ''.join(str(token) for token in tokens)
            else:
                newText += 'None'
            newText += '<br>'
        if(len(llil_list) > 0):
            self._LLIL = newText.strip()
        else:
            self._LLIL = 'None'

    @mlil.setter
    def mlil(self, mlil_list):
        newText = ""
        for mlil in mlil_list:
            if mlil is not None:
                tokens = mlil.deref_tokens if hasattr(mlil, 'deref_tokens') else mlil.tokens
                newText += (''.join(str(token) for token in tokens))
            else:
                newText += ('None')
            newText += '<br>'
        if(len(mlil_list) > 0):
            self._MLIL = newText.strip()
        else:
            self._MLIL = 'None'

    @state.setter
    def state(self, state_list):
        if state_list is not None:
            self._stateDisplay = '<br>'.join(state_list)
        else:
            self._stateDisplay = 'None'


def explain_window():
    global window
    # Creates a new window if it doesn't already exist
    if window is None:
        window = ExplanationWindow()
    return window
