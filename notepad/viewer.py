try:
    from PySide6.QtWidgets import QTextBrowser, QWidget
except ImportError:
    from PySide2.QtWidgets import QTextBrowser, QWidget

from .editor import JMarkdownEditor


class JMarkdownViewer(QTextBrowser):
    """Custom viwer widget which links to a JMarkdownEditor."""

    editor: JMarkdownEditor

    def __init__(self, parent: QWidget, editor: JMarkdownEditor):
        QTextBrowser.__init__(self, parent)

        self.editor = editor
        self.editor.textChanged.connect(self.on_editor_text_changed)

        self.setOpenLinks(True)
        self.setOpenExternalLinks(True)

    def on_editor_text_changed(self):
        """Update the viewer when the content of the linked editor changes."""

        self.setMarkdown(self.editor.toPlainText())
