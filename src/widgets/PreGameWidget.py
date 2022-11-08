from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel

from src.ui_files import PreGame_UI
from ..consts import (RU_LEVELS, ENG_LEVELS, PUNCT_LEVELS, RANDOM_WORDS, LEVEL_BUTTON_FONT, CUSTOM_BUTTON,
                      YOUR_NAME_LABEL, LANG_NOW, LEVEL_NOW, Languages)


# Меню с выбором уровней
class PreGameMenu(QWidget, PreGame_UI):
    """
    Меню выбора уровня

    Выбор встроенных уровней, переход в меню кастомных уровней и запуск игры.
    Язык нужен лишь для отображения в label'е.
    """
    pregame_quit_button: QPushButton
    startgame_button: QPushButton
    buttons_layout: QVBoxLayout
    name_label: QLabel
    lang_label: QLabel
    level_label: QLabel
    quit = pyqtSignal()
    game_started = pyqtSignal()
    open_custom_menu = pyqtSignal()
    level_changed = pyqtSignal(str)

    def __init__(self, ui_path: Path):
        super().__init__()
        self.level = 'ва ол'
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'pregame_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.pregame_quit_button.clicked.connect(self.quit.emit)
        self.startgame_button.clicked.connect(self.start_game)

    def edit_pregame_menu(self, username: str, level: str):
        self.name_label.setText(YOUR_NAME_LABEL.format(username))
        self.lang_label.setText(LANG_NOW.format(self.get_lang(level)))
        self.level_label.setText(LEVEL_NOW.format(level))
        if self.buttons_layout.count():
            return

        for levels in (RU_LEVELS, ENG_LEVELS):
            hlayout = QHBoxLayout()
            hlayout.setAlignment(Qt.AlignHCenter)
            for name in levels:
                button = QPushButton(name, self)
                button.setFixedSize(100, 50)
                button.setFont(LEVEL_BUTTON_FONT)
                button.clicked.connect(self.change_level)
                hlayout.addWidget(button)
            self.buttons_layout.addLayout(hlayout)

        for level in (PUNCT_LEVELS, RANDOM_WORDS):
            hlayout = QHBoxLayout()
            hlayout.setAlignment(Qt.AlignHCenter)
            for name in level:
                button = QPushButton(name, self)
                button.setFixedSize(150, 50)
                button.setFont(LEVEL_BUTTON_FONT)
                button.clicked.connect(self.change_level)
                hlayout.addWidget(button)
            self.buttons_layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignHCenter)
        button = QPushButton(CUSTOM_BUTTON, self)
        button.setFixedSize(250, 50)
        button.setFont(LEVEL_BUTTON_FONT)
        button.clicked.connect(self.open_custom_menu.emit)
        hlayout.addWidget(button)
        self.buttons_layout.addLayout(hlayout)

    def update_labels(self, level: str):
        self.level = level
        self.level_label.setText(LEVEL_NOW.format(level))
        self.lang_label.setText(LANG_NOW.format(self.get_lang(level)))

    def start_game(self):
        self.game_started.emit()

    @staticmethod
    def get_lang(level: str):
        if level in RU_LEVELS or level == Languages.RUSSIAN.value:
            return Languages.RU.value
        elif level in ENG_LEVELS or level == Languages.ENGLISH.value:
            return Languages.ENG.value
        elif level in PUNCT_LEVELS:
            return Languages.PUNCTS.value
        else:
            return Languages.CUSTOM.value

    def change_level(self):
        level = self.sender().text()
        self.update_labels(level)
        self.level_changed.emit(level)
