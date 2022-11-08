from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

from src.ui_files import Main_UI


class MainMenu(QWidget, Main_UI):
    """
    Стартово меню

    Просто кнопочки других менюшек и сигналы от их нажатия.
    """
    startgame_button: QPushButton
    settings_button: QPushButton
    record_button: QPushButton
    quit_button: QPushButton
    open_pregame = pyqtSignal()
    open_settings = pyqtSignal()
    open_records = pyqtSignal()
    close_app = pyqtSignal()

    def __init__(self, ui_path: Path):
        super().__init__()
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'main_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.startgame_button.clicked.connect(self.open_pregame.emit)
        self.settings_button.clicked.connect(self.open_settings.emit)
        self.record_button.clicked.connect(self.open_records.emit)
        self.quit_button.clicked.connect(self.close_app.emit)
