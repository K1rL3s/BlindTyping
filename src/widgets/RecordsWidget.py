from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QLabel

from src.ui_files import Record_UI
from ..database import Database
from ..consts import PLACES, RECORDS_FOUND, RECORDS_NOT_FOUND, RECORDS_WIDGET_COLUMNS, RECORD_RESULT


# Меню с отображением рекордов
class RecordsMenu(QWidget, Record_UI):
    record_quit_button: QPushButton
    record_words_button: QPushButton
    record_nums_button: QPushButton
    record_letters_button: QPushButton
    record_customs_button: QPushButton
    record_info_label: QLabel
    record_table: QTableWidget
    quit = pyqtSignal()

    def __init__(self,  ui_path: Path, db: Database):
        super().__init__()
        self.database = db
        self.init_ui(ui_path)

    def init_ui(self, ui_path: Path):
        try:
            uic.loadUi(ui_path / 'ui' / 'record_menu.ui', self)
        except FileNotFoundError:
            super().setupUi(self)
        self.record_quit_button.clicked.connect(self.quit.emit)
        self.record_words_button.clicked.connect(self.update_record_table)
        self.record_nums_button.clicked.connect(self.update_record_table)
        self.record_letters_button.clicked.connect(self.update_record_table)
        self.record_customs_button.clicked.connect(self.update_record_table)

    # def update_all_tables(self):
    #     for btn in (self.record_words_button, self.record_letters_button, self.record_nums_button):
    #         btn.click()

    def update_record_table(self):
        mode_name = self.sender().text().lower().strip()
        values = self.database.get_records(mode_name)
        self.record_table.setRowCount(len(values))
        if not values:
            return self.record_info_label.setText(RECORDS_NOT_FOUND)
        self.record_info_label.setText(RECORDS_FOUND.format(mode_name, len(values)))
        self.record_table.setColumnCount(len(values[0]))
        self.record_table.setHorizontalHeaderLabels(RECORDS_WIDGET_COLUMNS)
        for i, row in enumerate(values):
            name, record = row
            self.record_table.setItem(i, 0, QTableWidgetItem(name))
            self.record_table.setItem(i, 1, QTableWidgetItem(RECORD_RESULT.format(record)))
        self.record_table.resizeColumnsToContents()
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.paint_record_table(values)

    def paint_record_table(self, values: list[tuple[str, int]]):
        current_record = values[0][1]
        current_place = 0
        current_row = 0
        for row in values:
            record = row[1]
            if current_record != record:
                current_record = record
                current_place += 1
            if current_place > 2:
                break
            self.record_table.item(current_row, 0).setBackground(PLACES[current_place])
            self.record_table.item(current_row, 1).setBackground(PLACES[current_place])
            current_row += 1
