import binaryninjaui

if "qt_major_version" in dir(binaryninjaui) and binaryninjaui.qt_major_version == 6:
    from PySide6.QtCore import Qt
else:
    from PySide2.QtCore import Qt


from .notepad import docking
from .notepad.widget import NotepadDockWidget


docking.register_widget(
    NotepadDockWidget, "Notepad", Qt.RightDockWidgetArea, Qt.Vertical, False
)
