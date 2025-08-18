# ===== APPLICATION CONFIGURATION CLASS / КЛАСС КОНФИГУРАЦИИ ПРИЛОЖЕНИЯ =====
# Application configuration and file management class
# Класс конфигурации приложения и управления файлами
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

    This class manages application configuration files, directories and settings.
    It implements the Singleton pattern to ensure only one instance exists.

    Этот класс управляет конфигурационными файлами приложения, директориями и настройками.
    Он реализует паттерн Singleton для обеспечения существования только одного экземпляра.
    """

    # ===== SINGLETON PATTERN IMPLEMENTATION / РЕАЛИЗАЦИЯ ПАТТЕРНА СИНГЛТОН =====
    _instanse_AppCfg = None  # Stores single instance / Хранит единственный экземпляр
    _initialized_AppCfg = False  # Single initialization flag / Флаг на единственную инициализацию

    # ===== SINGLETON CREATION METHOD / МЕТОД СОЗДАНИЯ СИНГЛТОНА =====
    def __new__(cls):
        """
        Create single class instance / Создание единого объекта класса

        Ensures only one instance of AppConfig exists throughout the application lifecycle.
        Обеспечивает существование только одного экземпляра AppConfig в течение жизни приложения.

        Returns:
            AppConfig: Single instance of the configuration class
        """
        if cls._instanse_AppCfg is None:
            # If no class instance exists, create one / Если экземпляра класса нет создаём
            cls._instanse_AppCfg = super().__new__(cls)
        return cls._instanse_AppCfg

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self):
        """
        Initialize configuration only once / Инициализация конфигурации только один раз

        Initializes all configuration parameters, file paths, and creates necessary directories.
        Sets up logging and database configuration with default values.

        Инициализирует все параметры конфигурации, пути к файлам и создает необходимые директории.
        Настраивает логирование и конфигурацию базы данных со значениями по умолчанию.
        """
        if not AppConfig._initialized_AppCfg:
            # Successful constructor and class initialization / Успешная инициализация конструктора и класса
            AppConfig._initialized_AppCfg = True

            # ===== ERROR HANDLING SETUP / НАСТРОЙКА ОБРАБОТКИ ОШИБОК =====
            # Protection from recursion and other internal errors / Защита от рекурсии и прочих внутренних ошибок
            # Activated automatically when errors occur / Которая включается сама при возникновении ошибок
            # ! Log files are not saved for internal class errors - check console!!! / ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            # Internal error flag to prevent infinite recursion during error handling
            # Флаг внутренней ошибки для предотвращения бесконечной рекурсии при обработке ошибок
            self._internal_error_occurred = False

            # ===== FILESYSTEM CONFIGURATION / НАСТРОЙКА ФАЙЛОВОЙ СИСТЕМЫ =====
            # Common directories setup / Настройка общих папок
            self._CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            self._PROJECT_DIR = os.path.dirname(os.path.dirname(self._CURRENT_DIR))
            # Program settings directory / Папка настроек программы
            self._SAVE_SET_DIR = Path(f"{self._PROJECT_DIR}/src/config/settings/")

            # ===== LOGGING CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ ЛОГИРОВАНИЯ =====
            # Log directory path / Путь к папке для логов
            self._SAVE_LG_DIR = Path(os.path.join(self._PROJECT_DIR, "logs"))
            # Log settings file path / Путь к файлу настроек логов
            self._SAVE_SET_LG_FILE = Path(f"{self._SAVE_SET_DIR}/lg_settings.json")
            # Default log settings dictionary / Словарь настроек логов по умолчанию
            self._LG_DEF_SET = {
                "lg_lvl_set": 0,    # Default logging level / Уровень логирования по умолчанию
                "OFF": 0,           # Logging disabled / Логирование отключено
                "DEBUG": 10,        # Debug level / Уровень отладки
                "INFO": 20,         # Information level / Информационный уровень
                "WARNING": 30,      # Warning level / Уровень предупреждений
                "ERROR": 40,        # Error level / Уровень ошибок
                "CRITICAL": 50      # Critical level / Критический уровень
            }

            # ===== DATABASE CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ БАЗЫ ДАННЫХ =====
            # Database settings file path / Путь к файлу настроек БД
            self._SAVE_SET_DB_FILE = Path(f"{self._SAVE_SET_DIR}/db_settings.json")
            # Default database connection settings / Настройки подключения к БД по умолчанию
            self._DB_DEF_SET = {
                "host": "localhost",        # Database server host / Хост сервера базы данных
                "dbname": "Shcool App",     # Database name / Имя базы данных
                "port": 5432,               # Database port / Порт базы данных
                "user": "postgres",         # Database user / Пользователь базы данных
                "password": "345627"        # Database password / Пароль базы данных
            }

            # ===== FILE AND DIRECTORY INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ФАЙЛОВ И ДИРЕКТОРИЙ =====
            self._init_files()

            # ===== RUNTIME CONFIGURATION LOADING / ЗАГРУЗКА КОНФИГУРАЦИИ ВРЕМЕНИ ВЫПОЛНЕНИЯ =====
            # Load all logging settings from file / Загрузка всех настроек логирования из файла
            self._LG_ALL_SET = self.load_from_file(self._SAVE_SET_LG_FILE)
            # Current logging level / Текущий уровень логирования
            self._LG_LVL = self._LG_ALL_SET["lg_lvl_set"]

    # ===== PROPERTY METHODS - LOGGING CONFIGURATION / МЕТОДЫ-СВОЙСТВА - КОНФИГУРАЦИЯ ЛОГИРОВАНИЯ =====

    @property
    def save_lg_dir(self) -> Path | None:
        """
        Get log directory path / Получить путь к папке логов

        Returns:
            Path: Path to the logs directory
        """
        return self._SAVE_LG_DIR

    @property
    def save_set_lg_file(self) -> Path | None:
        """
        Get log settings file path / Получить путь к файлу настроек логов

        Returns:
            Path: Path to the log settings file
        """
        return self._SAVE_SET_LG_FILE

    @property
    def lg_all_set(self) -> dict | None:
        """
        Get all log settings / Получить все настройки логов

        Returns:
            dict: Dictionary containing all logging settings
        """
        return self._LG_ALL_SET

    @property
    def lg_lvl(self) -> int | None:
        """
        Get current log level / Получить текущий уровень логирования

        Returns:
            int: Current logging level value
        """
        return self._LG_LVL

    # ===== PROPERTY METHODS - DATABASE CONFIGURATION / МЕТОДЫ-СВОЙСТВА - КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ =====

    @property
    def save_set_db_file(self) -> Path | None:
        """
        Get database settings file path / Получить путь к файлу настроек БД

        Returns:
            Path: Path to the database settings file
        """
        return self._SAVE_SET_DB_FILE

    # ===== PRIVATE METHODS - FILE OPERATIONS / ПРИВАТНЫЕ МЕТОДЫ - ОПЕРАЦИИ С ФАЙЛАМИ =====

    def _init_files(self) -> None:
        """
        Initialize directories and files for the program / Инициализация папок и файлов для программы. Настройки, папка для логов и т.д.

        Creates necessary directories and configuration files if they don't exist.
        Sets up the basic file structure required for the application to function properly.

        Создает необходимые директории и конфигурационные файлы, если они не существуют.
        Настраивает базовую файловую структуру, необходимую для правильной работы приложения.
        """
        try:
            # ===== GENERAL DIRECTORY SETUP / ОБЩАЯ НАСТРОЙКА ДИРЕКТОРИЙ =====
            # Create settings directory if it doesn't exist / Создание папки настроек, если она не существует
            self._SAVE_SET_DIR.mkdir(parents=True, exist_ok=True)

            # ===== LOGGING SETUP / НАСТРОЙКА ЛОГИРОВАНИЯ =====
            # Create log directory if it doesn't exist / Создание папки для логов, если она не существует
            self._SAVE_LG_DIR.mkdir(parents=True, exist_ok=True)
            # Create log settings file with defaults if it doesn't exist / Создание файла настроек логов со значениями по умолчанию, если он не существует
            if not self._SAVE_SET_LG_FILE.exists():
                self.save_to_file(self._SAVE_SET_LG_FILE, self._LG_DEF_SET)

            # ===== DATABASE SETUP / НАСТРОЙКА БАЗЫ ДАННЫХ =====
            # Create database settings file with defaults if it doesn't exist / Создание файла настроек БД со значениями по умолчанию, если он не существует
            if not self._SAVE_SET_DB_FILE.exists():
                self.save_to_file(self._SAVE_SET_DB_FILE, self._DB_DEF_SET)

        except Exception as e:
            # Set internal error flag to prevent infinite recursion / Установка флага внутренней ошибки для предотвращения бесконечной рекурсии
            self._internal_error_occurred = True

    # ===== PUBLIC METHODS - FILE OPERATIONS / ПУБЛИЧНЫЕ МЕТОДЫ - ОПЕРАЦИИ С ФАЙЛАМИ =====

    def load_from_file(self, file_path: Path, mode="r") -> dict | None:
        """
        Load data from JSON file and return its contents / Загрузка данных из JSON файла и возврат его содержания

        Args:
            file_path (Path): Path to the file to load from

        Returns:
            dict: Loaded data from the file, or None if error occurs
        """
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # Set error flag and return None on failure / Установка флага ошибки и возврат None при неудаче
            self._internal_error_occurred = True

    def save_to_file(self, file_path: Path,  var: dict,  jsonl: bool = False, mode: str="w") -> None:
        """
        Save value to JSON file / Сохранение значения в JSON файл
        And Save value to JSONL file / Сохранение значения в JSONL файл

        Args:
            file_path (Path): Path to the file to save to
            var (dict): Data to save to the file
            mode (str): File open mode (used only for JSON). Defaults to "w".
                    Режим открытия файла (используется только для JSON).
            jsonl (bool): If True, save in JSONL format (one object per line).
                          Если True, сохраняет в формате JSONL (по объекту на строку).
        """
        try:
            if jsonl:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(var, ensure_ascii=False) + "\n")
            else:
                with open(file_path, mode, encoding="utf-8") as f:
                    json.dump(var, f, ensure_ascii=False)
        except Exception as e:
            # Set error flag on failure / Установка флага ошибки при неудаче
            self._internal_error_occurred = True


# ===== MAIN EXECUTION BLOCK / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ =====
if __name__ == '__main__':
    # Test configuration creation / Тестирование создания конфигурации
    # This block is used for testing the AppConfig class functionality
    # Этот блок используется для тестирования функциональности класса AppConfig
    appcfg = AppConfig()