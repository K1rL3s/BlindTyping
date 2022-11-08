from PyQt5.QtWidgets import QLineEdit

from ..consts import DISPLAY_TEXT_LENGHT


class DisplayText(QLineEdit):
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
