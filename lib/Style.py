class Style:
    def __init__(self, styles: list[str]):
        self.style = ""
        for style in styles:
            self.style += style

    def change_property(
            self,
            object_changed: str,
            property_search: str,
            new_property: str,
    ):
        new_style = f"\t{property_search}: {new_property};"
        style_l = self.style.split("\n")
        for i, line in enumerate(style_l):
            if object_changed in line:
                for j, property in enumerate(style_l[i + 1:]):
                    if f"{property_search}:" in property:
                        style_l[i + j + 1] = new_style
                        self.__set_style(style_l)
                        return
                    elif "}" in property:
                        style_l.insert(i + j + 1, new_style)
                        self.__set_style(style_l)
                        return

    def change_font_size(self, object_change: str, new_font_size: str):
        self.change_property(object_change, "font-size", new_font_size)

    def change_margin(self, object_change: str, new_margin: str):
        self.change_property(object_change, "margin", new_margin)

    def __set_style(self, style_l: list[str]):
        new_style = ""
        for line in style_l:
            new_style += line
        self.style = new_style
