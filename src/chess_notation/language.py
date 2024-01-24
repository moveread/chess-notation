import json
import functools
import os
from typing import Literal
import ramda as R

Language = Literal["CA", "EN", "DE", "RU", "RO", "BG", "FR", "AZ", "TR", "PL", "IS", "NL", "DK"]

@functools.lru_cache(maxsize=1)
def translations():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "translations.json")
    with open(path) as f:
        return json.load(f)

@functools.cache
def translator(language: Language) -> dict[int, str]:
    return str.maketrans(translations()[language])

@R.curry
def translate(language: Language, san: str) -> str:
    return san.translate(translator(language))