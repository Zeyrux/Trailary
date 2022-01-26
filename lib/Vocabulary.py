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
            searched: list[str],
            line: int
    ):
        self.lan_given = lan_given
        self.given = given
        self.lan_searched = lan_searched
        self.searched = searched
        self.line = line

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
               f"searched: {self.searched}; " \
               f"line: {self.line}"

    def switch_lan(self):
        help_lan = self.lan_searched
        help_vocab = self.searched
        self.lan_searched = self.lan_given
        self.searched = self.given
        self.lan_given = help_lan
        self.given = help_vocab


def save_vocabs(vocabs: list[Vocab]):
    if not os.path.isdir(DIR_VOCAB):
        Path(DIR_VOCAB).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "a") as f:
        for vocab in vocabs:
            f.write(get_save_vocab(vocab))


def get_save_vocab(vocab: Vocab) -> str:
    # vocab given
    result = vocab.lan_given.lower() + SEPARATOR
    for i in range(len(vocab.given) - 1):
        result += vocab.given[i].lower() + ALTERNATIVE
    result += vocab.given[-1].lower()

    # vocab searched
    result += SEPARATOR + vocab.lan_searched.lower() + SEPARATOR
    for i in range(len(vocab.searched) - 1):
        result += vocab.searched[i].lower() + ALTERNATIVE
    result += vocab.searched[-1].lower()
    result += "\n"
    return result


def edit_vocab(vocab: Vocab):
    lines = open(os.path.join(DIR_VOCAB, FILE_VOCAB), "r").readlines()
    lines[vocab.line] = get_save_vocab(vocab)
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "w") as f:
        f.writelines(lines)


def read_vocab():
    vocabs = []
    if not os.path.isfile(os.path.join(DIR_VOCAB, FILE_VOCAB)):
        return
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "r") as f:
        line_count = 0
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
                searched.split(ALTERNATIVE),
                line_count
            )
            vocabs.append(vocab)
            line_count += 1


def get_random_vocab(language_given="", language_search="") -> Vocab:
    if len(vocabs) == 0:
        return ""
    while True:
        vocab = copy_vocab(vocabs[random.randint(0, len(vocabs) - 1)])
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


def copy_vocab(vocab: Vocab) -> Vocab:
    return Vocab(
        vocab.lan_given,
        vocab.given,
        vocab.lan_searched,
        vocab.searched,
        vocab.line
    )


def reload():
    global vocabs
    vocabs = read_vocab()
    vocabs.sort()


reload()
