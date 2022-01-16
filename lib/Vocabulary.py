import os
import random

from pathlib import Path
from dataclasses import dataclass

DIR_VOCAB = "Vocabs"
FILE_VOCAB = "vocabs.vocabulary"
SEPARATOR = "#SEP#"
ALTERNATIVE = "#ALT#"
vocabs = []


@dataclass(frozen=True, order=True)
class Vocab:
    lan_given: str
    given: list[str]
    lan_searched: str
    searched: list[str]


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
    if not os.path.isfile(os.path.join(DIR_VOCAB, FILE_VOCAB)):
        return
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "r") as f:
        while True:
            line = f.readline().replace("\n", "")
            if line == "":
                return
            len_given, given, len_searched, searched \
                = line.split(SEPARATOR)
            vocab = Vocab(
                len_given,
                given.split(ALTERNATIVE),
                len_searched,
                searched.split(ALTERNATIVE)
            )
            vocabs.append(vocab)


def get_random_vocab() -> Vocab:
    if len(vocabs) == 0:
        return ""
    return vocabs[random.randint(0, len(vocabs) - 1)]


read_vocab()
