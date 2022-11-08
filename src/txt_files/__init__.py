from src.txt_files.russian_levels import russian_levels
from src.txt_files.english_levels import english_levels
from src.txt_files.punctuations_and_numbers import puncts_levels

try:
    from src.txt_files.russian_utf8 import russian_words
except ImportError:
    from requests import get
    from pathlib import Path
    from os import remove
    ru_words_txt = 'https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt'
    txt_files_path = Path(__file__).parent
    response = get(ru_words_txt)
    text = response.content.decode('cp1251')
    with open(txt_files_path / 'russian.txt', 'wb') as ru:
        ru.write(text.encode('utf-8'))

    with open(txt_files_path / 'russian.txt', 'r', encoding='utf-8') as txt_file:
        with open(txt_files_path / 'russian_utf8.py', 'w', encoding='utf8') as py_file:
            py_file.write('russian_words = [\n')
            for line in txt_file:
                py_file.write(f'"{line.strip()}",\n')
            py_file.write(']')

    remove(txt_files_path / 'russian.txt')
    from src.txt_files.russian_utf8 import russian_words
