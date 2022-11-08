from PyQt5.QtWidgets import QLineEdit

from ..consts import DISPLAY_TEXT_LENGHT


class DisplayText(QLineEdit):
    """
    Виджет отображения текста в GameWidget

    Используется для:
    1. Отображения текущего фрагмента текста;
    2. Получения всего текста уровня для изменения progress_bar'а;

    Сдвиг происходит после нажатия пробела в TypingFilterWidget
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.start = 0
        self.text = ''

    def set_level_text(self, text: str):
        self.start = 0
        self.text = text
        self.update_text_displayment(0)

    def get_level_text(self):
        return self.text

    def update_text_displayment(self, step):
        self.start += step
        self.setText(self.text[self.start:self.start + DISPLAY_TEXT_LENGHT])
