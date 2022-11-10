from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from src.widgets.InfoConfirmWidget import InfoConfirm
from src.ui_files import Custom_UI
from ..consts import (LEVEL_BUTTON_FONT, OOPS, CANNOT_DELETE_LEVEL, DELETING_LEVEL_TITLE, DELETING_LEVEL_CONTENT,
                      LEVEL_DELETED_SUCCESSFULY_TITLE, LEVEL_DELETED_SUCCESSFULY_CONTENT, CUSTOMS_LEVELS_IN_ROW)
from ..database import Database


# Сигнал от кнопок изменений передаётся в мэйн и оттуда уже cudmenu
class CustomMenu(QWidget, Custom_UI):
    """
    Меню кастомных уровней.

    Имеет кнопки с названиями уровней для выбора кастомного уровня.
    Имеет переход в CUD Меню для удаления или редактирования выбранного кастомного уровня.
    Сигнал от кнопок передаётся в main.py и оттуда уже в CUDWidget и PreGameWidget.
    Сам делает вызов класса базы данных для удаления уровней.
    """
    add_level_button: QPushButton
    update_level_button: QPushButton
    delete_level_button: QPushButton
    custom_quit_button: QPushButton
    buttons_layout: QVBoxLayout
    quit = pyqtSignal()
    add_level = pyqtSignal()
    update_level = pyqtSignal()
    delete_level = pyqtSignal(str)
    level_changed = pyqtSignal(str)
    levels_updated = pyqtSignal()

    def __init__(self, ui_path: Path, database: Database, user_width: int, user_height: int):
        super().__init__()
        self.user_width = user_width
        self.user_height = user_height
        self.database = database
        self.level = ''
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'custom_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.custom_quit_button.clicked.connect(self.quit.emit)
        self.add_level_button.clicked.connect(self.add_level)
        self.delete_level_button.clicked.connect(self.open_delete_level)
        self.update_level_button.clicked.connect(self.update_level)
        self.clear_buttons()
        self.upload_buttons()

    def open_confirm_window(self, window_title: str, window_text: str):
        self.confirm_window = InfoConfirm(window_title, window_text, self.user_width, self.user_height)

    def clear_buttons(self):
        for i in reversed(range(self.buttons_layout.count())):
            layout = self.buttons_layout.itemAt(i).layout()
            for j in reversed(range(layout.count())):
                layout.itemAt(j).widget().setParent(None)
            self.buttons_layout.itemAt(i).layout().deleteLater()

    def upload_buttons(self):
        self.clear_buttons()
        titles = [i[0] for i in self.database.get_custom_levels()]
        for row in range(0, len(titles), CUSTOMS_LEVELS_IN_ROW):
            row_titles = titles[row:row + CUSTOMS_LEVELS_IN_ROW]
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            for title in row_titles:
                btn = QPushButton(title)
                btn.setFont(LEVEL_BUTTON_FONT)
                btn.clicked.connect(self.change_level)
                btn.setFixedSize(btn.sizeHint())
                layout.addWidget(btn)
            self.buttons_layout.addLayout(layout)

    def change_level(self):
        self.level = self.sender().text()
        self.level_changed.emit(self.level)

    def open_delete_level(self):
        if not self.level or self.level not in [i[0] for i in self.database.get_custom_levels()]:
            return self.open_confirm_window(OOPS, CANNOT_DELETE_LEVEL)
        valid = QMessageBox.question(self, DELETING_LEVEL_TITLE, DELETING_LEVEL_CONTENT.format(self.level),
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            level_info = self.database.get_custom_level(self.level)
            if not level_info:
                ValueError("It is impossible, bro. Don't do strange things.")
            self.database.delete_custom_level(level_info[0])
            self.open_confirm_window(LEVEL_DELETED_SUCCESSFULY_TITLE,
                                     LEVEL_DELETED_SUCCESSFULY_CONTENT.format(self.level))
            self.upload_buttons()
            self.delete_level.emit(self.level)









