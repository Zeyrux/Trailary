import os
import random

from lib.CustomWidgets import CustomDialog

from pathlib import Path

DIR_VOCAB = "Vocabs"
FILE_VOCAB = "vocabs.vocabulary"
SEPARATOR = "#SEP#"
ALTERNATIVE = "#ALT#"
PRÄFIX = "#PRA#"

vocabs: list["Vocab"] = None


class VocabPiece:
    def __init__(
            self,
            vocab: str,
            präfix: str = ""
    ):
        self.vocab = vocab
        self.präfix = "" if präfix is None else präfix

    def __lt__(self, other: "VocabPiece"):
        if self.vocab == other.vocab:
            return self.präfix < other.präfix
        return self.vocab < other.vocab

    def __str__(self):
        if self.präfix == "":
            return self.vocab
        return f"{self.präfix} {self.vocab}"


class Vocab:
    def __init__(
            self,
            lan_given: str,
            given: list[VocabPiece],
            lan_searched: str,
            searched: list[VocabPiece],
            line: int = -1
    ):
        self.lan_given = lan_given
        self.given = given
        self.lan_searched = lan_searched
        self.searched = searched
        self.line = line

        # given in str form
        self.given_str = ""
        for piece in given:
            self.given_str += f"{piece}, "
        self.given_str = self.given_str[:len(self.given_str)-2]
        # searched in str form
        self.searched_str = ""
        for piece in searched:
            self.searched_str += f"{piece}, "
        self.searched_str = self.searched_str[:len(self.searched_str) - 2]

        # given only vocabs
        self.given_vocabs = []
        for piece in self.given:
            self.given_vocabs.append(piece.vocab)
        # searched only vocabs
        self.searched_vocabs = []
        for piece in self.searched:
            self.searched_vocabs.append(piece.vocab)

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
               f"given: {self.given_str}; " \
               f"lan_searched: {self.lan_searched}; " \
               f"searched: {self.searched_str}; " \
               f"line: {self.line}"

    def __eq__(self, other: str):
        if other in self.searched_str.split(", "):
            return True
        if other in self.searched_vocabs:
            return True
        return False

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
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "ab") as f:
        for vocab in vocabs:
            f.write(get_save_vocab(vocab).encode())


def get_save_vocab(vocab: Vocab) -> str:
    # lan given
    result = vocab.lan_given.lower() + SEPARATOR

    # vocab given
    for piece in vocab.given:
        result += piece.vocab.lower()
        if piece.präfix != "":
            result += PRÄFIX + piece.präfix.lower()
        result += ALTERNATIVE
    result = result[:len(result)-len(ALTERNATIVE)]
    result += SEPARATOR

    # lan searched
    result += vocab.lan_searched.lower() + SEPARATOR

    # vocab searched
    for piece in vocab.searched:
        result += piece.vocab.lower()
        if piece.präfix != "":
            result += PRÄFIX + piece.präfix.lower()
        result += ALTERNATIVE
    result = result[:len(result)-len(ALTERNATIVE)]
    result += "\n"
    return result


def edit_vocab(vocab: Vocab):
    lines = binary_list_to_string(
        open(os.path.join(DIR_VOCAB, FILE_VOCAB), "rb").readlines()
    )
    lines[vocab.line] = get_save_vocab(vocab)
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "wb") as f:
        f.writelines(string_list_to_binary(lines))


def read_vocab():
    vocabs = []
    if not os.path.isfile(os.path.join(DIR_VOCAB, FILE_VOCAB)):
        return
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "rb") as f:
        line_count = 0
        while True:
            line = f.readline().decode()
            line = line.replace("\n", "")
            if line == "":
                return vocabs
            lan_given, given, lan_searched, searched \
                = line.split(SEPARATOR)
            given = given.split(ALTERNATIVE)
            given_pieces: list[VocabPiece] = []
            for element in given:
                given_pieces.append(input_to_vocab_piece(element))

            searched = searched.split(ALTERNATIVE)
            searched_pieces: list[VocabPiece] = []
            for element in searched:
                searched_pieces.append(input_to_vocab_piece(element))
            vocab = Vocab(
                lan_given,
                given_pieces,
                lan_searched,
                searched_pieces,
                line_count
            )
            vocabs.append(vocab)
            line_count += 1


def input_to_vocab_piece(element) -> VocabPiece:
    piece = element.split(PRÄFIX)
    if len(piece) == 1:
        return VocabPiece(piece[0])
    elif len(piece) == 2:
        return VocabPiece(piece[0], piece[1])
    else:
        CustomDialog(
            title="ERROR",
            message=f"Error at reading all vocabs!\n"
                    f"Please restart and check you vocabs!"
        )


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


def split_comma(string: str) -> str:
    if string == "":
        return string
    string = string.split(",")
    for i, word in enumerate(string):
        if word[0] == " ":
            string[i] = word[1:len(word)]
    return string


def copy_vocab(vocab: Vocab) -> Vocab:
    return Vocab(
        vocab.lan_given,
        vocab.given,
        vocab.lan_searched,
        vocab.searched,
        vocab.line
    )


def binary_list_to_string(binar_l: list) -> list[str]:
    for i, element in enumerate(binar_l):
        binar_l[i] = element.decode()
    return binar_l


def string_list_to_binary(string_l: list) -> list:
    for i, element in enumerate(string_l):
        string_l[i] = element.encode()
    return string_l


def reload():
    global vocabs
    vocabs = read_vocab()
    vocabs.sort()


def delete_vocab(line):
    lines = binary_list_to_string(
        open(os.path.join(DIR_VOCAB, FILE_VOCAB), "rb").readlines()
    )
    del lines[line]
    open(os.path.join(DIR_VOCAB, FILE_VOCAB), "wb").writelines(
        string_list_to_binary(lines)
    )


reload()
