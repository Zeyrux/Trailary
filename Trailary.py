import os
import sys

from Vocabulary import Vocab, read_vocab, save_vocab
from PyQt6.QtCore import QSize, Qt
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setFixedSize(QSize(800, 600))

        # trainer
        layout_trainer = QVBoxLayout()
        layout_trainer.addWidget(QLabel("Text"))
        layout_trainer.addWidget(QLineEdit())

        widget_trainer = QWidget()
        widget_trainer.setLayout(layout_trainer)

        # add new vocabs
        layout_new_vocabs = QVBoxLayout()
        layout_new_vocabs.addWidget(QLabel("English:"))
        layout_new_vocabs.addWidget(QLineEdit())
        layout_new_vocabs.addWidget(QLabel("German:"))
        layout_new_vocabs.addWidget(QLineEdit())
        layout_new_vocabs.addWidget(QPushButton("Save"))

        widget_new_vocabs = QWidget()
        widget_new_vocabs.setLayout(layout_new_vocabs)

        # all vocabs
        widget_all_vocabs = QListWidget()
        widget_all_vocabs.addItem("Vocab1: German")
        widget_all_vocabs.addItem("Vocab2: German")
        widget_all_vocabs.addItem("Vocab3: German")
        widget_all_vocabs.addItem("Vocab4: German")
        widget_all_vocabs.addItem("Vocab5: German")

        # tabs
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)

        tabs.addTab(widget_trainer, "learn")
        tabs.addTab(widget_new_vocabs, "add vocabs")
        tabs.addTab(widget_all_vocabs, "all vocabs")

        self.setCentralWidget(tabs)


app = QApplication(sys.argv)
app.setStyle("Fusion")

window = MainWindow()
window.show()

app.exec()
