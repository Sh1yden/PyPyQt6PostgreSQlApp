from PyQt6.QtSql import QSqlDatabase
from src.core.Logger import Logger
import json
from pathlib import Path
import os


class Connection:
    """Класс подключения базы данных."""

    # Конструктор класса.
    def __init__(self):
        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Connection.")
        self.lg.debug("Logger created in class Connection().")

        # Указание файловой системы для программы.
        # Общие папки.
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_DIR = os.path.dirname(os.path.dirname(self.CURRENT_DIR))
        self.SAVE_DIR_DB = Path(f"{self.PROJECT_DIR}/src/config/settings/")
        # Файл настроек.
        self.SAVE_FILE_DB = Path(f"{self.SAVE_DIR_DB}/db_settings.json")

        # Работа с файлами.
        self.db_set_var = {}
        self._initialize_files()
        self.con_db()

    def _initialize_files(self):
        """Инициализация файлов и директорий для программы."""
        try:
            # Создаём директорию.
            self.SAVE_DIR_DB.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not self.SAVE_FILE_DB.exists():
                self._save_to_file()
        except Exception as e:
            self.lg.critical(f"Connection internal error: {e}. In DEF _initialize_files()")

    def _load_from_file(self):
        """Загрузка данных из файла настроек."""
        try:
            with open(self.SAVE_FILE_DB, "r") as f:
                self.db_set_var = json.load(f)
        except Exception as e:
            self.lg.critical(f"Connection internal error: {e}. In DEF load_from_file()")

    def _save_to_file(self):
        """Загрузка данных в файл настроек."""
        try:
            # TODO сделать авто ввод данных бд на выбор, либо пользователь, либо авто
            with open(self.SAVE_FILE_DB, "w") as f:
                json.dump(self.db_set_var, f, indent=2)
        except Exception as e:
            self.lg.critical(f"Connection internal error: {e}. In DEF _save_to_file()")

    def con_db(self):
        try:
            self._load_from_file()
            # Не подлючение к базе данных, а задание параметров для неё.
            db = QSqlDatabase.addDatabase("QPSQL")
            db.setHostName(self.db_set_var["db_settings"]["db_host_name"])
            db.setDatabaseName(self.db_set_var["db_settings"]["db_name"])
            db.setPort(self.db_set_var["db_settings"]["db_port"])
            db.setUserName(self.db_set_var["db_settings"]["db_user"])
            db.setPassword(self.db_set_var["db_settings"]["db_password"])
            # Подключение к базе данных.
            ok = db.open()
            if ok:
                self.lg.debug("Connected to DB")
            else:
                self.lg.error("Connection FAILED")
        except Exception as e:
            self.lg.critical(f"Connection internal error: {e}. In DEF connect_db()")
