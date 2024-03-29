from pathlib import Path

from PySide6.QtGui import QImage
from binaryninjaui import SidebarWidgetType, Sidebar

from .explain import make_description
from .explainers import X86Explainer
from .gui import ExplanationWindow
from .util import debug_instruction

__all__ = [debug_instruction, make_description, X86Explainer]

root = Path(__file__).parent


class ExplainSidebarWidgetType(SidebarWidgetType):
    def __init__(self):
        # Icon is blackboard by lastspark from the Noun Project
        # https://thenounproject.com/term/blackboard/367906/
        icon = QImage(str(root.joinpath("icon.png")))
        SidebarWidgetType.__init__(self, icon, "Explain Instruction")

    def createWidget(self, frame, data):
        # This callback is called when a widget needs to be created for a given context. Different
        # widgets are created for each unique BinaryView. They are created on demand when the sidebar
        # widget is visible and the BinaryView becomes active.
        return ExplanationWindow("Explain Instruction", frame, data)


Sidebar.addSidebarWidgetType(ExplainSidebarWidgetType())
