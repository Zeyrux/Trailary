import Tabs
import lib
from lib.Vocabulary import (
    remove_list,
    Vocab,
    edit_vocab,
    delete_vocab,
    reload
)
from lib.CustomWidgets import CustomLineEdit, CustomDialog
from lib.Style import Style
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QWidget,
    QPushButton,
    QLabel
)


class AllVocabs(QMainWindow):
    def __init__(self, style=Style([])):
        super().__init__()

        self.scroll_area_vocabs = QScrollArea()

        self.button_reload = QPushButton("Reload vocabs")
        self.button_reload.clicked.connect(self.reload)

        self.line_edit_delete = CustomLineEdit(
            key_release=self.delete_vocab,
            placeholder="vocab line, that should be deledet",
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area_vocabs)
        self.layout.addWidget(self.line_edit_delete)
        self.layout.addWidget(self.button_reload)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setObjectName("MainWidget")
        self.widget.setStyleSheet(style.style)

        self.set_scroll_area()
        self.setCentralWidget(self.widget)

    def reload(self):
        reload()
        self.set_scroll_area()

    def set_scroll_area(self) -> QScrollArea:
        layout_vocabs = QGridLayout()
        for i, vocab in enumerate(lib.Vocabulary.vocabs):
            layout_vocabs.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=vocab.lan_given,
                alignment=Qt.AlignmentFlag.AlignCenter
            ), i, 0)
            layout_vocabs.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=remove_list(vocab.given),
                alignment=Qt.AlignmentFlag.AlignCenter
            ), i, 1)
            layout_vocabs.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=vocab.lan_searched,
                alignment=Qt.AlignmentFlag.AlignCenter
            ), i, 2)
            layout_vocabs.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=remove_list(vocab.searched),
                alignment=Qt.AlignmentFlag.AlignCenter
            ), i, 3)
            line_label = QLabel(str(vocab.line))
            line_label.setObjectName(str(i))
            layout_vocabs.addWidget(line_label, i, 4)

        widget_vocabs = QWidget()
        widget_vocabs.setObjectName("Table")
        widget_vocabs.setLayout(layout_vocabs)

        self.scroll_area_vocabs.setWidget(widget_vocabs)

    def edit_vocab(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            vocab_widgets: list[QObject]
            children = self.scroll_area_vocabs.findChildren(
                QWidget, "Table"
            )[0]
            for child in children.children()[1:]:
                if child.hasFocus():
                    vocab_widgets = self.scroll_area_vocabs.findChildren(
                        QWidget, child.objectName()
                    )
            vocab = Vocab(
                vocab_widgets[0].text(),
                vocab_widgets[1].text().split(", "),
                vocab_widgets[2].text(),
                vocab_widgets[3].text().split(", "),
                int(vocab_widgets[4].text())
            )
            edit_vocab(vocab)
            if Tabs.settings_tab.show_dialogs:
                CustomDialog(message="Vocab changed")

    def delete_vocab(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            try:
                line = int(self.line_edit_delete.text())
                delete_vocab(line)
                print(Tabs.settings_tab.show_dialogs)
                if Tabs.settings_tab.show_dialogs:
                    CustomDialog(message="Deleted line")
            except ValueError:
                CustomDialog(
                    title="Warning",
                    message="Please enter the line number"
                )
