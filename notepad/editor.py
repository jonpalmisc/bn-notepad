import binaryninjaui

try:
    from PySide6.QtWidgets import QPlainTextEdit, QWidget
except ImportError:
    from PySide2.QtWidgets import QPlainTextEdit, QWidget


class JMarkdownEditor(QPlainTextEdit):
    """Custom editor widget."""

    def __init__(self, parent: QWidget):
        QPlainTextEdit.__init__(self, parent)

        # Editor should use a monospace font
        self.setFont(binaryninjaui.getDefaultMonospaceFont())
