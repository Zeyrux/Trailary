from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QLineEdit


def empty(_):
    pass


class CustomLineEdit(QLineEdit):
    def __init__(
            self,
            key_press=empty,
            key_release=empty
    ):
        super().__init__()
        self.key_press = key_press
        self.key_release = key_release

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.key_press(event)
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        super().keyReleaseEvent(event)
        self.key_release(event)
        event.accept()