from PyQt6.QtWidgets import (
    QWidget,
    QListWidget
)


class AllVocabs(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QListWidget()
        self.widget.addItem("Vocab1: German")
        self.widget.addItem("Vocab2: German")
        self.widget.addItem("Vocab3: German")
        self.widget.addItem("Vocab4: German")
        self.widget.addItem("Vocab5: German")