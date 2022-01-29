from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLineEdit,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout
)


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
    def __init__(self, title="INFO", message=""):
        super().__init__()
        self.setWindowTitle(title)

        self.button_exit = QPushButton("Exit")
        self.button_exit.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(message))
        self.layout.addWidget(self.button_exit)

        self.setLayout(self.layout)
        self.exec()
