from random import choices
from json import loads

from requests import get

from src.txt_files import russian_words
from src.consts import ENGLISH_WORDS_API


def get_english_words(number: int, length: int = None) -> tuple[str]:
    url_api = f'{ENGLISH_WORDS_API}/word?{number=}'
    if length and length > 2:
        url_api += f'&{length=}'
    respones = get(url_api)
    return tuple(loads(respones.text))


def get_russian_words(number: int) -> tuple[str]:
    return tuple(choices(russian_words, k=number))


def normalize_text(string: str) -> str:
    return ' '.join(string.strip().split())
