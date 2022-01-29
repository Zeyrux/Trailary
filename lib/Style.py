
class Style:
    def __init__(self, styles: list[str]):
        self.style = ""
        for style in styles:
            self.style += style

    def change_font_size(self, object_change: str, new_font_size: int):
        new_style = f"\tfont-size: {new_font_size}px;"
        style_l = self.style.split("\n")
        for a in style_l:
            print(a)
        for i, line in enumerate(style_l):
            if object_change in line:
                for j, property in enumerate(style_l[i+1:]):
                    if "font-size:" in property:
                        style_l[i+j+1] = new_style
                        self.__set_style(style_l)
                        return
                    elif "}" in property:
                        style_l.insert(i+j+1, new_style)
                        self.__set_style(style_l)
                        return

    def __set_style(self, style_l: list[str]):
        new_style = ""
        for line in style_l:
            new_style += line
        self.style = new_style
