from __future__ import print_function
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont

mlil_tooltip = """Often, several assembly instructions make up one MLIL instruction.
The MLIL instruction shown may not correspond to this instruction
alone, or this instruction may not have a direct MLIL equivalent."""

def make_hline():
    out =QtWidgets.QFrame()
    out.setFrameShape(QtWidgets.QFrame.HLine)
    out.setFrameShadow(QtWidgets.QFrame.Sunken)
    return out

def __None__(*args):
    return None, None

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

    @instruction.setter
    def instruction(self, instr):
        if instr is not None:
            short_form, url = self.get_doc_url(instr.tokens[0])
            self._instruction.setText(''.join(str(token) for token in instr.tokens).replace('    ', ' '))
            self._shortForm.setText("<a href=\"{href}\">{form}</a>".format(href=url, form=short_form))
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
            self.state_Display.setPlainText('None')
