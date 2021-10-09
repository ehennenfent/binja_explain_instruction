from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QImage, QPainter, QFont, QColor
from binaryninjaui import SidebarWidgetType, Sidebar, getDefaultMonospaceFont

from .gui import ExplanationWindow, make_description
from .util import debug_instruction
from .explainers import X86Explainer

__all__ = [debug_instruction, make_description, X86Explainer]


class ExplainSidebarWidgetType(SidebarWidgetType):
    def __init__(self):
        # Sidebar icons are 28x28 points. Should be at least 56x56 pixels for
        # HiDPI display compatibility. They will be automatically made theme
        # aware, so you need only provide a grayscale image, where white is
        # the color of the shape.
        icon = QImage(56, 56, QImage.Format_RGB32)
        icon.fill(0)

        self.font: QFont = getDefaultMonospaceFont()
        self.font.setPointSize(56)

        p = QPainter()
        p.begin(icon)
        p.setFont(self.font)
        p.setPen(QColor(255, 255, 255, 255))
        p.drawText(QRectF(0, 0, 56, 56), Qt.AlignCenter, "E")
        p.end()

        SidebarWidgetType.__init__(self, icon, "Explain Instruction")

    def createWidget(self, frame, data):
        # This callback is called when a widget needs to be created for a given context. Different
        # widgets are created for each unique BinaryView. They are created on demand when the sidebar
        # widget is visible and the BinaryView becomes active.
        return ExplanationWindow("Explain Instruction", frame, data)


Sidebar.addSidebarWidgetType(ExplainSidebarWidgetType())
