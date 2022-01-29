from lib.CustomWidgets import get_styles
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

show_dialogs = True

STYLE = open("styles\\SettingsTab.css", "r").read()


class Settings(QMainWindow):
    def __init__(self, styles=[]):
        super().__init__()
        self.button_dialogs = QPushButton("Dialogs: On")
        self.button_dialogs.clicked.connect(self.change_dialog)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_dialogs)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setObjectName("MainWidget")

        styles.append(STYLE)
        self.setStyleSheet(get_styles(styles))
        
        self.setCentralWidget(self.widget)

    def change_dialog(self):
        global show_dialogs
        show_dialogs = False if show_dialogs else True
        if show_dialogs:
            self.button_dialogs.setText("Dialogs: On")
        else:
            self.button_dialogs.setText("Dialogs: Off")
