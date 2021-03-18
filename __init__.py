from PySide2.QtCore import Qt

from .notepad import docking
from .notepad.widget import NotepadDockWidget


docking.register_widget(
    NotepadDockWidget, "Notepad", Qt.RightDockWidgetArea, Qt.Vertical, False
)
