# ===== PROGRAM LOGGING CLASS / КЛАСС ЛОГИРОВАНИЯ ПРОГРАММЫ =====

# ===== IMPORTS / ИМПОРТЫ =====
import datetime
from pathlib import Path
import os
import sys
from src.config.AppConfig import AppConfig


# ===== LOGGER CLASS / КЛАСС ЛОГГЕРА =====
class Logger:
    """
    Program logging class / Класс логирования программы
    Singleton pattern implementation for unified logging / Реализация паттерна Singleton для унифицированного логирования
    """

    # ===== SINGLETON PATTERN / ПАТТЕРН СИНГЛТОН =====
    _instanse_Logger = None  # Stores single instance / Хранит единственный экземпляр
    _initialized_Logger = False  # Single initialization flag / Флаг на единственную инициализацию

    # ===== SINGLETON CREATION / СОЗДАНИЕ СИНГЛТОНА =====
    def __new__(cls):
        """Create single class instance / Создание единого объекта класса"""
        if cls._instanse_Logger is None:
            # If no class instance exists, create one / Если экземпляра класса нет создаём
            cls._instanse_Logger = super().__new__(cls)
        return cls._instanse_Logger

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self):
        """Class constructor / Конструктор класса"""
        if not Logger._initialized_Logger:
            # Successful constructor and class initialization / Успешная инициализация конструктора и класса
            Logger._initialized_Logger = True

            # ===== ERROR HANDLING / ОБРАБОТКА ОШИБОК =====
            # Protection from recursion and other internal errors / Защита от рекурсии и прочих внутренних ошибок
            # Activated automatically when errors occur / Которая включается сама при возникновении ошибок
            # ! Log files are not saved for internal class errors - check console!!! / ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            self._internal_error_occurred = False

            # ===== CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ =====
            # Work with program files / Работа с файлами программы
            self._appcfg = AppConfig()

            # ===== DATE AND FILE SETUP / НАСТРОЙКА ДАТЫ И ФАЙЛОВ =====
            # Current date / Текущая дата
            self._DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
            # Log file name for program runtime, to avoid creating new ones / Имя файла логов на время выполнения программы, чтобы новые не создавать
            self._NAME_OF_LOG = self._name_of_logs()
            # Temporary buffer / Временный буфер
            self._lg_var = {}

    # ===== FILE MANAGEMENT / УПРАВЛЕНИЕ ФАЙЛАМИ =====
    def _name_of_logs(self):
        """Create log file name / Создание имени для логов"""
        try:
            logs_list = os.listdir(self._appcfg.save_lg_dir)
            
            # If no files in directory, set name with 01 / Если файла в директории нет задаём имя с 01
            if len(logs_list) < 1:
                save_file_name = Path(f"{self._appcfg.save_lg_dir}/{self._DATE}-{"01"}.json")
            else:
                # Otherwise give name + 1 from existing maximum in directory / Иначе выдаём имя + 1 от существующего максимального в директории
                # Create list with sequential values 01, 02, etc. / Создание листа с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # If sequential value is less than 10, add 0 to number, e.g. 02 / Если последовательное значение меньше 10, к числу добавляем 0, например 02
                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(
                        f"{self._appcfg.save_lg_dir}/{self._DATE}-0{int(max(name_logs_list)) + 1}.json"
                    )
                else:
                    # Otherwise just remove zero / Иначе просто убираем ноль
                    save_file_name = Path(
                        f"{self._appcfg.save_lg_dir}/{self._DATE}-{int(max(name_logs_list)) + 1}.json"
                    )

            return save_file_name
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _name_of_logs().")

    # ===== UNIVERSAL LOGGING / УНИВЕРСАЛЬНОЕ ЛОГИРОВАНИЕ =====
    def _univ_log(self, message: str, tag: str):
        """Universal template to avoid code repetition / Универсальный шаблон, чтобы не повторять код"""
        # Определения времени выполнения вплоть до миллисекунд / Run-time definitions down to milliseconds
        current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
        
        # Protection from internal class errors / Защита от внутренних ошибок класса
        # + Protection from recursion / + Защита от рекурсии
        if self._internal_error_occurred:
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)
            return
            
        try:
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)

            self._appcfg.save_to_file(self._NAME_OF_LOG, self._lg_var)
            self._lg_var = self._appcfg.load_from_file(self._NAME_OF_LOG)
            self._lg_var.update({f"[{current_time}] [{tag}]": f"{message}"})
            self._appcfg.save_to_file(self._NAME_OF_LOG, self._lg_var)
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _univ_log().")

    # ===== LOG LEVELS / УРОВНИ ЛОГОВ =====
    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        """Debug level logging / Логирование уровня отладки"""
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["DEBUG"]:
            self._univ_log(message=message, tag=tag)

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        """Info level logging / Логирование информационного уровня"""
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["INFO"]:
            self._univ_log(message=message, tag=tag)

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        """Warning level logging / Логирование уровня предупреждений"""
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["WARNING"]:
            self._univ_log(message=message, tag=tag)

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        """Error level logging / Логирование уровня ошибок"""
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["ERROR"]:
            self._univ_log(message=message, tag=tag)

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        """Critical level logging / Логирование критического уровня"""
        if self._appcfg.lg_lvl >= self._appcfg.lg_all_set["CRITICAL"]:
            self._univ_log(message=message, tag=tag)


# ===== FUNCTIONALITY TESTING / ПРОВЕРКА РАБОТОСПОСОБНОСТИ =====
if __name__ == '__main__':
    # Create logger instance and test all levels / Создание экземпляра логгера и тестирование всех уровней
    lg = Logger()

    lg.debug()
    lg.info()
    lg.warning()
    lg.error()
    lg.critical()