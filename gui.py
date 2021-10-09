import traceback
import typing

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QColor
from PySide6.QtWidgets import (
    QFrame,
)
from PySide6.QtWidgets import QVBoxLayout, QLabel
from binaryninja import (
    BinaryView,
    Architecture,
    log_error,
    LowLevelILInstruction,
    InstructionTextTokenType,
    ThemeColor,
    InstructionTextToken,
)
from binaryninjaui import (
    SidebarWidget,
    UIActionHandler,
    getTokenColor,
    getThemeColor,
    getMonospaceFont,
)

from .explain import explain_llil, fold_multi_il
from .util import (
    get_function_at,
    find_llil,
    find_lifted_il,
    inst_in_func,
    colorize,
    get_instruction,
)

from .explainers import explainer_for_architecture


def make_hline():
    out = QFrame()
    out.setFrameShape(QFrame.HLine)
    out.setFrameShadow(QFrame.Sunken)
    return out


class ExplanationWindow(SidebarWidget):
    """Displays a brief explanation of what an instruction does"""

    def __init__(self, name, _frame, bv: typing.Optional[BinaryView] = None):
        SidebarWidget.__init__(self, name)
        self.actionHandler = UIActionHandler()
        self.actionHandler.setupActionHandler(self)

        self.configured_arch = None
        self._bv = None
        self.arch_explainer = None

        # Configures configured_arch, _bv, and arch_explainer
        self.bv = bv

        self.colors = {t: getTokenColor(self, t) for t in InstructionTextTokenType}

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self.newline = "\n"

        self._label_font: QFont = QFont()
        self._mono_font: QFont = getMonospaceFont(self)
        self._mono_font_large: QFont = getMonospaceFont(self)
        self._mono_font_large.setPointSize(self._mono_font.pointSize() + 6)

        def make_label(text):
            label = QLabel(text)
            label.setFont(self._label_font)
            return label

        self._instruction = QLabel()
        self._instruction.setFont(self._mono_font_large)
        self._instruction.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._instruction.setWordWrap(True)
        self._layout.addWidget(self._instruction)

        self._layout.addWidget(make_hline())

        self._short_form_label = make_label("Short Form:")
        self._layout.addWidget(self._short_form_label)

        self._shortForm = QLabel()
        self._shortForm.setTextFormat(Qt.RichText)
        self._shortForm.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self._shortForm.setOpenExternalLinks(True)
        self._shortForm.setWordWrap(True)
        self._layout.addWidget(self._shortForm)

        self._layout.addWidget(make_hline())

        self._description_label = make_label("Description:")
        self._layout.addWidget(self._description_label)

        self._description = QLabel()
        self._description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._description.setWordWrap(True)
        self._layout.addWidget(self._description)

        self._layout.addWidget(make_hline())

        self._llil_label = make_label("Corresponding LLIL:")
        self._layout.addWidget(self._llil_label)

        self._LLIL = QLabel()
        self._LLIL.setFont(self._mono_font)
        self._LLIL.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._LLIL.setWordWrap(True)
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

    @property
    def short_form(self):
        return self._shortForm.text()

    @instruction.setter
    def instruction(self, instr: typing.Optional[str]):
        self._instruction.setText(str(instr))

    @description.setter
    def description(self, desc_list: typing.List[str]):
        self._description.setText("\n".join(desc_list))

    @llil.setter
    def llil(self, llil_list: typing.List[str]):
        print(llil_list)
        self._LLIL.setText("<br>".join(llil_list))

    @short_form.setter
    def short_form(self, new_short_form: typing.Optional[str]):
        self._shortForm.setText(str(new_short_form))

    @property
    def bv(self):
        return self._bv

    @bv.setter
    def bv(self, new_bv: typing.Optional[BinaryView]):
        self._bv = new_bv
        if self._bv is not None:
            self.configure_for_arch(self._bv.arch)

    @staticmethod
    def escape(in_str):
        return in_str

    def explain_instruction(self, addr):
        """Callback for the menu item that passes the information to the GUI"""

        # Get the relevant information for this address
        func = get_function_at(self.bv, addr)
        if func is None:
            return self.reset()
        instruction = get_instruction(self.bv, addr)

        with Atomic():
            self.instruction = (
                f"<font color={getThemeColor(ThemeColor.AddressColor).name()}>"
                f"{addr:^0{self.bv.arch.address_size}x}</font>:  "
                f"{''.join(colorize(self.colors, instruction))}"
            )

        with Atomic():
            docs = self.arch_explainer.get_doc_url(instruction)
            self.short_form = "\n".join(
                '<a href="{href}">{form}</a>'.format(href=url, form=short_form)
                for short_form, url in docs
            )

        self._description.setText("Generating description...")

        lifted_il_list = func.get_lifted_ils_at(addr)
        llil_list = func.get_llils_at(addr)

        with Atomic():
            self.llil = dereference_llil(llil_list, self.colors)

        with Atomic():
            self.description = make_description(
                self.bv, self.arch_explainer, instruction, lifted_il_list, llil_list
            )

    def reset(self):
        self.instruction = None
        self.short_form = None
        self.description = []
        self.llil = []

    def configure_for_arch(self, arch: Architecture):
        self.configured_arch = arch
        self.arch_explainer = explainer_for_architecture(arch)(self.bv)

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

    def notifyThemeChanged(self, *args, **kwargs):
        self.repaint()

    def notifyFontChanged(self, *args, **kwargs):
        # I don't know how to get a non-monospaced font from the Binja UI API
        self._label_font = QFont()
        self._mono_font: QFont = getMonospaceFont(self)
        self._mono_font_large: QFont = getMonospaceFont(self)
        self._mono_font_large.setPointSize(self._mono_font.pointSize() + 6)

        self._short_form_label.setFont(self._label_font)
        self._description_label.setFont(self._label_font)
        self._llil_label.setFont(self._label_font)

        self._instruction.setFont(self._mono_font_large)
        self._LLIL.setFont(self._mono_font)


class Atomic:
    """Suppresses all exceptions within the wrapped context"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value is not None:
            log_error(traceback.format_exc())
        return True


def make_description(bv, arch_explainer, instruction, lifted_il_list, llil_list):
    # Typically, we use the Low Level IL for parsing instructions. However, sometimes there isn't a corresponding
    # LLIL instruction (like for cmp), so in cases like that, we use the lifted IL, which is closer to the raw assembly
    parse_il = fold_multi_il(bv, llil_list if len(llil_list) > 0 else lifted_il_list)
    # Give the architecture submodule a chance to supply an explanation for this instruction that takes precedence
    # over the one generated via the LLIL
    (
        should_supersede,
        explanation_list,
    ) = arch_explainer.explain_instruction(instruction, lifted_il_list)
    return explanation_list + (
        [] if should_supersede else [explain_llil(bv, llil) for llil in parse_il]
    )


def dereference_llil(
    llil_list: typing.List[LowLevelILInstruction], color_map
) -> typing.List[str]:
    # TODO - fix dereferencing
    return list(
        "{}: ".format(llil.instr_index)
        + "".join(
            colorize(
                color_map,
                (
                    llil.tokens
                    if not hasattr(llil, "deref_tokens")
                    else llil.deref_tokens
                ),
            )
        )
        for llil in llil_list
        if llil is not None
    )
