from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLineEdit,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QBoxLayout
)
import Tabs


def empty(_):
    pass


class CustomLineEdit(QLineEdit):
    def __init__(
            self,
            key_press=empty,
            key_release=empty,
            object_name="",
            placeholder="",
            text="",
            alignment=Qt.AlignmentFlag.AlignLeft
    ):
        super().__init__()
        self.key_press = key_press
        self.key_release = key_release
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder)
        self.setText(text)
        self.setAlignment(alignment)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.key_press(event)
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        super().keyReleaseEvent(event)
        self.key_release(event)
        event.accept()


class CustomDialog(QDialog):
    def __init__(self, title="INFO", message="", ignore_settings=False):
        if Tabs.settings_tab.show_dialogs and not ignore_settings:
            return
        super().__init__()
        self.setWindowTitle(title)

        self.button_exit = QPushButton("Exit")
        self.button_exit.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(message))
        self.layout.addWidget(self.button_exit)

        self.setLayout(self.layout)
        self.exec()


class CustomScrollArea(QScrollArea):
    def __init__(self, alignment=Qt.AlignmentFlag.AlignLeft):
        super().__init__()
        self.setAlignment(alignment)


class CustomPushButton(QPushButton):

    is_focused = False

    def __init__(
            self,
            text="",
            color_unfocus="rgb(105, 17, 5)",
            color_focus="rgb(41, 112, 35)"
    ):
        super().__init__()

        self.color_unfocus = color_unfocus
        self.color_focus = color_focus

        self.setText(text)

    def unfocus(self):
        self.setStyleSheet(f"background: {self.color_unfocus};")
        self.is_focused = False

    def focus(self):
        self.setStyleSheet(f"background: {self.color_focus};")
        self.is_focused = True

    def change_focus(self):
        if self.is_focused:
            self.unfocus()
        else:
            self.focus()


class SteerGrid:
    def __init__(self, grid: QBoxLayout):
        pass
