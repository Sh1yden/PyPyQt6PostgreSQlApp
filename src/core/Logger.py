import datetime
from pathlib import Path
import json
import os
import sys


class Logger:
    """Класс логирования программы."""

    _instanse = None # Хранит единственный экземпляр.
    _initialized = False # Флаг на единственную инициализацию.

    # Создание единого объекта класса.
    def __new__(cls):
        if cls._instanse is None:
            # Если экземпляра класса нет создаём.
            cls._instanse = super().__new__(cls)

        return cls._instanse

    # Конструктор класса.
    def __init__(self):
        if not Logger._initialized:
            # Успешная инициализация конструктора и класса.
            Logger._initialized = True

            # TODO сделать один класс настройки путей и файлов
            # Указание файловой системы для программы.
            # Общие папки.
            self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            self.PROJECT_DIR = os.path.dirname(os.path.dirname(self.CURRENT_DIR))

            # Логи.
            self.SAVE_DIR_LOG = Path(os.path.join(self.PROJECT_DIR, "logs"))

            # Текущая дата.
            self.DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"

            # Имя файла логов на время выполнения программы, чтобы новые не создавать.
            self._SAVE_LOG = self._name_of_logs()

            # Настройки.
            self.SAVE_DIR_SET = Path(f"{self.PROJECT_DIR}/src/config/settings/")
            self.SAVE_SET = Path(f"{self.SAVE_DIR_SET}/lg_settings.json")

            # ! Выбор уровня логирования
            self.LOG_ALL_SET = self.lvl_log()
            self.LOG_LVL = self.LOG_ALL_SET["lg_settings"]["lg_lvl_set"]

            # Ошибки.
            # * Защита от рекурсии и прочих внутренних ошибок.
            # Которая включается сама при возникновении ошибок.
            # ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            self._internal_error_occurred = False

            # Работа с файлами.
            # Словарь хранения логов и настроек на время выполнения программы.
            self._log_set_var = {}
            self._log_var = {}
            self._initialize_files()

    def lvl_log(self):
        """Функция, которая принимает данные из файла и ставит их в логер."""
        try:
            self._load_from_set()
            return self._log_set_var
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF lvl_log()")

    def _name_of_logs(self):
        """Создание имени для логов."""
        try:
            logs_list = os.listdir(self.SAVE_DIR_LOG)
            # Если файла в директории нет задаём имя с 01.
            if len(logs_list) < 1:
                save_file_name = Path(f"{self.SAVE_DIR_LOG}/{self.DATE}-{"01"}.json")
            else:  # Иначе выдаём имя + 1 от существующего максимального в директории.
                # Создание листа с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # Если последовательное значение меньше 10, к числу добавляем 0, например 02.
                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(f"{self.SAVE_DIR_LOG}/{self.DATE}-0{int(max(name_logs_list)) + 1}.json")
                else:  # Иначе просто убираем ноль.
                    save_file_name = Path(f"{self.SAVE_DIR_LOG}/{self.DATE}-{int(max(name_logs_list)) + 1}.json")

            return save_file_name
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _name_of_logs()")

    def _initialize_files(self):
        """Инициализация файлов и директорий для программы."""
        try:
            # Настройки.
            # Создаём директорию для настроек.
            self.SAVE_DIR_SET.mkdir(parents=True, exist_ok=True)
            if not self.SAVE_SET.exists():
                # * DEFAULT settings.
                self._log_set_var = {
                    "lg_settings" : {
                        "lg_lvl_set" : "DEBUG",
                        "OFF" : 0,
                        "DEBUG" : 10,
                        "INFO" : 20,
                        "WARNING": 30,
                        "ERROR": 40,
                        "CRITICAL": 50
                    }
                }
                self._save_to_set()

            # Логи.
            # Создаём директорию для логов.
            self.SAVE_DIR_LOG.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not self._SAVE_LOG.exists():
                self._save_to_log()
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _initialize_files()")

    def _load_from_set(self):
        """Загрузка данных с файла логов."""
        try:
            with open(self.SAVE_SET, "r") as f:
                self._log_set_var = json.load(f)
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _load_from_set()")

    def _save_to_set(self):
        """Загрузка в файл логов."""
        try:
            with open(self.SAVE_SET, "w") as f:
                json.dump(self._log_set_var, f, indent=2)
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _save_to_set()")

    def _load_from_log(self):
        """Загрузка данных с файла логов."""
        try:
            with open(self._SAVE_LOG, "r") as f:
                self._log_var = json.load(f)
        except Exception as e:
            self._internal_error_occurred = True
            self.error(f"Logger internal error: {e}. In DEF _load_from_log()")

    def _save_to_log(self):
        """Загрузка в файл логов."""
        try:
            # Место для проверки внутренних ошибок. Заменить self._SAVE_LOG например на "".
            with open(self._SAVE_LOG, "w") as f: # !
                json.dump(self._log_var, f, indent=2)
        except Exception as e:
            self._internal_error_occurred = True
            self.error(f"Logger internal error: {e}. In DEF _save_to_log()")

    # Универсальный шаблон, чтобы не повторять код.
    def _univ_log(self, message: str, tag: str):
        # Защита от внутренних ошибок класса.
        # + Защита от рекурсии.
        if self._internal_error_occurred:
            current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)
            return
        try:
            current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)

            self._load_from_log()
            self._log_var.update({f"[{current_time}] [{tag}]": f"{message}"})
            self._save_to_log()
        except Exception as e:
            self._internal_error_occurred = True
            print(f"Logger internal error: {e}. In DEF _univ_log()", file=sys.stderr)

    # Уровни логов.
    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        if self.LOG_LVL >= self.LOG_ALL_SET["lg_settings"]["DEBUG"]:
            self._univ_log(message=message, tag=tag)

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        if self.LOG_LVL >= self.LOG_ALL_SET["lg_settings"]["INFO"]:
            self._univ_log(message=message, tag=tag)

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        if self.LOG_LVL >= self.LOG_ALL_SET["lg_settings"]["WARNING"]:
            self._univ_log(message=message, tag=tag)

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        if self.LOG_LVL >= self.LOG_ALL_SET["lg_settings"]["ERROR"]:
            self._univ_log(message=message, tag=tag)

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        if self.LOG_LVL >= self.LOG_ALL_SET["lg_settings"]["CRITICAL"]:
            self._univ_log(message=message, tag=tag)


# Проверка работоспособности.
if __name__ == '__main__':
    lg = Logger()

    lg.debug()
    lg.info()
    lg.warning()
    lg.error()
    lg.critical()
