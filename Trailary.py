import sys
import ctypes

from Tabs.learn_page import Training, get_tabs
from Tabs.add_vocabs_page import AddVocabs
from Tabs.all_vocabs import AllVocabs
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

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

        # add new vocabs
        widget_new_vocabs = AddVocabs()

        # all vocabs
        widget_all_vocabs = AllVocabs()

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)

        learn_tabs = get_tabs()

        for tab in learn_tabs:
            self.tabs.addTab(
                tab.widget,
                f"{tab.language_given} to {tab.language_search}"
            )

        self.tabs.addTab(widget_new_vocabs, "add vocabs")
        self.tabs.addTab(widget_all_vocabs, "all vocabs")

        self.setCentralWidget(self.tabs)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
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
