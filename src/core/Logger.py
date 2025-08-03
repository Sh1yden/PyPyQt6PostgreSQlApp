import datetime
from pathlib import Path
import os
import sys
from src.config.AppConfig import AppConfig


class Logger:
    """Класс логирования программы."""

    _instanse_Logger = None # Хранит единственный экземпляр.
    _initialized_Logger = False # Флаг на единственную инициализацию.

    # Создание единого объекта класса.
    def __new__(cls):
        if cls._instanse_Logger is None:
            # Если экземпляра класса нет создаём.
            cls._instanse_Logger = super().__new__(cls)

        return cls._instanse_Logger

    # Конструктор класса.
    def __init__(self):
        if not Logger._initialized_Logger:
            # Успешная инициализация конструктора и класса.
            Logger._initialized_Logger = True

            # Ошибки.
            # * Защита от рекурсии и прочих внутренних ошибок.
            # Которая включается сама при возникновении ошибок.
            # ! Файлы логов при внутренних ошибках класса не сохраняются смотреть в консоли!!!
            self._internal_error_occurred = False

            # Работа с файлами программы
            self.appcfg = AppConfig()

            # Текущая дата.
            self._DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
            # Имя файла логов на время выполнения программы, чтобы новые не создавать.
            self._NAME_OF_LOG = self._name_of_logs()
            # Временный буфер
            self._lg_var = {}

    def _name_of_logs(self):
        """Создание имени для логов."""
        try:
            logs_list = os.listdir(self.appcfg.SAVE_LG_DIR)
            # Если файла в директории нет задаём имя с 01.
            if len(logs_list) < 1:
                save_file_name = Path(f"{self.appcfg.SAVE_LG_DIR}/{self._DATE}-{"01"}.json")
            else:  # Иначе выдаём имя + 1 от существующего максимального в директории.
                # Создание листа с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # Если последовательное значение меньше 10, к числу добавляем 0, например 02.
                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(
                        f"{self.appcfg.SAVE_LG_DIR}/{self._DATE}-0{int(max(name_logs_list)) + 1}.json"
                    )
                else:  # Иначе просто убираем ноль.
                    save_file_name = Path(
                        f"{self.appcfg.SAVE_LG_DIR}/{self._DATE}-{int(max(name_logs_list)) + 1}.json"
                    )

            return save_file_name
        except Exception as e:
            self._internal_error_occurred = True
            self.critical(f"Logger internal error: {e}. In DEF _name_of_logs()")

    # Универсальный шаблон, чтобы не повторять код.
    def _univ_log(self, message: str, tag: str):
        current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
        # Защита от внутренних ошибок класса.
        # + Защита от рекурсии.
        if self._internal_error_occurred:
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)
            return
        try:
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)

            self.appcfg.save_to_file(self._NAME_OF_LOG, self._lg_var)
            self._lg_var = self.appcfg.load_from_file(self._NAME_OF_LOG)
            self._lg_var.update({f"[{current_time}] [{tag}]": f"{message}"})
            self.appcfg.save_to_file(self._NAME_OF_LOG, self._lg_var)
        except Exception as e:
            self._internal_error_occurred = True
            print(f"Logger internal error: {e}. In DEF _univ_log()", file=sys.stderr)

    # Уровни логов.
    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        if self.appcfg.LG_LVL >= self.appcfg.LG_ALL_SET["DEBUG"]:
            self._univ_log(message=message, tag=tag)

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        if self.appcfg.LG_LVL >= self.appcfg.LG_ALL_SET["INFO"]:
            self._univ_log(message=message, tag=tag)

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        if self.appcfg.LG_LVL >= self.appcfg.LG_ALL_SET["WARNING"]:
            self._univ_log(message=message, tag=tag)

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        if self.appcfg.LG_LVL >= self.appcfg.LG_ALL_SET["ERROR"]:
            self._univ_log(message=message, tag=tag)

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        if self.appcfg.LG_LVL >= self.appcfg.LG_ALL_SET["CRITICAL"]:
            self._univ_log(message=message, tag=tag)


# Проверка работоспособности.
if __name__ == '__main__':
    lg = Logger()

    lg.debug()
    lg.info()
    lg.warning()
    lg.error()
    lg.critical()
