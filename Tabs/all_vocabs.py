from lib.Vocabulary import vocabs, remove_list, Vocab, edit_vocab, copy_vocab
from lib.CustomWidgets import CustomLineEdit
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QPushButton,
    QLabel
)


class AllVocabs(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scroll_area_vocabs = QScrollArea()
        self.set_scroll_area()

        self.button_reload = QPushButton("Reload vocabs")
        self.button_reload.clicked.connect(self.reload)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area_vocabs)
        self.layout.addWidget(self.button_reload)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def reload(self):
        self.set_scroll_area()

    def set_scroll_area(self) -> QScrollArea:
        layout_vocabs = QVBoxLayout()
        for i, vocab in enumerate(vocabs):
            layout_vocab = QHBoxLayout()
            layout_vocab.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=vocab.lan_given
            ))
            layout_vocab.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=remove_list(vocab.given)
            ))
            layout_vocab.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=vocab.lan_searched
            ))
            layout_vocab.addWidget(CustomLineEdit(
                key_release=self.edit_vocab,
                object_name=str(i),
                text=remove_list(vocab.searched)
            ))
            line_label = QLabel(str(vocab.line))
            line_label.setObjectName(str(i))
            layout_vocab.addWidget(line_label)
            widget = QWidget()
            widget.setLayout(layout_vocab)
            layout_vocabs.addWidget(widget)

        widget_vocabs = QWidget()
        widget_vocabs.setObjectName("object")
        widget_vocabs.setLayout(layout_vocabs)

        self.scroll_area_vocabs.setWidget(widget_vocabs)

    def edit_vocab(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return:
            vocab_widgets: list[QObject]
            children = self.scroll_area_vocabs.findChildren(
                QWidget, "object"
            )[0]
            has_found_focus = False
            for child in children.children()[1:]:
                if has_found_focus:
                    break
                for line_edit in child.children()[1:]:
                    if line_edit.hasFocus():
                        vocab_widgets = self.scroll_area_vocabs.findChildren(
                            QWidget, line_edit.objectName()
                        )
                        has_found_focus = True
                        break
            vocab = Vocab(
                vocab_widgets[0].text(),
                vocab_widgets[1].text().split(", "),
                vocab_widgets[2].text(),
                vocab_widgets[3].text().split(", "),
                int(vocab_widgets[4].text())
            )
            edit_vocab(vocab)
