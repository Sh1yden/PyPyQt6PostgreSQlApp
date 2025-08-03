# TODO как-то добавить логер сюда
import json
import os
from pathlib import Path


class AppConfig:
    """Настройка и создание конфига для всей программы. Работа с файлами программы."""

    _instanse_AppCfg = None # Хранит единственный экземпляр.
    _initialized_AppCfg = False # Флаг на единственную инициализацию.

    # Создание единого объекта класса.
    def __new__(cls):
        if cls._instanse_AppCfg is None:
            # Если экземпляра класса нет создаём.
            cls._instanse_AppCfg = super().__new__(cls)

        return cls._instanse_AppCfg

    def __init__(self):
        if not AppConfig._initialized_AppCfg:
            # Успешная инициализация конструктора и класса.
            AppConfig._initialized_AppCfg = True

            # Ошибки.
            # * Защита от рекурсии и прочих внутренних ошибок.
            # Которая включается сама при возникновении ошибок.
            # ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            self._internal_error_occurred = False


            # Указание файловой системы для программы.
            # Общие папки.
            self._CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            self._PROJECT_DIR = os.path.dirname(os.path.dirname(self._CURRENT_DIR))
            # Папка настроек программы
            self._SAVE_SET_DIR = Path(f"{self._PROJECT_DIR}/src/config/settings/")


            # Логи
            # Папка для логов
            self.SAVE_LG_DIR = Path(os.path.join(self._PROJECT_DIR, "logs"))
            # Настройки логов
            self.SAVE_SET_LG_FILE = Path(f"{self._SAVE_SET_DIR}/lg_settings.json")
            self._LG_DEF_SET = {
                "lg_lvl_set" : 0,
                "OFF" : 0,
                "DEBUG" : 10,
                "INFO" : 20,
                "WARNING": 30,
                "ERROR": 40,
                "CRITICAL": 50
            }


            # БД
            # Настройки БД
            self.SAVE_SET_DB_FILE = Path(f"{self._SAVE_SET_DIR}/db_settings.json")
            self._DB_DEF_SET = {
                "host": "localhost",
                "dbname": "Shcool App",
                "port": 5432,
                "user": "postgres",
                "password": "345627"
            }

            # Инициализация файлов
            self._init_files()

            # Уровень логирования
            self.LG_ALL_SET = self.load_from_file(self.SAVE_SET_LG_FILE)
            self.LG_LVL = self.LG_ALL_SET["lg_lvl_set"]

    def _init_files(self):
        """Инициализация папок и файлов для программы. Настройки, папка для логов и т.д."""
        try:
            # Общее
            # Если папки настроек нет
            self._SAVE_SET_DIR.mkdir(parents=True, exist_ok=True)

            # Логи
            # Если папки для логов нет
            self.SAVE_LG_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла настроек нет
            if not self.SAVE_SET_LG_FILE.exists():
                self.save_to_file(self.SAVE_SET_LG_FILE, self._LG_DEF_SET)

            # БД
            # Создание файла настроек
            # Если файла настроек нет
            if not self.SAVE_SET_DB_FILE.exists():
                self.save_to_file(self.SAVE_SET_DB_FILE, self._DB_DEF_SET)
        except Exception as e:
            self._internal_error_occurred = True

    def load_from_file(self, file_path):
        """Загрузка из файла и возврат его содержания."""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self._internal_error_occurred = True

    def save_to_file(self, file_path, var):
        """Сохранение значения в файл."""
        try:
            with open(file_path, "w") as f:
                json.dump(var, f, indent=2)
        except Exception as e:
            self._internal_error_occurred = True

if __name__ == '__main__':
    appcfg = AppConfig()
