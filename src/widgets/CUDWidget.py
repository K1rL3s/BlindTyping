from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QPlainTextEdit

from src.main_funcs import Database
from src.widgets.InfoConfirmWidget import InfoConfirm
from src.ui_files import CUD_UI
from ..consts import (Actions, NAMEING_LENGHT_LIMIT, LEVEL_ADDED_SUCCESSFULY_TITLE, LEVEL_ADDED_SUCCESSFULY_CONTENT,
                      OOPS, LEVEL_UPDATED_SUCCESSFULY_TITLE, LEVEL_UPDATED_SUCCESSFULY_CONTENT, LEVEL_NOT_FOUND,
                      LEVEL_NAME_ALREADY_TAKEN, BAD_SYMBOLS)


# при добавлении/изменении кастомного уровня обновление self.levels (main.py) и кнопок в CustomMenu
# функционал = изменение/добавление кастомных уровней сразу в бд и выброс сигнала
class CreateUpdateDeleteMenu(QWidget, CUD_UI):
    cud_title_line: QLineEdit
    cud_content_plain: QPlainTextEdit
    cud_confirm_button: QPushButton
    cud_quit_button: QPushButton
    quit = pyqtSignal()
    levels_updated = pyqtSignal()

    def __init__(self, ui_path: Path, database: Database, user_width: int, user_height: int):
        super().__init__()
        self.user_width = user_width
        self.user_height = user_height
        self.current_action = ''  # 'new', 'update'
        self.level_id: int | None = None
        self.database = database
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'cud_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.cud_quit_button.clicked.connect(self.quit.emit)
        self.cud_confirm_button.clicked.connect(self.on_confirm_click)

    def fill_values(self, title: str = '', content: str = ''):
        self.cud_title_line.setText(title)
        self.cud_content_plain.setPlainText(content)

    @staticmethod
    def format_text(text: str) -> str:
        for bad_symbol in BAD_SYMBOLS:
            while bad_symbol in text:
                text = text.replace(bad_symbol, ' ')
        return text

    def set_action(self, action: str, level_title: str = None):
        self.current_action = action
        if action == Actions.ADD.value:
            self.fill_values()
        elif action == Actions.UPDATE.value:
            if level_title is None:
                raise ValueError('If action is "update", level_title is required')
            level_info = self.database.get_custom_level(level_title)
            if not level_info:
                self.open_confirm_window(OOPS, LEVEL_NOT_FOUND.format(level_title))
                return False
            else:
                self.level_id = level_info[0]
                self.fill_values(*level_info[1:])
                return True

    def on_confirm_click(self):
        if self.current_action == Actions.ADD.value:
            self.add_level()
        elif self.current_action == Actions.UPDATE.value:
            self.update_level()

    def open_confirm_window(self, window_title: str, window_text: str):
        self.confirm_window = InfoConfirm(window_title, window_text, self.user_width, self.user_height)

    def add_level(self):
        title = self.cud_title_line.text()[:NAMEING_LENGHT_LIMIT]
        content = self.format_text(self.cud_content_plain.toPlainText())
        if not content or not title:
            return
        if self.database.add_custom_level(title, content):
            self.open_confirm_window(LEVEL_ADDED_SUCCESSFULY_TITLE, LEVEL_ADDED_SUCCESSFULY_CONTENT.format(title))
            self.quit.emit()
            self.levels_updated.emit()
        else:
            self.open_confirm_window(OOPS, LEVEL_NAME_ALREADY_TAKEN.format(title))

    def update_level(self):
        title = self.cud_title_line.text()[:NAMEING_LENGHT_LIMIT]
        content = self.format_text(self.cud_content_plain.toPlainText())
        if not content or not title:
            return
        if self.database.update_custom_level(self.level_id, title, content):
            self.open_confirm_window(LEVEL_UPDATED_SUCCESSFULY_TITLE, LEVEL_UPDATED_SUCCESSFULY_CONTENT.format(title))
            self.quit.emit()
            self.levels_updated.emit()
        else:
            self.open_confirm_window(OOPS, LEVEL_NAME_ALREADY_TAKEN.format(title))
