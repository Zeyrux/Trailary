import os
import random

from pathlib import Path
from dataclasses import dataclass, field

DIR_VOCAB = "Vocabs"
FILE_VOCAB = "vocabs.vocabulary"
SEPARATOR = "#SEP#"
vocabs = []


@dataclass(frozen=True, order=True)
class Vocab:
    eng: str
    ger: str = field(compare=False)

    def __len__(self):
        return len(self.vocab)


def save_vocab(vocabs: list[Vocab]):
    if not os.path.isdir(DIR_VOCAB):
        Path(DIR_VOCAB).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "a") as f:
        for vocab in vocabs:
            f.write(vocab.eng)
            f.write(SEPARATOR)
            f.write(vocab.ger)
            f.write("\n")


def read_vocab():
    if not os.path.isfile(os.path.join(DIR_VOCAB, FILE_VOCAB)):
        return
    with open(os.path.join(DIR_VOCAB, FILE_VOCAB), "r") as f:
        while True:
            line = f.readline().replace("\n", "").split(SEPARATOR)
            if line[0] == "":
                return
            vocabs.append(Vocab(line[0], line[1]))


def get_random_vocab() -> Vocab:
    if len(vocabs) == 0:
        return ""
    return vocabs[random.randint(0, len(vocabs) - 1)]


read_vocab()
