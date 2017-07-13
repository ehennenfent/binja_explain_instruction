from __future__ import print_function
from binaryninja import show_message_box
from cgi import escape

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
        if instr is not None:
            docs = self.get_doc_url(instr.split(' '))
            self._instruction = escape(instr.replace('    ', ' '))
            self._shortForm = '<br>'.join("<a href=\"{href}\">{form}</a>".format(href=url, form=escape(short_form)) for short_form, url in docs)
        else:
            self._instruction = 'None'
            self._shortForm = 'None'

    @description.setter
    def description(self, desc_list):
        self._description = '<br>'.join(escape(new_description) for new_description in desc_list)

    @llil.setter
    def llil(self, llil_list):
        newText = ""
        for llil in llil_list:
            if llil is not None:
                tokens = llil.deref_tokens if hasattr(llil, 'deref_tokens') else llil.tokens
                newText += "{}: ".format(llil.instr_index)
                newText += ''.join(escape(str(token)) for token in tokens)
            else:
                newText += 'None'
            newText += '<br>'
        if(len(llil_list) > 0):
            self._LLIL = newText.strip('<br>')
        else:
            self._LLIL = 'None'

    @mlil.setter
    def mlil(self, mlil_list):
        newText = ""
        for mlil in mlil_list:
            if mlil is not None:
                tokens = mlil.deref_tokens if hasattr(mlil, 'deref_tokens') else mlil.tokens
                newText += (''.join(escape(str(token)) for token in tokens))
            else:
                newText += ('None')
            newText += '<br>'
        if(len(mlil_list) > 0):
            self._MLIL = newText.strip('<br>')
        else:
            self._MLIL = 'None'

    @state.setter
    def state(self, state_list):
        if state_list is not None:
            self._stateDisplay = '<br>'.join(escape(state) for state in state_list)
        else:
            self._stateDisplay = 'None'

    @flags.setter
    def flags(self, tuple_list_list):
        out = ""
        counter = 0
        for f_read, f_written in tuple_list_list:
            if len(f_read) > 0:
                out += ("({}) ".format(counter) if len(tuple_list_list) > 1 else "") + "Reads: " + ', '.join(f_read) + '\n'
            if len(f_written) > 0:
                out += ("({}) ".format(counter) if len(tuple_list_list) > 1 else "") + "Writes: " + ', '.join(f_written) + '\n'
            out += '\n'
            counter += 1
        out = out.strip()
        out = "None" if out == "" else out
        self._flags = (out)


def explain_window():
    global window
    # Creates a new window if it doesn't already exist
    if window is None:
        window = ExplanationWindow()
    return window
