from PySide2.QtWidgets import QPlainTextEdit, QWidget

from .highlighter import JMarkdownHighlighter


class JMarkdownEditor(QPlainTextEdit):
    """Custom editor widget which integrates Markdown highlighting."""

    highlighter: JMarkdownHighlighter

    def __init__(self, parent: QWidget):
        QPlainTextEdit.__init__(self, parent)
        self.highlighter = JMarkdownHighlighter(
            self.document(), self.fontInfo().pointSize()
        )
