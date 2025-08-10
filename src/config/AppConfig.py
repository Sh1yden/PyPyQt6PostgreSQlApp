# ===== APPLICATION CONFIGURATION CLASS / КЛАСС КОНФИГУРАЦИИ ПРИЛОЖЕНИЯ =====
# TODO: Add logger here / TODO как-то добавить логер сюда

# ===== IMPORTS / ИМПОРТЫ =====
import json
import os
from pathlib import Path


# ===== CONFIGURATION CLASS / КЛАСС КОНФИГУРАЦИИ =====
class AppConfig:
    """
    Application configuration and file management / Настройка и создание конфига для всей программы. Работа с файлами программы.
    Singleton pattern implementation for global settings / Реализация паттерна Singleton для глобальных настроек
    """

    # ===== SINGLETON PATTERN / ПАТТЕРН СИНГЛТОН =====
    _instanse_AppCfg = None  # Stores single instance / Хранит единственный экземпляр
    _initialized_AppCfg = False  # Single initialization flag / Флаг на единственную инициализацию

    # ===== SINGLETON CREATION / СОЗДАНИЕ СИНГЛТОНА =====
    def __new__(cls):
        """Create single class instance / Создание единого объекта класса"""
        if cls._instanse_AppCfg is None:
            # If no class instance exists, create one / Если экземпляра класса нет создаём
            cls._instanse_AppCfg = super().__new__(cls)
        return cls._instanse_AppCfg

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self):
        """Initialize configuration only once / Инициализация конфигурации только один раз"""
        if not AppConfig._initialized_AppCfg:
            # Successful constructor and class initialization / Успешная инициализация конструктора и класса
            AppConfig._initialized_AppCfg = True

            # ===== ERROR HANDLING / ОБРАБОТКА ОШИБОК =====
            # Protection from recursion and other internal errors / Защита от рекурсии и прочих внутренних ошибок
            # Activated automatically when errors occur / Которая включается сама при возникновении ошибок
            # ! Log files are not saved for internal class errors - check console!!! / ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            self._internal_error_occurred = False

            # ===== FILESYSTEM SETUP / НАСТРОЙКА ФАЙЛОВОЙ СИСТЕМЫ =====
            # Common directories / Общие папки
            self._CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            self._PROJECT_DIR = os.path.dirname(os.path.dirname(self._CURRENT_DIR))
            # Program settings directory / Папка настроек программы
            self._SAVE_SET_DIR = Path(f"{self._PROJECT_DIR}/src/config/settings/")

            # ===== LOGGING CONFIGURATION / КОНФИГУРАЦИЯ ЛОГИРОВАНИЯ =====
            # Log directory / Папка для логов
            self._SAVE_LG_DIR = Path(os.path.join(self._PROJECT_DIR, "logs"))
            # Log settings file / Настройки логов
            self._SAVE_SET_LG_FILE = Path(f"{self._SAVE_SET_DIR}/lg_settings.json")
            # Default log settings / Настройки логов по умолчанию
            self._LG_DEF_SET = {
                "lg_lvl_set": 0,
                "OFF": 0,
                "DEBUG": 10,
                "INFO": 20,
                "WARNING": 30,
                "ERROR": 40,
                "CRITICAL": 50
            }

            # ===== DATABASE CONFIGURATION / КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ =====
            # Database settings file / Настройки БД
            self._SAVE_SET_DB_FILE = Path(f"{self._SAVE_SET_DIR}/db_settings.json")
            # Default database settings / Настройки БД по умолчанию
            self._DB_DEF_SET = {
                "host": "localhost",
                "dbname": "Shcool App",
                "port": 5432,
                "user": "postgres",
                "password": "345627"
            }

            # ===== FILE INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ФАЙЛОВ =====
            self._init_files()

            # ===== RUNTIME CONFIGURATION / НАСТРОЙКА ВРЕМЕНИ ВЫПОЛНЕНИЯ =====
            # Logging level / Уровень логирования
            self._LG_ALL_SET = self.load_from_file(self._SAVE_SET_LG_FILE)
            self._LG_LVL = self._LG_ALL_SET["lg_lvl_set"]

    # ===== PROPERTY METHODS - LOGGING / МЕТОДЫ-СВОЙСТВА - ЛОГИРОВАНИЕ =====
    @property
    def save_lg_dir(self):
        """Get log directory path / Получить путь к папке логов"""
        return self._SAVE_LG_DIR

    @property
    def save_set_lg_file(self):
        """Get log settings file path / Получить путь к файлу настроек логов"""
        return self._SAVE_SET_LG_FILE

    @property
    def lg_all_set(self):
        """Get all log settings / Получить все настройки логов"""
        return self._LG_ALL_SET

    @property
    def lg_lvl(self):
        """Get current log level / Получить текущий уровень логирования"""
        return self._LG_LVL

    # ===== PROPERTY METHODS - DATABASE / МЕТОДЫ-СВОЙСТВА - БАЗА ДАННЫХ =====
    @property
    def save_set_db_file(self):
        """Get database settings file path / Получить путь к файлу настроек БД"""
        return self._SAVE_SET_DB_FILE

    # ===== FILE OPERATIONS / ОПЕРАЦИИ С ФАЙЛАМИ =====
    def _init_files(self):
        """Initialize directories and files for the program / Инициализация папок и файлов для программы. Настройки, папка для логов и т.д."""
        try:
            # ===== GENERAL SETUP / ОБЩАЯ НАСТРОЙКА =====
            # Create settings directory if it doesn't exist / Если папки настроек нет
            self._SAVE_SET_DIR.mkdir(parents=True, exist_ok=True)

            # ===== LOGGING SETUP / НАСТРОЙКА ЛОГИРОВАНИЯ =====
            # Create log directory if it doesn't exist / Если папки для логов нет
            self._SAVE_LG_DIR.mkdir(parents=True, exist_ok=True)
            # Create log settings file if it doesn't exist / Если файла настроек нет
            if not self._SAVE_SET_LG_FILE.exists():
                self.save_to_file(self._SAVE_SET_LG_FILE, self._LG_DEF_SET)

            # ===== DATABASE SETUP / НАСТРОЙКА БАЗЫ ДАННЫХ =====
            # Create database settings file / Создание файла настроек
            # Create settings file if it doesn't exist / Если файла настроек нет
            if not self._SAVE_SET_DB_FILE.exists():
                self.save_to_file(self._SAVE_SET_DB_FILE, self._DB_DEF_SET)

        except Exception as e:
            self._internal_error_occurred = True

    def load_from_file(self, file_path):
        """Load from file and return its contents / Загрузка из файла и возврат его содержания"""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self._internal_error_occurred = True

    def save_to_file(self, file_path, var):
        """Save value to file / Сохранение значения в файл"""
        try:
            with open(file_path, "w") as f:
                json.dump(var, f, indent=2)
        except Exception as e:
            self._internal_error_occurred = True


# ===== MAIN EXECUTION / ГЛАВНОЕ ВЫПОЛНЕНИЕ =====
if __name__ == '__main__':
    # Test configuration creation / Тестирование создания конфигурации
    appcfg = AppConfig()