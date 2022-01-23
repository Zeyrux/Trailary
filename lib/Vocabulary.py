import os
import random

from pathlib import Path

DIR_VOCAB = "Vocabs"
FILE_VOCAB = "vocabs.vocabulary"
SEPARATOR = "#SEP#"
ALTERNATIVE = "#ALT#"

vocabs: list["Vocab"] = None


class Vocab:
    def __init__(
            self,
            lan_given: str,
            given: list[str],
            lan_searched: str,
            searched: list[str]
    ):
        self.lan_given = lan_given
        self.given = given
        self.lan_searched = lan_searched
        self.searched = searched

    def __lt__(self, other: "Vocab"):
        if self.lan_given == other.lan_given:
            if self.lan_searched == other.lan_searched:
                if self.given == other.given:
                    return self.searched < other.searched
                return self.given < other.given
            return self.lan_searched < other.lan_searched
        return self.lan_given < other.lan_searched

    def __str__(self):
        return f"lan_given: {self.lan_given}; " \
               f"given: {self.given}; " \
               f"lan_searched: {self.lan_searched}; " \
               f"searched: {self.searched}"

    def switch_lan(self):
        help_lan = self.lan_searched
        help_vocab = self.searched
        self.lan_searched = self.lan_given
        self.searched = self.given
        self.lan_given = help_lan
        self.given = help_vocab


def save_vocab(vocabs: list[Vocab]):
    if not os.path.isdir(DIR_VOCAB):
        Path(DIR_VOCAB).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "a") as f:
        for vocab in vocabs:
            # vocab given
            f.write(vocab.lan_given.lower() + SEPARATOR)
            for i in range(len(vocab.given) - 1):
                f.write(vocab.given[i].lower() + ALTERNATIVE)
            f.write(vocab.given[-1].lower())

            # vocab searched
            f.write(SEPARATOR + vocab.lan_searched.lower() + SEPARATOR)
            for i in range(len(vocab.searched) - 1):
                f.write(vocab.searched[i].lower() + ALTERNATIVE)
            f.write(vocab.searched[-1].lower())
            f.write("\n")


def read_vocab():
    vocabs = []
    if not os.path.isfile(os.path.join(DIR_VOCAB, FILE_VOCAB)):
        return
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "r") as f:
        while True:
            line = f.readline().replace("\n", "")
            if line == "":
                return vocabs
            len_given, given, len_searched, searched \
                = line.split(SEPARATOR)
            vocab = Vocab(
                len_given,
                given.split(ALTERNATIVE),
                len_searched,
                searched.split(ALTERNATIVE)
            )
            vocabs.append(vocab)


def get_random_vocab(language_given="", language_search="") -> Vocab:
    if len(vocabs) == 0:
        return ""
    while True:
        copy_vocab = vocabs[random.randint(0, len(vocabs) - 1)]
        vocab = Vocab(
            copy_vocab.lan_given,
            copy_vocab.given,
            copy_vocab.lan_searched,
            copy_vocab.searched
        )
        if language_given == vocab.lan_given \
                or vocab.lan_searched \
                and language_search == vocab.lan_given \
                or vocab.lan_searched:
            if language_given != vocab.lan_given:
                vocab.switch_lan()
            break
    return vocab


def get_languages() -> list[str]:
    languages = []
    for vocab in vocabs:
        if vocab.lan_given not in languages:
            languages.append(vocab.lan_given)
        if vocab.lan_searched not in languages:
            languages.append(vocab.lan_searched)
    return languages


def remove_list(list: list) -> str:
    final_string = ""
    for i, string in enumerate(list):
        string = string.replace("[", "")
        string = string.replace("]", "")
        string = string.replace("\"", "")
        string = string.replace("'", "")
        final_string += f"{string}, " if len(list) != i + 1 else string
    return final_string


def reload():
    global vocabs
    vocabs = read_vocab()
    vocabs.sort()


reload()
