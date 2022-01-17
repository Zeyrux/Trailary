from PyQt6.QtGui import QKeyEvent


class Keyboard:
    def __init__(self, keys: list[int]):
        self.keys = {}
        for key in keys:
            self.keys[key] = False

    def key_press(self, event: QKeyEvent):
        if event.key() in self.keys:
            self.keys[event.key()] = True

    def key_release(self, event: QKeyEvent):
        if event.key() in self.keys:
            self.keys[event.key()] = False

    def key(self, key):
        return self.keys.get(key)
