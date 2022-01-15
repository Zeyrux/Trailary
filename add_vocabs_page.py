from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton
)


class AddVocabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("English:"))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QLabel("German:"))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QPushButton("Save"))

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
