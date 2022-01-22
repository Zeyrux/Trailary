from lib.Vocabulary import vocabs, remove_list, reload
from PyQt6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton
)


class AllVocabs(QMainWindow):
    def __init__(self):
        super().__init__()

        self.list_given = QListWidget()
        self.list_searched = QListWidget()

        for vocab in vocabs:
            self.list_given.addItem(
                remove_list(f"{vocab.lan_given:}: {vocab.given}")
            )
            self.list_searched.addItem(
                remove_list(f"{vocab.lan_searched}: {vocab.searched}")
            )

        self.layout_lists = QHBoxLayout()
        self.layout_lists.addWidget(self.list_given)
        self.layout_lists.addWidget(self.list_searched)

        self.button_language = QPushButton("Edit language")

        self.button_vocab = QPushButton("Edit vocab")

        self.button_reload = QPushButton("Reload vocabs")
        self.button_reload.clicked.connect(self.reload)

        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.addWidget(self.button_vocab)
        self.layout_buttons.addWidget(self.button_language)
        self.layout_buttons.addWidget(self.button_reload)

        self.widget_lists = QWidget()
        self.widget_lists.setLayout(self.layout_lists)

        self.widget_buttons = QWidget()
        self.widget_buttons.setLayout(self.layout_buttons)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget_lists)
        self.layout.addWidget(self.widget_buttons)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def reload(self):
        reload()
        self.list_given.clear()
        self.list_searched.clear()
        for vocab in vocabs:
            self.list_given.addItem(
                remove_list(f"{vocab.lan_given:}: {vocab.given}")
            )
            self.list_searched.addItem(
                remove_list(f"{vocab.lan_searched}: {vocab.searched}")
            )
