import sys
import ctypes

from Tabs.learn_tab import get_tabs
from Tabs.add_vocabs_tab import AddVocabs
from Tabs.all_vocabs_tab import AllVocabs
from Tabs.settings_tab import Settings
from lib.Style import Style
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

APP_NAME = "Trailary"
STYLE_MAIN_WIDGET = open("styles\\MainWidget.css", "r").read()
STYLE_CUSTOM_LINE_EDIT = open("styles\\CustomLineEdit.css", "r").read()
STYLE_Q_BUTTON_PUSH = open("styles\\QPushButton.css", "r").read()
STYLE_Q_LABEL = open("styles\\QLabel.css", "r").read()
STYLE_Q_SCROLL_AREA = open("styles\\QScrollArea.css", "r").read()
STYLE_Q_GRID_LAYOUT = open("styles\\QGridLayout.css", "r").read()

STYLE_WINDOW = open("styles\\TrailaryMain.css", "r").read()
STYLE_APP = "Fusion"
SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)


class MainWindow(QMainWindow):
    is_fullscreen = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setBaseSize(400, 800)
        self.setMinimumSize(400, 800)

        # styles
        # learn
        learn_tabs_style = Style([
            STYLE_MAIN_WIDGET,
            STYLE_CUSTOM_LINE_EDIT,
            STYLE_Q_BUTTON_PUSH,
            STYLE_Q_LABEL
        ])
        # add vocabs
        add_vocabs_style = Style([
            STYLE_MAIN_WIDGET,
            STYLE_CUSTOM_LINE_EDIT,
            STYLE_Q_BUTTON_PUSH,
            STYLE_Q_LABEL
        ])
        # all vocabs
        all_vocabs_style = Style([
            STYLE_MAIN_WIDGET,
            STYLE_CUSTOM_LINE_EDIT,
            STYLE_Q_BUTTON_PUSH,
            STYLE_Q_LABEL,
            STYLE_Q_SCROLL_AREA,
            STYLE_Q_GRID_LAYOUT
        ])
        all_vocabs_style.change_font_size("CustomLineEdit", "20px")
        # settings
        settings_style = Style([
            STYLE_MAIN_WIDGET,
            STYLE_Q_BUTTON_PUSH
        ])

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)

        learn_tabs = get_tabs(learn_tabs_style)

        for tab in learn_tabs:
            self.tabs.addTab(
                tab.widget,
                f"{tab.language_given[0].upper() + tab.language_given[1:]} "
                f"to "
                f"{tab.language_search[0].upper() + tab.language_search[1:]}"
            )

        self.tabs.addTab(AddVocabs(add_vocabs_style), "Add vocabs")
        self.tabs.addTab(AllVocabs(all_vocabs_style), "All vocabs")
        self.tabs.addTab(Settings(settings_style), "Settings")

        self.setStyleSheet(STYLE_WINDOW)
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
app.setStyle(STYLE_APP)

window = MainWindow()
window.show()

app.exec()
