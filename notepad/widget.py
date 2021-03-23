from typing import Optional

from binaryninja import BinaryView
from binaryninjaui import DockContextHandler

try:
    from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
    from PySide6.QtCore import QTimer
except ImportError:
    from PySide2.QtWidgets import QWidget, QTextEdit, QVBoxLayout
    from PySide2.QtCore import QTimer

from .editor import JMarkdownEditor

# A "unique" metadata key is used to store the user's notes in attempt to avoid
# collisions with other plugins using the metadata API.
METADATA_KEY = "92f8c608-notepad-11078da3f6fd"


class NotepadDockWidget(QWidget, DockContextHandler):
    """
    NotepadDockWidget is the - you guessed it - notepad dock widget. It is
    responsible for saving and restoring the user's notes, and providing the
    user an interface to edit their notes from.
    """

    # The actual editor widget.
    editor: JMarkdownEditor

    # Timer for auto-saving.
    save_timer: QTimer

    # The currently focused BinaryView.
    bv: Optional[BinaryView] = None

    def __init__(self, parent: QWidget, name: str, bv: Optional[BinaryView]):
        """
        Initialize a new NotepadDockWidget.

        :param parent: the QWidget to parent this NotepadDockWidget to
        :param name: the name to register the dock widget under
        :param bv: the currently focused BinaryView (may be None)
        """

        self.bv = bv

        QWidget.__init__(self, parent)
        DockContextHandler.__init__(self, self, name)

        # Set up the save timer to save the current notepad content on timeout.
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(lambda: self.store_notes())

        # Initialize the editor and set up the text changed callback.
        self.editor = JMarkdownEditor(self)
        self.editor.textChanged.connect(self.on_editor_text_changed)

        # Create a simple layout for the editor and set it as the root layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        self.setLayout(layout)

        # Probably does nothing since there should be no BV when the program
        # starts, but needs confirmation, so here it will stay.
        self.query_notes()

    def on_editor_text_changed(self):
        """
        Callback triggered when the editor's text changes.

        Used is to start the save timer, which will automatically save the
        user's notes after 1 second of typing inactivity.
        """

        self.save_timer.start(1000)

    def on_binary_view_changed(self, new_bv: BinaryView):
        """
        Callback triggered when the focused BinaryView changes.

        Used to save the notes of the old BinaryView and load the stored notes
        from the new BinaryView, if there are any.
        """

        # Do nothing if we have no BinaryView, which might happen at startup?
        if self.bv is not None:
            self.store_notes()

        # Update the internal BinaryView reference to point to the new
        # BinaryView, and attempt to load the notes stored in it. If there is no
        # new BinaryView, remove the reference to the old one.
        if new_bv is None:
            self.bv = None
        else:
            self.bv = new_bv
            self.query_notes()

    def query_notes(self):
        """
        Attempt to retrieve the saved notes from the database. Will do nothing
        if there is no active BinaryView.
        """

        # Do nothing if we have no BinaryView, which might happen at startup?
        if self.bv is None:
            pass

        # Attempt to access the notes stored in the database metadata. Will
        # throw a KeyError if this is a brand new database.
        try:
            notes = self.bv.query_metadata(METADATA_KEY)
            self.editor.setPlainText(notes)
        except KeyError:
            self.editor.setPlainText("")

    def store_notes(self):
        """
        Attempt to store the current notes in the database. Will do nothing if
        there is no active BinaryView.
        """

        # Do nothing if we have no BinaryView, which might happen at startup?
        if self.bv is None:
            pass

        # Store the notes in the metadata of the database.
        notes = self.editor.toPlainText()
        self.bv.store_metadata(METADATA_KEY, notes)

    # -- Binary Ninja UI callbacks (camelCase shenanigans warning) --

    # Should the notepad be visible? Helps with automatically hiding the notepad
    # when it is not needed.
    def shouldBeVisible(self, vf):
        return vf is not None

    # Triggered when a view changes, vf is a ViewFrame.
    def notifyViewChanged(self, vf):
        self.on_binary_view_changed(vf.getCurrentViewInterface().getData())
