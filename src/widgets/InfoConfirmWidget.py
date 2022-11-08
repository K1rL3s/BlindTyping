from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from ..consts import CONFIRM_INFO_FONT


class InfoConfirm(QWidget):
    """
    Виджет подтверждения информации.

    Самый переиспользуемый класс из всех представленных, моя гордость.
    Нужен лишь для нажатия "OK".
    """
    def __init__(self, window_title: str, label_text: str, user_width: int, user_height: int):
        super().__init__()
        self.init_ui(window_title, label_text, user_width, user_height)

    def init_ui(self, window_title: str, qlabel_text: str, user_width: int, user_height: int):
        self.setWindowTitle(window_title)
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout()
        lbl = QLabel(qlabel_text, self)
        lbl.setFont(CONFIRM_INFO_FONT)
        lbl.adjustSize()
        btn_ok = QPushButton('OK', self)
        btn_ok.setFont(CONFIRM_INFO_FONT)
        btn_ok.clicked.connect(self.close)
        btn_ok.adjustSize()
        btn_ok.setShortcut("Return")  # "Enter" Key
        hlayout.addWidget(btn_ok)
        layout.addWidget(lbl)
        layout.addLayout(hlayout)
        sizehint = self.sizeHint()
        width, height = sizehint.width(), sizehint.height()
        self.setGeometry((user_width - width) // 2, (user_height - height) // 2, width, height)
        self.show()
