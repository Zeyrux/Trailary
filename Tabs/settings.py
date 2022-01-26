from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

show_dialogs = True


class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_dialogs = QPushButton("Dialogs: On")
        self.button_dialogs.clicked.connect(self.change_dialog)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_dialogs)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def change_dialog(self):
        global show_dialogs
        show_dialogs = False if show_dialogs else True
        print(show_dialogs)
        if show_dialogs:
            self.button_dialogs.setText("Dialogs: On")
        else:
            self.button_dialogs.setText("Dialogs: Off")
