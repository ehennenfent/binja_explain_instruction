from __future__ import print_function
import sys
if (sys.platform == 'win32'):
    sys.path.append("C:\\Python27\\lib\\site-packages")

from PyQt5.QtWidgets import QApplication, QMainWindow, qApp
from PyQt5.QtCore import QCoreApplication

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont

app = QApplication.instance()
if app is None:
    app = QCoreApplication.instance()
if app is None:
    app = qApp
try:
    main_window = [x for x in app.allWidgets() if x.__class__ is QMainWindow][0]
except IndexError:
    raise Exception("Could not attach to main window!")

mlil_tooltip = """Often, several assembly instructions make up one MLIL instruction.
The MLIL instruction shown may not correspond to this instruction
alone, or this instruction may not have a direct MLIL equivalent."""

def make_hline():
    out = QtWidgets.QFrame()
    out.setFrameShape(QtWidgets.QFrame.HLine)
    out.setFrameShadow(QtWidgets.QFrame.Sunken)
    return out

def __None__(*args):
    return [("No documentation available", "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md")]

class ExplanationWindow(QtWidgets.QWidget):
    """ Displays a brief explanation of what an instruction does """
    def __init__(self):
        super(ExplanationWindow, self).__init__()
        self.setWindowTitle("Explain Instruction")
        self.setLayout(QtWidgets.QVBoxLayout())
        self._layout = self.layout()

        self._labelFont = QFont()
        self._labelFont.setPointSize(12)

        self._labelA = QtWidgets.QLabel()
        self._labelA.setText("Instruction:")
        self._labelA.setFont(self._labelFont)
        self._layout.addWidget(self._labelA)

        self._instruction = QtWidgets.QLabel()
        self._instruction.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._instruction.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._instruction)

        self._layout.addWidget(make_hline())

        self._labelF = QtWidgets.QLabel()
        self._labelF.setText("Short Form:")
        self._labelF.setFont(self._labelFont)
        self._layout.addWidget(self._labelF)

        self._shortForm = QtWidgets.QLabel()
        self._shortForm.setTextFormat(Qt.RichText)
        self._shortForm.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self._shortForm.setOpenExternalLinks(True)
        self._layout.addWidget(self._shortForm)

        self._layout.addWidget(make_hline())

        self._labelB = QtWidgets.QLabel()
        self._labelB.setText("Description:")
        self._labelB.setFont(self._labelFont)
        self._layout.addWidget(self._labelB)

        self._description = QtWidgets.QLabel()
        self._description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._description)

        self._layout.addWidget(make_hline())

        self._labelC = QtWidgets.QLabel()
        self._labelC.setText("Equivalent LLIL:")
        self._labelC.setFont(self._labelFont)
        self._layout.addWidget(self._labelC)

        self._LLIL = QtWidgets.QLabel()
        self._LLIL.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._LLIL.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._LLIL)

        self._layout.addWidget(make_hline())

        self._labelD = QtWidgets.QLabel()
        self._labelD.setText("Equivalent* MLIL:")
        self._labelD.setToolTip(mlil_tooltip)
        self._labelD.setFont(self._labelFont)
        self._layout.addWidget(self._labelD)

        self._MLIL = QtWidgets.QLabel()
        self._MLIL.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._MLIL.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._MLIL)

        self._layout.addWidget(make_hline())

        self._labelG = QtWidgets.QLabel()
        self._labelG.setText("Flag Operations:")
        self._labelG.setFont(self._labelFont)
        self._layout.addWidget(self._labelG)

        self._flags = QtWidgets.QLabel()
        self._flags.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._flags)

        self._layout.addWidget(make_hline())

        self._labelE = QtWidgets.QLabel()
        self._labelE.setText("Instruction State:")
        self._labelE.setFont(self._labelFont)
        self._layout.addWidget(self._labelE)

        self._stateDisplay = QtWidgets.QTextBrowser()
        self._stateDisplay.setOpenLinks(False)
        self._stateDisplay.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._layout.addWidget(self._stateDisplay)

        self.setObjectName('Explain_Window')

        self.get_doc_url = __None__

    @property
    def instruction(self):
        return self._instruction.text()

    @property
    def description(self):
        return self._description.text()

    @property
    def llil(self):
        return self._LLIL.text()

    @property
    def mlil(self):
        return self._MLIL.text()

    @property
    def state(self):
        return self._stateDisplay.toPlainText()

    @property
    def flags(self):
        return self._flags.text()

    @instruction.setter
    def instruction(self, instr):
        if instr is not None:
            docs = self.get_doc_url(instr.split(' '))
            self._instruction.setText(instr.replace('    ', ' '))
            self._shortForm.setText('<br>'.join("<a href=\"{href}\">{form}</a>".format(href=url, form=short_form) for short_form, url in docs))
        else:
            self._instruction.setText('None')
            self._shortForm.setText('None')

    @description.setter
    def description(self, desc_list):
        self._description.setText('\n'.join(new_description for new_description in desc_list))

    @llil.setter
    def llil(self, llil_list):
        newText = ""
        for llil in llil_list:
            if llil is not None:
                tokens = llil.deref_tokens if hasattr(llil, 'deref_tokens') else llil.tokens
                newText += "{}: ".format(llil.instr_index)
                newText += ''.join(str(token) for token in tokens)
            else:
                newText += 'None'
            newText += '\n'
        if(len(llil_list) > 0):
            self._LLIL.setText(newText.strip())
        else:
            self._LLIL.setText('None')

    @mlil.setter
    def mlil(self, mlil_list):
        newText = ""
        for mlil in mlil_list:
            if mlil is not None:
                tokens = mlil.deref_tokens if hasattr(mlil, 'deref_tokens') else mlil.tokens
                newText += (''.join(str(token) for token in tokens))
            else:
                newText += ('None')
            newText += '\n'
        if(len(mlil_list) > 0):
            self._MLIL.setText(newText.strip())
        else:
            self._MLIL.setText('None')

    @state.setter
    def state(self, state_list):
        if state_list is not None:
            self._stateDisplay.setPlainText('\n'.join(state_list))
        else:
            self._stateDisplay.setPlainText('None')

    @flags.setter
    def flags(self, tuple_list_list):
        out = ""
        counter = 0
        for f_read, f_written in tuple_list_list:
            if len(f_read) > 0:
                out += ("({})".format(counter) if len(tuple_list_list) > 1 else "") + "Reads: " + ', '.join(f_read) + '\n'
            if len(f_written) > 0:
                out += ("({})".format(counter) if len(tuple_list_list) > 1 else "") + "Writes: " + ', '.join(f_written) + '\n'
            out += '\n'
            counter += 1
        out = out.strip()
        out = "None" if out == "" else out
        self._flags.setText(out)

def explain_window():
    global main_window
    # Creates a new window if it doesn't already exist
    if not hasattr(main_window, 'explain_window'):
        main_window.explain_window = ExplanationWindow()

    return main_window.explain_window
