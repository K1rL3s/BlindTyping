import sqlite3

from src.consts import ModeNames
from src.main_funcs import normalize_text


class Database:
    """
    Класс базы данных.

    Умеет:
    1. Инициировать необходимые для работы таблицы.
    2. Добавлять и возвращать рекорды;
    3. Добавлять, изменять, удалять и возвращать кастомные уровни.
    """
    def __init__(self, database_name: str = 'records.db'):
        self.db = sqlite3.connect(database_name, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.init_tables()
        self.init_modes()

    def init_tables(self):
        for table in (CUSTOM_LEVELS_TABLE, MODES_TABLE, RECORDS_TABLE):
            self.cursor.execute(table)
            self.db.commit()

    def init_modes(self):
        modes_now = [i[0] for i in self.cursor.execute("SELECT title FROM modes").fetchall()]
        for title in ModeNames:
            if title.value not in modes_now:
                self.cursor.execute('INSERT INTO modes (title) VALUES (?)', (title.value,))
                self.db.commit()

    def add_new_record(self, name: str, record: int, mode_name: str):
        self.cursor.execute(f"INSERT INTO records VALUES (?, ?, (SELECT id FROM modes WHERE title = ?))",
                            (normalize_text(name), record, mode_name))
        self.db.commit()

    def get_records(self, mode_name: str) -> list[tuple[str, int]]:
        data = self.cursor.execute("""SELECT name, result FROM records WHERE mode_id =
                                      (SELECT id FROM modes WHERE title = ?)
                                      ORDER BY result DESC """, (mode_name,)).fetchall()
        return data if data else []

    def get_custom_levels(self) -> list[tuple[str, str]]:
        data = self.cursor.execute("SELECT title, content FROM custom_levels ORDER BY id").fetchall()
        return data if data else []

    def get_custom_level(self, title: str) -> list[int, str, str]:
        data = self.cursor.execute("SELECT * FROM custom_levels WHERE title = ?", (title,)).fetchone()
        return data if data else []

    def add_custom_level(self, title: str, content: str):
        if self.cursor.execute("SELECT * FROM custom_levels WHERE title = ?", (title,)).fetchall():
            return False
        self.cursor.execute("INSERT INTO custom_levels (title, content) VALUES (?, ?)",
                            (normalize_text(title), normalize_text(content)))
        self.db.commit()
        return True

    def delete_custom_level(self, level_id: int):
        self.cursor.execute("DELETE FROM custom_levels WHERE id = ?", (level_id,))
        self.db.commit()

    def update_custom_level(self, level_id: int, title: str, content: str):
        level = self.get_custom_level(title)
        if level and level[0] != level_id:
            return False
        self.cursor.execute("UPDATE custom_levels SET title = ?, content = ? WHERE id = ?",
                            (normalize_text(title), normalize_text(content), level_id))
        self.db.commit()
        return True

    def close(self):
        self.db.close()


CUSTOM_LEVELS_TABLE = """
                      CREATE TABLE IF NOT EXISTS "custom_levels" (
                          "id" INTEGER NOT NULL UNIQUE,
                          "title" TEXT NOT NULL UNIQUE,
                          "content" TEXT NOT NULL,
                          PRIMARY KEY("id" AUTOINCREMENT)
                      )"""
MODES_TABLE = """
              CREATE TABLE IF NOT EXISTS "modes" (
                  "id" INTEGER NOT NULL UNIQUE,
                  "title" TEXT NOT NULL UNIQUE,
                  PRIMARY KEY("id" AUTOINCREMENT)
              )"""
RECORDS_TABLE = """
                CREATE TABLE IF NOT EXISTS "records" (
                    "name" TEXT NOT NULL,
                    "result" INTEGER NOT NULL,
                    "mode_id" INTEGER NOT NULL,
                    FOREIGN KEY("mode_id") REFERENCES "modes"("id")
                )"""