from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

from ..consts import CONFIRM_INFO_FONT, RECORD_CONFIRM_TITLE, RECORD_CONFIRM_CONTENT


# Просто красивое подтверждение результата после игры
class RecordConfirm(QWidget):
    record_confirm = pyqtSignal(int)

    def __init__(self, user_width: int, user_height: int):
        super().__init__()
        self.symbs_per_min = 0
        self.user_width = user_width
        self.user_height = user_height
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(RECORD_CONFIRM_TITLE)
        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setFont(CONFIRM_INFO_FONT)
        layout.addWidget(self.label)
        hlayout = QHBoxLayout()
        btn_ok = QPushButton('ОК')
        btn_ok.setFont(CONFIRM_INFO_FONT)
        btn_ok.clicked.connect(self.confirmed)
        btn_no = QPushButton('NO')
        btn_no.setFont(CONFIRM_INFO_FONT)
        btn_no.clicked.connect(self.close)
        hlayout.addWidget(btn_ok)
        hlayout.addWidget(btn_no)
        layout.addLayout(hlayout)

    def confirmed(self):
        self.record_confirm.emit(self.symbs_per_min)
        self.close()

    def show_for_confirm(self, user_name: str, symbs_per_min: int):
        self.label.setText(RECORD_CONFIRM_CONTENT.format(user_name, symbs_per_min))
        self.symbs_per_min = symbs_per_min
        sizehint = self.sizeHint()
        width, height = sizehint.width(), sizehint.height()
        self.setGeometry((self.user_width - width) // 2, (self.user_height - height) // 2, width, height)
        self.show()
