from lib.Style import Style
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

show_dialogs = True


class SettingsTab(QMainWindow):
    def __init__(self, style=Style([])):
        super().__init__()
        self.button_dialogs = QPushButton("Dialogs: On")
        self.button_dialogs.clicked.connect(self.change_dialog)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_dialogs)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setObjectName("MainWidget")

        self.setStyleSheet(style.style)
        
        self.setCentralWidget(self.widget)

    def change_dialog(self):
        global show_dialogs
        show_dialogs = False if show_dialogs else True
        if show_dialogs:
            self.button_dialogs.setText("Dialogs: On")
        else:
            self.button_dialogs.setText("Dialogs: Off")
