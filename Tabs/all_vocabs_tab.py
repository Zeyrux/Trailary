import Tabs
import lib
from lib.Vocabulary import (
    Vocab,
    VocabPiece,
    edit_vocab,
    delete_vocab,
    reload,
    split_comma
)
from lib.CustomWidgets import CustomLineEdit, CustomDialog, CustomScrollArea
from lib.Style import Style
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QPushButton,
    QLabel
)


class AllVocabs(QMainWindow):
    def __init__(self, style=Style([])):
        super().__init__()

        self.scroll_area_vocabs = CustomScrollArea(
            alignment=Qt.AlignmentFlag.AlignCenter
        )

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

    def set_scroll_area(self) -> CustomScrollArea:
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
                text=vocab.given_str,
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
                text=vocab.searched_str,
                alignment=Qt.AlignmentFlag.AlignCenter
            ), i, 3)
            line_label = QLabel(str(vocab.line))
            line_label.setObjectName(str(i))
            layout_vocabs.addWidget(line_label, i, 4)

        widget_vocabs = QWidget()
        widget_vocabs.setObjectName("QGridLayout")
        widget_vocabs.setLayout(layout_vocabs)

        self.scroll_area_vocabs.setWidget(widget_vocabs)

    def edit_vocab(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            vocab_widgets: list[QObject]
            children = self.scroll_area_vocabs.findChildren(
                QWidget, "QGridLayout"
            )[0]
            for child in children.children()[1:]:
                if child.hasFocus():
                    vocab_widgets = self.scroll_area_vocabs.findChildren(
                        QWidget, child.objectName()
                    )
                    break
            given_pieces = []
            given = split_comma(vocab_widgets[1].text())
            for piece in given:
                pieces = piece.split(" ")
                präfix = ""
                for i in range(len(pieces) - 1):
                    präfix += pieces[i] + " "
                präfix = präfix[:len(präfix)-1]
                given_pieces.append(VocabPiece(pieces[-1], präfix=präfix))

            searched_pieces = []
            searched = split_comma(vocab_widgets[3].text())
            for piece in searched:
                pieces = piece.split(" ")
                präfix = ""
                for i in range(len(pieces) - 1):
                    präfix += pieces[i] + " "
                präfix = präfix[:len(präfix) - 1]
                searched_pieces.append(VocabPiece(pieces[-1], präfix=präfix))

            vocab = Vocab(
                vocab_widgets[0].text(),
                given_pieces,
                vocab_widgets[2].text(),
                searched_pieces,
                int(vocab_widgets[4].text())
            )
            edit_vocab(vocab)
            CustomDialog(message="Vocab changed")

    def delete_vocab(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            try:
                line = int(self.line_edit_delete.text())
                delete_vocab(line)
                CustomDialog(message="Deleted line")
            except ValueError:
                CustomDialog(
                    title="Warning",
                    message="Please enter the line number",
                    ignore_settings=True
                )
