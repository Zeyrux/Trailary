import os
import sys
import ctypes

from learn_page import Training
from add_vocabs_page import AddVocabs
from all_vocabs import AllVocabs
from Vocabulary import Vocab, read_vocab, save_vocab, get_random_vocab
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QPushButton,
                             QLineEdit,
                             QHBoxLayout,
                             QVBoxLayout,
                             QWidget,
                             QLabel,
                             QTabWidget,
                             QListWidget,)

APP_NAME = "Trailary"
STYLE = "Fusion"
SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)


class MainWindow(QMainWindow):

    is_fullscreen = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(800, 600)

        # trainer
        widget_training = Training().widget

        # add new vocabs
        widget_new_vocabs = AddVocabs().widget

        # all vocabs
        widget_all_vocabs = AllVocabs().widget

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.tabs.setMovable(True)

        self.tabs.addTab(widget_training, "learn")
        self.tabs.addTab(widget_new_vocabs, "add vocabs")
        self.tabs.addTab(widget_all_vocabs, "all vocabs")

        self.setCentralWidget(self.tabs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F11:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True


app = QApplication(sys.argv)
app.setStyle(STYLE)

window = MainWindow()
window.show()

app.exec()
