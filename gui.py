import traceback
import typing
from importlib import import_module

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import (
    QFrame,
)
from PySide6.QtWidgets import QVBoxLayout, QLabel
from binaryninja import BinaryView, Architecture, log_error
from binaryninjaui import SidebarWidget, UIActionHandler

from .explain import explain_llil, fold_multi_il
from .util import *
from .util import (
    get_function_at,
    find_llil,
    find_lifted_il,
    inst_in_func,
    dereference_symbols,
)

arch_specific_explanations = {}
doc_urls = {}
_remappings = {
    "arm": "ual",
    "thumb2": "ual",
    "6502": "asm6502",
}

for arch in Architecture:
    for supported in (
        "x86",
        "mips",
        "aarch64",
        "arm",
        "thumb2",
        "6502",
        "msp430",
        "powerpc",
    ):
        if supported in arch.name:
            doc_urls[arch.name] = import_module(
                f".{_remappings.get(supported, supported)}",
                package="binja_explain_instruction",
            ).get_doc_url
            arch_specific_explanations[arch.name] = import_module(
                f".{_remappings.get(supported, supported)}.explain",
                package="binja_explain_instruction",
            ).arch_explain_instruction


def make_hline():
    out = QFrame()
    out.setFrameShape(QFrame.HLine)
    out.setFrameShadow(QFrame.Sunken)
    return out


def no_documentation_available(*_args):
    return [
        (
            "No documentation available",
            "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md",
        )
    ]


def no_arch_specific_explanations_available(*_args):
    return False, ["Architecture-specific explanations unavailable"]


class ExplanationWindow(SidebarWidget):
    """Displays a brief explanation of what an instruction does"""

    def __init__(self, name, _frame, bv: typing.Optional[BinaryView] = None):
        SidebarWidget.__init__(self, name)
        self.actionHandler = UIActionHandler()
        self.actionHandler.setupActionHandler(self)

        self.configured_arch = None
        self._bv = None

        self.bv = bv

        self.architecture_specific_explanation_function = (
            no_arch_specific_explanations_available
        )
        self.get_doc_url = no_documentation_available

        self._layout = QVBoxLayout(self)

        self.newline = "\n"

        self._labelFont = QFont()
        self._labelFont.setPointSize(12)

        self._labelA = QLabel()
        self._labelA.setText("Instruction:")
        self._labelA.setFont(self._labelFont)
        self._layout.addWidget(self._labelA)

        self._instruction = QLabel()
        self._instruction.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._instruction.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._instruction)

        self._layout.addWidget(make_hline())

        self._labelF = QLabel()
        self._labelF.setText("Short Form:")
        self._labelF.setFont(self._labelFont)
        self._layout.addWidget(self._labelF)

        self._shortForm = QLabel()
        self._shortForm.setTextFormat(Qt.RichText)
        self._shortForm.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self._shortForm.setOpenExternalLinks(True)
        self._layout.addWidget(self._shortForm)

        self._layout.addWidget(make_hline())

        self._labelB = QLabel()
        self._labelB.setText("Description:")
        self._labelB.setFont(self._labelFont)
        self._layout.addWidget(self._labelB)

        self._description = QLabel()
        self._description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._description)

        self._layout.addWidget(make_hline())

        self._labelC = QLabel()
        self._labelC.setText("Corresponding LLIL:")
        self._labelC.setFont(self._labelFont)
        self._layout.addWidget(self._labelC)

        self._LLIL = QLabel()
        self._LLIL.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self._LLIL.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._layout.addWidget(self._LLIL)

    @property
    def instruction(self):
        return self._instruction.text()

    @property
    def description(self):
        return self._description.text()

    @property
    def llil(self):
        return self._LLIL.text()

    @instruction.setter
    def instruction(self, instr):
        i, s = parse_instruction(self, instr)
        self._instruction.setText(i)
        self._shortForm.setText(s)

    @description.setter
    def description(self, desc_list):
        self._description.setText(parse_description(self, desc_list))

    @llil.setter
    def llil(self, llil_list):
        self._LLIL.setText(parse_llil(self, llil_list))

    @property
    def bv(self):
        return self._bv

    @bv.setter
    def bv(self, new_bv: typing.Optional[BinaryView]):
        self._bv = new_bv
        if self._bv is not None:
            self.configure_for_arch(self._bv.arch)

    def escape(self, in_str):
        return in_str

    def explain_instruction(self, addr):
        """Callback for the menu item that passes the information to the GUI"""
        # Get the relevant information for this address
        func = get_function_at(self.bv, addr)
        if func is None:
            return self.reset()

        instruction = inst_in_func(func, addr)
        lifted_il_list = find_lifted_il(func, addr)
        llil_list = find_llil(func, addr)

        # Typically, we use the Low Level IL for parsing instructions. However, sometimes there isn't a corresponding
        # LLIL instruction (like for cmp), so in cases like that, we use the lifted IL, which is closer to the raw assembly
        parse_il = fold_multi_il(
            self.bv, llil_list if len(llil_list) > 0 else lifted_il_list
        )

        # Give the architecture submodule a chance to supply an explanation for this instruction that takes precedence
        # over the one generated via the LLIL
        (
            should_supersede_llil,
            explanation_list,
        ) = self.architecture_specific_explanation_function(
            self.bv, instruction, lifted_il_list
        )

        # Display the raw instruction
        try:
            self.instruction = "{addr}:  {inst}".format(
                addr=hex(addr).replace("L", ""), inst=instruction
            )
        except Exception:
            log_error(traceback.format_exc())

        if len(explanation_list) > 0:
            if should_supersede_llil:
                # If we got an architecture-specific explanation and it should supersede the LLIL, use that
                self.description = [explanation for explanation in explanation_list]
            else:
                # Otherwise, just prepend the arch-specific explanation to the LLIL explanation
                self.description = [explanation for explanation in explanation_list] + [
                    explain_llil(self.bv, llil) for llil in (parse_il)
                ]
        else:
            # By default, we just use the LLIL explanation
            # We append the line number if we're displaying a conditional.
            self.description = [explain_llil(self.bv, llil) for llil in parse_il]

        # Display the  LLIL, dereferencing anything that looks like a hex number into a symbol if possible
        self.llil = (
            llil_list  # [dereference_symbols(self.bv, llil) for llil in llil_list]
        )

    def reset(self):
        self.instruction = None
        self.description = []
        self.llil = []

    def configure_for_arch(self, arch: Architecture):
        self.configured_arch = arch
        self.architecture_specific_explanation_function = (
            arch_specific_explanations.get(
                arch.name, no_arch_specific_explanations_available
            )
        )
        self.get_doc_url = doc_urls.get(arch.name, no_documentation_available)

    def notifyOffsetChanged(self, offset):
        self.explain_instruction(offset)

    def notifyViewChanged(self, view_frame):
        if view_frame is None:
            self.bv = None
        else:
            view = view_frame.getCurrentViewInterface()
            self.bv = view.getData()

    def contextMenuEvent(self, event):
        self.m_contextMenuManager.show(self.m_menu, self.actionHandler)
