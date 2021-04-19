import binaryninjaui
from binaryninja import core_ui_enabled

if "qt_major_version" in dir(binaryninjaui) and binaryninjaui.qt_major_version == 6:
    from PySide6.QtCore import Qt
else:
    from PySide2.QtCore import Qt


from .notepad import docking
from .notepad.widget import NotepadDockWidget


if core_ui_enabled():
    docking.register_widget(
        NotepadDockWidget, "Notepad", Qt.RightDockWidgetArea, Qt.Vertical, False
    )
