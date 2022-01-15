from lib.Vocabulary import get_random_vocab
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class Training(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(get_random_vocab().vocab))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QPushButton("Help!"))

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
