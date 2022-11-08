from random import randint
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QInputDialog

from src.ui_files import Settings_UI
from ..consts import CHANGE_NAME_TITLE, CHANGE_NAME_CONTENT


# Меню с сменой имени и фона
class SettingsMenu(QWidget, Settings_UI):
    settings_quit_button: QPushButton
    changename_button: QPushButton
    changebackground_button: QPushButton
    quit = pyqtSignal()
    name_changed = pyqtSignal(str)
    background_changed = pyqtSignal(int)

    def __init__(self, ui_path: Path):
        super().__init__()
        self.background_num = randint(1, 3)
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'settings_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.settings_quit_button.clicked.connect(self.quit.emit)
        self.changename_button.clicked.connect(self.change_name)
        self.changebackground_button.clicked.connect(self.change_background)

    def change_name(self):
        input_name = QInputDialog(self)
        username, ok_pressed = input_name.getText(self, CHANGE_NAME_TITLE, CHANGE_NAME_CONTENT)
        if ok_pressed and username:
            self.name_changed.emit(username)

    def change_background(self):
        self.background_num = self.background_num % 3 + 1
        self.background_changed.emit(self.background_num)
