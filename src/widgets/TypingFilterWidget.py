from PyQt5.Qt import QKeySequence
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QKeyEvent

from ..consts import DISPLAY_TEXT_LENGHT


class TypingFilter(QLineEdit):
    """
    Виджет ввода текста

    Не позволяет ввести неверный символ.
    Создаёт сигнал правильного ввода в случае, когда пользователь ввёл верное слово (пробел)
    или ввёл текст равный длине максимального отображения на экране.
    Создаёт сигнал конца игры, когда весь текст уровня был введён.
    """
    game_ended = pyqtSignal()
    right_input = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.level_text = ''
        self.is_game_end = False
        self.textChanged.connect(self.input_filter)

    def switch_input(self, switch: bool):
        self.setEnabled(switch)

    def set_level_text(self, text):
        self.setText('')
        self.level_text = text

    def get_level_text(self):
        return self.level_text

    def input_filter(self):
        text = self.text()
        if not text:
            return

        last_symb = text[-1]
        if self.level_text[len(text) - 1] != last_symb:
            self.setText(text[:-1])
            return

        if last_symb == ' ' or len(text) >= DISPLAY_TEXT_LENGHT:
            if text == self.level_text:
                self.game_ended.emit()
                return
            self.level_text = self.level_text[len(text):]
            self.setText('')
            self.right_input.emit(len(text))
            return

        if text == self.level_text:
            self.game_ended.emit()

    # Обработка ctrl+v
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == QKeySequence.Paste:
            event.ignore()
        else:
            self.setText(self.text() + event.text())

