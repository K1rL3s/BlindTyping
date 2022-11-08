from time import time as timestamp
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QProgressBar

from src.widgets.DisplayTextWidget import DisplayText
from src.widgets.TypingFilterWidget import TypingFilter
from src.widgets.RecordConfirmWidget import RecordConfirm
from src.ui_files import Game_UI
from ..consts import HANDS_STYLE_SHEETS, KEYBOARD_STYLE_SHEETS, TIME_INTERVAL, GAME_DELAY


class GameMenu(QWidget, Game_UI):
    progress_bar: QProgressBar
    displayed_text: DisplayText
    input_text_line: TypingFilter
    central_layout: QVBoxLayout
    timer_label: QLabel
    keyboard_label: QLabel
    right_hand_label: QLabel
    left_hand_label: QLabel
    game_quit_button: QPushButton
    keyboard_hide_button: QPushButton
    hands_hide_button: QPushButton
    quit = pyqtSignal()
    game_ended = pyqtSignal(int)
    
    def __init__(self, ui_path: Path, user_width: int, user_height: int):
        super().__init__()
        self.start_time: float = 0.0
        self.username = ''
        self.init_ui(ui_path, user_width, user_height)
        
    def init_ui(self, ui_path: Path, user_width: int, user_height: int):
        try:
            uic.loadUi(ui_path / 'ui' / 'game_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.record_confirm = RecordConfirm(user_width, user_height)
        self.record_confirm.record_confirm.connect(self.new_record)

        self.game_timer = QTimer()
        self.game_timer.setInterval(TIME_INTERVAL)
        self.game_timer.timeout.connect(self.update_timer)
        self.enable_input_timer = QTimer()
        self.enable_input_timer.setInterval(GAME_DELAY * 1000)
        self.enable_input_timer.setSingleShot(True)
        self.enable_input_timer.timeout.connect(self.enable_input)

        self.game_quit_button.clicked.connect(self.leave_game)
        self.keyboard_hide_button.clicked.connect(self.game_hide_keyboard)
        self.hands_hide_button.clicked.connect(self.game_hide_hands)

        self.input_text_line.right_input.connect(self.update_progress_bar)
        self.input_text_line.right_input.connect(self.displayed_text.update_text_displayment)
        self.input_text_line.game_ended.connect(self.stop_game)

    def open_confirm_record(self, symbs_per_min: int):
        self.record_confirm.show_for_confirm(self.username, symbs_per_min)

    def game_hide_keyboard(self):
        if self.keyboard_label.isHidden():
            self.keyboard_label.show()
            self.keyboard_hide_button.setStyleSheet('\n'.join(KEYBOARD_STYLE_SHEETS))
        else:
            self.keyboard_label.hide()
            style_sheets = list(KEYBOARD_STYLE_SHEETS)
            style_sheets[2] = 'border-image: url(:/icons/images/keyboard_off.png);'
            self.keyboard_hide_button.setStyleSheet('\n'.join(style_sheets))
        self.change_game_layout_stretch()

    def game_hide_hands(self):
        if self.right_hand_label.isHidden():
            self.right_hand_label.show()
            self.left_hand_label.show()
            self.hands_hide_button.setStyleSheet('\n'.join(HANDS_STYLE_SHEETS))
        else:
            self.right_hand_label.hide()
            self.left_hand_label.hide()
            style_sheets = list(HANDS_STYLE_SHEETS)
            style_sheets[2] = 'border-image: url(:/icons/images/hands_off.png);'
            self.hands_hide_button.setStyleSheet('\n'.join(style_sheets))
        self.change_game_layout_stretch()

    def change_game_layout_stretch(self):
        if self.keyboard_label.isHidden() and self.right_hand_label.isHidden():
            [self.central_layout.setStretch(i, j) for i, j in enumerate([0, 4, 2, 0, 3])]
        else:
            [self.central_layout.setStretch(i, j) for i, j in enumerate([0, 2, 1, 2, 1])]

    def set_displayed_text(self, text):
        self.progress_bar.setValue(0)
        self.displayed_text.set_level_text(text)
        self.input_text_line.set_level_text(text)

    def update_timer(self):
        if not self.start_time:
            return self.timer_label.setText('00:00')
        time = int((timestamp() - self.start_time) * 100)
        palette = QPalette()
        if time <= 0:
            palette.setColor(QPalette.WindowText, QColor(230, 2, 2))
            self.timer_label.setPalette(palette)
            self.timer_label.setText(f'{round(abs(time) / 100 % 60, 2):.2f}')
        else:
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            self.timer_label.setPalette(palette)
            self.timer_label.setText(f'{time // 6000}:{round(time / 100 % 60, 2):.2f}')

    def enable_input(self):
        self.input_text_line.switch_input(True)
        self.input_text_line.setFocus()

    def disable_input(self):
        self.input_text_line.switch_input(False)

    def update_progress_bar(self):
        now_text = self.input_text_line.get_level_text()
        full_text = self.displayed_text.get_level_text()
        self.progress_bar.setValue(round(100 - len(now_text) / len(full_text) * 100))

    def start_game(self, username: str):
        self.username = username
        self.enable_input_timer.start()
        self.start_time = timestamp() + GAME_DELAY
        self.game_timer.start()

    def leave_game(self):
        self.game_timer.stop()
        self.enable_input_timer.stop()
        self.disable_input()
        self.timer_label.setText('00:00')
        self.start_time = 0.0
        self.quit.emit()

    def stop_game(self):
        time_now = timestamp()
        symbs = len(self.displayed_text.get_level_text())
        symbs_per_minute = round(symbs / (time_now - self.start_time) * 60)
        self.leave_game()
        self.open_confirm_record(symbs_per_minute)

    def new_record(self, symbs_per_minute: int):
        self.game_ended.emit(symbs_per_minute)
