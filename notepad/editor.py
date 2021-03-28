import binaryninjaui

if "qt_major_version" in dir(binaryninjaui) and binaryninjaui.qt_major_version == 6:
    from PySide6.QtWidgets import QPlainTextEdit, QWidget
else:
    from PySide2.QtWidgets import QPlainTextEdit, QWidget


class JMarkdownEditor(QPlainTextEdit):
    """Custom editor widget."""

    def __init__(self, parent: QWidget):
        QPlainTextEdit.__init__(self, parent)

        # Editor should use a monospace font
        self.setFont(binaryninjaui.getDefaultMonospaceFont())
