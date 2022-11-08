import sys
import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from src import (MainMenu, SettingsMenu, PreGameMenu, GameMenu, RecordsMenu, InfoConfirm, CustomMenu,
                 CreateUpdateDeleteMenu, consts, Database, russian_levels, english_levels, puncts_levels,
                 get_english_words, get_russian_words)


USER_WIDTH, USER_HEIGHT = 800, 600 
UI_PATH = Path().absolute() / 'src' / 'ui_files'


# Основное окно, которое обеспечивает связь между всеми виджетами
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = os.getlogin()
        self.level = 'ва ол'
        self.levels = dict()
        self.custom_levels = dict()
        self.database = Database()
        self.stacked_widget = QStackedWidget(self)
        self.init_levels()
        self.upload_levels()
        self.init_ui()

    # Добавление встроенных уровней
    def init_levels(self):
        for key, value in zip(consts.RU_LEVELS, russian_levels):
            self.levels[key] = value
        for key, value in zip(consts.ENG_LEVELS, english_levels):
            self.levels[key] = value
        for key, value in zip(consts.PUNCT_LEVELS, puncts_levels):
            self.levels[key] = value
        self.upload_levels()

    def init_ui(self):
        self.resize(consts.MAIN_WINDOW_WIDTH, consts.MAIN_WINDOW_HEIGHT)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.resize(self.size())
        self.setObjectName('MainWindow')
        self.setWindowTitle(consts.APP_NAME)
        self.main_menu = MainMenu(UI_PATH)
        self.settings_menu = SettingsMenu(UI_PATH)
        self.pregame_menu = PreGameMenu(UI_PATH)
        self.custom_menu = CustomMenu(UI_PATH, self.database, USER_WIDTH, USER_HEIGHT)
        self.cud_menu = CreateUpdateDeleteMenu(UI_PATH, self.database, USER_WIDTH, USER_HEIGHT)
        self.records_menu = RecordsMenu(UI_PATH, self.database)
        self.game_menu = GameMenu(UI_PATH, USER_WIDTH, USER_HEIGHT)

        self.main_menu.open_pregame.connect(self.open_pregame)
        self.main_menu.open_settings.connect(self.open_settings)
        self.main_menu.open_records.connect(self.open_records)
        self.main_menu.close_app.connect(self.close)

        self.settings_menu.quit.connect(self.open_main_menu)
        self.settings_menu.name_changed.connect(self.change_name)
        self.settings_menu.background_changed.connect(self.change_background)
        self.settings_menu.change_background()

        self.pregame_menu.quit.connect(self.open_main_menu)
        self.pregame_menu.open_custom_menu.connect(self.open_custom_menu)
        self.pregame_menu.level_changed.connect(self.change_level)
        self.pregame_menu.game_started.connect(self.start_game)

        self.custom_menu.quit.connect(self.open_pregame)
        self.custom_menu.level_changed.connect(self.change_level)
        self.custom_menu.add_level.connect(self.cud_add_level)
        self.custom_menu.update_level.connect(self.cud_update_level)
        self.custom_menu.delete_level.connect(self.upload_levels)

        self.cud_menu.quit.connect(self.open_custom_menu)
        self.cud_menu.levels_updated.connect(self.upload_levels)

        self.records_menu.quit.connect(self.open_main_menu)

        self.game_menu.quit.connect(self.open_main_menu)
        self.game_menu.game_ended.connect(self.new_record)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings_menu)
        self.stacked_widget.addWidget(self.pregame_menu)
        self.stacked_widget.addWidget(self.custom_menu)
        self.stacked_widget.addWidget(self.cud_menu)
        self.stacked_widget.addWidget(self.records_menu)
        self.stacked_widget.addWidget(self.game_menu)
        self.open_main_menu()

    def open_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def open_pregame(self):
        self.stacked_widget.setCurrentWidget(self.pregame_menu)
        self.pregame_menu.edit_pregame_menu(self.username, self.level)

    def open_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_menu)

    def open_records(self):
        # self.records_menu.update_all_tables()
        self.stacked_widget.setCurrentWidget(self.records_menu)

    def open_game(self):
        self.stacked_widget.setCurrentWidget(self.game_menu)

    def open_custom_menu(self):
        self.custom_menu.upload_buttons()
        self.stacked_widget.setCurrentWidget(self.custom_menu)

    def open_confirm_info(self, window_title: str, window_text: str):
        self.confirm_window = InfoConfirm(window_title, window_text, USER_WIDTH, USER_HEIGHT)

    def change_name(self, name):
        self.username = name[:consts.NAMEING_LENGHT_LIMIT]
        self.open_confirm_info(consts.NAME_CHANGED_SUCCESSFULY, consts.YOUR_NAME_NOW.format(self.username))

    # Смена фона делается с помощью Qt styleSheets
    def change_background(self, background):
        style_sheets_mainwindow = '#MainWindow {' + \
                                  f'border-image: url(:/images/images/background{background}.png)' \
                                  + '}'
        self.setStyleSheet(style_sheets_mainwindow)

    # pregame_menu.update_labels вызывается, чтобы при выборе кастомных уровней в custom_menu
    # информация на pregame_menu обновлялась
    def change_level(self, level):
        if self.level != level:
            self.level = level
            self.pregame_menu.update_labels(level)
            self.open_confirm_info(consts.LEVEL_CHANGED_SUCCESSFULY, consts.CURRENT_LEVEL.format(level))

    def start_game(self):
        text = self.get_level_text()
        # Проверка на случай удаления уровня и попытка запуска игры с ним
        if text:
            self.open_game()
            self.game_menu.set_displayed_text(text.strip())
            self.game_menu.start_game(self.username)
        else:
            self.open_confirm_info(consts.OOPS, consts.TEXT_NOT_FOUND.format(self.level))

    # Открытие CUDMenu без данных
    def cud_add_level(self):
        self.cud_menu.set_action(consts.Actions.ADD.value)
        self.stacked_widget.setCurrentWidget(self.cud_menu)

    # Открытие CUDMenu с данными выбранного КАСТОМНОГО уровня
    def cud_update_level(self):
        if self.cud_menu.set_action(consts.Actions.UPDATE.value, self.level):
            self.stacked_widget.setCurrentWidget(self.cud_menu)

    # Загрузка кастомных уровней из бд в словарь
    def upload_levels(self):
        self.custom_levels.clear()
        for key, value in self.database.get_custom_levels():
            self.custom_levels[key] = value

    def get_level_text(self):
        text = ''
        if self.level == consts.Languages.RUSSIAN.value:
            while len(text) <= consts.MINIMUM_TEXT_LENGTH:
                text += ' '.join((get_russian_words(10))) + ' '
        elif self.level == consts.Languages.ENGLISH.value:
            while len(text) <= consts.MINIMUM_TEXT_LENGTH:
                text += ' '.join((get_english_words(10))) + ' '
        elif self.level in self.levels.keys():
            text = self.levels[self.level]
        else:
            text = self.custom_levels.get(self.level)
        return text

    def new_record(self, symbs_per_min: int):
        if self.level in russian_levels or self.level in english_levels:
            mode_name = consts.ModeNames.LETTERS.value
        elif self.level in puncts_levels:
            mode_name = consts.ModeNames.NUMBERS.value
        elif self.level in (consts.Languages.ENGLISH.value, consts.Languages.RUSSIAN.value):
            mode_name = consts.ModeNames.WORDS.value
        else:
            mode_name = consts.ModeNames.CUSTOMS.value
        self.database.add_new_record(self.username, symbs_per_min, mode_name)

    def closeEvent(self, event):
        self.database.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = app.desktop().screenGeometry()
    USER_WIDTH, USER_HEIGHT = display.width(), display.height()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
