from PyQt5.QtGui import QFont, QColor
from enum import Enum


APP_NAME = 'Слепопечать v0.1'
LEVEL_BUTTON_FONT = QFont("Comic Sans MS", 15)
HANDS_STYLE_SHEETS = ('#hands_hide_button {',
                      'background-color: transparent;',
                      'border-image: url(:/icons/images/hands_on.png);',
                      'background: none;',
                      'border: none;',
                      'background-repeat: none;}')
KEYBOARD_STYLE_SHEETS = ('#keyboard_hide_button {',
                         'background-color: transparent;',
                         'border-image: url(:/icons/images/keyboard_on.png);',
                         'background: none;',
                         'border: none;',
                         'background-repeat: none;}')
CONFIRM_INFO_FONT = QFont("Comic Sans MS", 25)
TIME_INTERVAL = 75
PREGAME_DELAY = 5000
MINIMUM_TEXT_LENGTH = 250  # for random russian or english words, not for custom levels
MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT = 1200, 800
RANDOM_WORDS = ('русские', 'инглиш')
PUNCT_LEVELS = ('основные', 'числа', 'другие')
RU_LEVELS = ('ва ол', 'фы дж', 'ми ть', 'еп нр', 'ук гш', 'чс бю', 'йц щц', 'я эхъ')
ENG_LEVELS = ('df jl', 'as l;', 'vb nm', 'tg yh', 'er ui', 'qw op', 'xc ,.', 'z!?/')
BAD_SYMBOLS = ('\n', '	', '  ')  # newline, tab-char and double space
PLACES = (QColor(224, 214, 0), QColor(180, 181, 189), QColor(155, 82, 33))
DISPLAY_TEXT_LENGHT = 25
NAMEING_LENGHT_LIMIT = 16
GAME_DELAY = 5
CUSTOMS_LEVEL_IN_ROW = 5
CUSTOM_BUTTON = 'кастомные уровни'


ENGLISH_WORDS_API = 'https://random-word-api.herokuapp.com'
OOPS = 'Упс...'
NAME_CHANGED_SUCCESSFULY = 'Имя успешно изменено!'
YOUR_NAME_NOW = 'Теперь вас зовут {}!'
LEVEL_CHANGED_SUCCESSFULY = 'Выбран другой уровень!'
LEVEL_UPDATED_SUCCESSFULY_TITLE = 'Уровень изменён!'
LEVEL_UPDATED_SUCCESSFULY_CONTENT = 'Уровень "{}" успешно обновлён!'
LEVEL_ADDED_SUCCESSFULY_TITLE = 'Уровень добавлен!'
LEVEL_ADDED_SUCCESSFULY_CONTENT = 'Уровень "{}" успешно добавлен!'
LEVEL_DELETED_SUCCESSFULY_TITLE = 'Уровень удалён!'
LEVEL_DELETED_SUCCESSFULY_CONTENT = 'Уровень "{}" успешно удалён!'
LEVEL_NOT_FOUND = 'Уровень "{}" не найден'
LEVEL_NAME_ALREADY_TAKEN = 'Название "{}" уже занято'
CURRENT_LEVEL = 'Текущий уровень: {}!'
TEXT_NOT_FOUND = 'Для уровня "{}" не найден текст'
CANNOT_DELETE_LEVEL = 'Нельзя удалить этот уровень'
DELETING_LEVEL_TITLE = 'Удаление уровня'
DELETING_LEVEL_CONTENT = 'Удалить уровень "{}"?'
YOUR_NAME_LABEL = 'Ваше имя: {}'
LANG_NOW = 'Язык текста: {}'
LEVEL_NOW = 'Уровень: {}'
RECORD_CONFIRM_TITLE = 'Сохранить рекорд?'
RECORD_CONFIRM_CONTENT = "Имя: {}\nРекорд: {} символов/мин"
RECORDS_FOUND = 'Рекордов типа "{}": {}'
RECORDS_NOT_FOUND = 'Нет рекордов :('
RECORD_RESULT = '{} symbs/minute'
RECORDS_WIDGET_COLUMNS = ('Имя', 'Скорость')
CHANGE_NAME_TITLE = 'Введите ваше имя'
CHANGE_NAME_CONTENT = 'Как вас зовут?'


class Languages(Enum):
    ENGLISH = 'инглиш'
    RUSSIAN = 'русские'
    ENG = 'ENG'
    RU = 'RU'
    PUNCTS = 'Символы'
    CUSTOM = 'Кастом'


class Actions(Enum):
    ADD = 'new'
    UPDATE = 'update'


class ModeNames(Enum):
    WORDS = 'слова'
    NUMBERS = 'числа'
    LETTERS = 'буквы'
    CUSTOMS = 'кастом'
