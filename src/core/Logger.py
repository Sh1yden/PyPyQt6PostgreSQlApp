# ===== PROGRAM LOGGING CLASS / КЛАСС ЛОГИРОВАНИЯ ПРОГРАММЫ =====
# Unified logging system for the entire application
# Унифицированная система логирования для всего приложения

# ===== IMPORTS / ИМПОРТЫ =====
import datetime
from pathlib import Path
import os
import sys
import inspect
from src.config.AppConfig import AppConfig


# ===== LOGGER CLASS / КЛАСС ЛОГГЕРА =====
class Logger:
    """
    Program logging class / Класс логирования программы
    Singleton pattern implementation for unified logging / Реализация паттерна Singleton для унифицированного логирования

    This class provides centralized logging functionality for the entire application.
    It implements the Singleton pattern to ensure consistent logging across all modules.
    Supports multiple log levels and automatic file management.

    Этот класс предоставляет централизованную функциональность логирования для всего приложения.
    Он реализует паттерн Singleton для обеспечения последовательного логирования во всех модулях.
    Поддерживает несколько уровней логирования и автоматическое управление файлами.
    """

    # ===== SINGLETON PATTERN IMPLEMENTATION / РЕАЛИЗАЦИЯ ПАТТЕРНА СИНГЛТОН =====
    _instanse_Logger = None  # Stores single instance / Хранит единственный экземпляр
    _initialized_Logger = False  # Single initialization flag / Флаг на единственную инициализацию

    # ===== SINGLETON CREATION METHOD / МЕТОД СОЗДАНИЯ СИНГЛТОНА =====
    def __new__(cls):
        """
        Create single class instance / Создание единого объекта класса

        Ensures only one Logger instance exists throughout the application lifecycle.
        This prevents multiple log files and maintains consistency.

        Обеспечивает существование только одного экземпляра Logger в течение жизни приложения.
        Это предотвращает создание множественных лог-файлов и поддерживает согласованность.

        Returns:
            Logger: Single instance of the logger class
        """
        if cls._instanse_Logger is None:
            # If no class instance exists, create one / Если экземпляра класса нет создаём
            cls._instanse_Logger = super().__new__(cls)
        return cls._instanse_Logger

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self):
        """
        Class constructor / Конструктор класса

        Initializes the logger with configuration from AppConfig.
        Sets up file paths, date formatting, and internal error handling.

        Инициализирует логгер с конфигурацией из AppConfig.
        Настраивает пути к файлам, форматирование даты и обработку внутренних ошибок.
        """
        if not Logger._initialized_Logger:
            # Successful constructor and class initialization / Успешная инициализация конструктора и класса
            Logger._initialized_Logger = True

            # ===== ERROR HANDLING SETUP / НАСТРОЙКА ОБРАБОТКИ ОШИБОК =====
            # Protection from recursion and other internal errors / Защита от рекурсии и прочих внутренних ошибок
            # Activated automatically when errors occur / Которая включается сама при возникновении ошибок
            # ! Log files are not saved for internal class errors - check console!!! / ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            # Internal error flag prevents infinite recursion during logging operations
            # Флаг внутренней ошибки предотвращает бесконечную рекурсию во время операций логирования
            self._internal_error_occurred = False

            # ===== CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ =====
            # Load application configuration for logging settings / Загрузка конфигурации приложения для настроек логирования
            self._appcfg = AppConfig()

            # ===== DATE AND FILE SETUP / НАСТРОЙКА ДАТЫ И ФАЙЛОВ =====
            # Current date for log file naming / Текущая дата для именования файлов логов
            self._DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
            # Log file name for program runtime, to avoid creating new ones / Имя файла логов на время выполнения программы, чтобы новые не создавать
            self._DEF_STRUCTURE = {}
            self._NAME_OF_LOG = self._name_of_logs()
            # Temporary buffer for log data / Временный буфер для данных логов
            self._lg_var = {}

    # ===== PRIVATE METHODS - FILE MANAGEMENT / ПРИВАТНЫЕ МЕТОДЫ - УПРАВЛЕНИЕ ФАЙЛАМИ =====

    def _name_of_logs(self):
        """
        Create unique log file name based on date and sequence / Создание уникального имени файла логов на основе даты и последовательности

        Generates log file names with format: YYYY-MM-DD-XX.json where XX is a sequence number.
        This prevents overwriting existing log files and maintains chronological order.

        Генерирует имена файлов логов в формате: YYYY-MM-DD-XX.json, где XX - порядковый номер.
        Это предотвращает перезапись существующих файлов логов и поддерживает хронологический порядок.

        Returns:
            Path: Complete path to the new log file
        """
        try:
            # Get list of existing log files / Получение списка существующих файлов логов
            logs_list = os.listdir(self._appcfg.save_lg_dir)

            # If no files in directory, set name with 01 / Если файлов в директории нет, задаём имя с 01
            if len(logs_list) < 1:
                save_file_name = Path(f"{self._appcfg.save_lg_dir}/{self._DATE}-{"01"}.jsonl")
            else:
                # Otherwise give name + 1 from existing maximum in directory / Иначе выдаём имя + 1 от существующего максимального в директории
                # Create list with sequential values 01, 02, etc. / Создание списка с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # Format sequence number with leading zero if needed / Форматирование порядкового номера с ведущим нулем при необходимости
                next_sequence = int(max(name_logs_list)) + 1
                if next_sequence < 10:
                    save_file_name = Path(
                        f"{self._appcfg.save_lg_dir}/{self._DATE}-0{next_sequence}.jsonl"
                    )
                else:
                    save_file_name = Path(
                        f"{self._appcfg.save_lg_dir}/{self._DATE}-{next_sequence}.jsonl"
                    )

            return save_file_name
        except Exception as e:
            # Set error flag and log to console as fallback / Установка флага ошибки и логирование в консоль как резервный вариант
            self._internal_error_occurred = True
            self.critical(f"Internal error: {e}")

    # ===== PRIVATE METHODS - CORE LOGGING / ПРИВАТНЫЕ МЕТОДЫ - ОСНОВНОЕ ЛОГИРОВАНИЕ =====

    def _univ_log(self, message: str, tag: str):
        """
        Universal logging template to avoid code repetition / Универсальный шаблон логирования, чтобы не повторять код

        Core logging method that handles timestamp generation, console output, and file writing.
        Provides protection against internal errors and recursion.

        Основной метод логирования, который обрабатывает генерацию временных меток, вывод в консоль и запись в файл.
        Обеспечивает защиту от внутренних ошибок и рекурсии.

        Args:
            message (str): Message to log / Сообщение для логирования
            tag (str): Log level tag (DEBUG, INFO, etc.) / Тег уровня логирования (DEBUG, INFO и т.д.)
        """
        stack = inspect.stack()
        caller_frame = stack[2].frame

        # Generate timestamp with millisecond precision / Генерация временной метки с точностью до миллисекунд
        current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
        file_name = Path(inspect.getfile(caller_frame)).name
        module = inspect.getmodule(caller_frame).__name__
        deff = caller_frame.f_code.co_name
        cls_obj = caller_frame.f_locals.get("self", None)
        cls_name = cls_obj.__class__.__name__ if cls_obj else None

        self._DEF_STRUCTURE = {
            "timestamp": current_time,
            "level": tag,
            "filename": file_name,
            "module": module,
            "class": cls_name,
            "def": deff,
            "message": message
        }

        # Protection from internal class errors and recursion / Защита от внутренних ошибок класса и рекурсии
        if self._internal_error_occurred:
            print(self._DEF_STRUCTURE, file=sys.stderr)
            return

        try:
            # Output to console for immediate feedback / Вывод в консоль для немедленной обратной связи
            print(self._DEF_STRUCTURE, file=sys.stderr)
            self._appcfg.save_to_log(self._NAME_OF_LOG, self._DEF_STRUCTURE)
        except Exception as e:
            # Set error flag and attempt fallback logging / Установка флага ошибки и попытка резервного логирования
            self._internal_error_occurred = True
            self.critical(f"Internal error: {e}")

    # ===== PUBLIC METHODS - LOG LEVELS / ПУБЛИЧНЫЕ МЕТОДЫ - УРОВНИ ЛОГИРОВАНИЯ =====

    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        """
        Debug level logging / Логирование уровня отладки

        Used for detailed diagnostic information, typically only of interest during development.
        Only logged if the current log level is DEBUG or lower.

        Используется для подробной диагностической информации, обычно интересной только во время разработки.
        Логируется только если текущий уровень логирования DEBUG или ниже.

        Args:
            message (str): Debug message to log / Отладочное сообщение для логирования
            tag (str): Custom tag for the message / Пользовательский тег для сообщения
        """
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["DEBUG"]:
            self._univ_log(message=message, tag=tag)

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        """
        Info level logging / Логирование информационного уровня

        Used for general information about program execution flow.
        Confirms that things are working as expected.

        Используется для общей информации о ходе выполнения программы.
        Подтверждает, что всё работает как ожидается.

        Args:
            message (str): Information message to log / Информационное сообщение для логирования
            tag (str): Custom tag for the message / Пользовательский тег для сообщения
        """
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["INFO"]:
            self._univ_log(message=message, tag=tag)

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        """
        Warning level logging / Логирование уровня предупреждений

        Used when something unexpected happened, or when a problem might occur in the future.
        The software is still working as expected.

        Используется когда произошло что-то неожиданное, или когда проблема может возникнуть в будущем.
        Программное обеспечение всё ещё работает как ожидается.

        Args:
            message (str): Warning message to log / Предупреждающее сообщение для логирования
            tag (str): Custom tag for the message / Пользовательский тег для сообщения
        """
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["WARNING"]:
            self._univ_log(message=message, tag=tag)

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        """
        Error level logging / Логирование уровня ошибок

        Used when a serious problem occurred that prevented the program from performing a function.
        The software may still be able to continue running.

        Используется когда произошла серьёзная проблема, которая помешала программе выполнить функцию.
        Программное обеспечение может всё ещё продолжать работу.

        Args:
            message (str): Error message to log / Сообщение об ошибке для логирования
            tag (str): Custom tag for the message / Пользовательский тег для сообщения
        """
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["ERROR"]:
            self._univ_log(message=message, tag=tag)

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        """
        Critical level logging / Логирование критического уровня

        Used when a very serious error occurred that may prevent the program from continuing.
        This is the highest priority log level.

        Используется когда произошла очень серьёзная ошибка, которая может помешать продолжению работы программы.
        Это наивысший приоритетный уровень логирования.

        Args:
            message (str): Critical error message to log / Критическое сообщение об ошибке для логирования
            tag (str): Custom tag for the message / Пользовательский тег для сообщения
        """
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["CRITICAL"]:
            self._univ_log(message=message, tag=tag)


# ===== MAIN EXECUTION BLOCK - FUNCTIONALITY TESTING / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ПРОВЕРКА РАБОТОСПОСОБНОСТИ =====
if __name__ == '__main__':
    # Test logger functionality by creating instance and testing all log levels
    # Тестирование функциональности логгера путем создания экземпляра и проверки всех уровней логирования
    print("=== Logger Functionality Test / Тест функциональности логгера ===")

    # Create logger instance / Создание экземпляра логгера
    lg = Logger()

    # Test all log levels / Тестирование всех уровней логирования
    lg.debug("Debug message test / Тест отладочного сообщения")
    lg.info("Info message test / Тест информационного сообщения")
    lg.warning("Warning message test / Тест предупреждающего сообщения")
    lg.error("Error message test / Тест сообщения об ошибке")
    lg.critical("Critical message test / Тест критического сообщения")

    print("=== Test completed / Тест завершён ===")