
class Style:
    def __init__(self, styles: list[str]):
        self.style = ""
        for style in styles:
            self.style += style

    def change_font_size(self, new_font_size: int):
        pass
