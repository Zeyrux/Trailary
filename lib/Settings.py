import os
import pathlib

from lib.CustomWidgets import CustomDialog

SEPERATOR = ";"


class Setting:
    def __init__(self, name: str, value: object, dtype=""):
        self.name = name
        if dtype == "":
            self.value = value
            self.dtype = type(value)
        else:
            if dtype == "float":
                self.value = float(value)
                self.dtype = float
            elif dtype == "str":
                self.value = str(value)
                self.dtype = str
            elif dtype == "int":
                self.value = int(value)
                self.dtype = int
            else:
                CustomDialog(
                    title="WARNING",
                    message="could not find the datatype of setting",
                    ignore_settings=True
                )

    def __str__(self):
        return f"name: {self.name}; " \
               f"value: {self.value}; " \
               f"dtype: {self.dtype}"


class Settings:
    def __init__(self, file_location: str):
        assert os.path.isfile(file_location)
        self.settings = []
        with open(file_location, "rb") as f:
            while True:
                line = f.readline().decode()
                line = line.replace("\n", "")
                if line == "":
                    break
                setting_type = line[:line.index(SEPERATOR)]
                line = line[line.index(SEPERATOR)+1:]
                setting_name = line[:line.index(SEPERATOR)]
                setting_value = line[line.index(SEPERATOR)+1:]
                self.settings.append(Setting(
                    setting_name,
                    setting_value,
                    setting_type
                ))

    def get(self, name) -> Setting:
        for setting in self.settings:
            if setting.name == name:
                return setting
        return None

    @classmethod
    def new(cls, location: str, settings: list[Setting]=None):
        if settings is None:
            settings = []
        if "\\" in location:
            if not os.path.isdir(location[0:location.rindex("\\")]):
                pathlib.Path(location).mkdir(parents=True, exist_ok=True)

        with open(location, "wb") as f:
            for setting in settings:
                f.write(setting.dtype.__name__.encode())
                f.write(SEPERATOR.encode())
                f.write(setting.name.encode())
                f.write(SEPERATOR.encode())
                f.write(str(setting.value).encode())
                f.write("\n".encode())
        return Settings(location)
