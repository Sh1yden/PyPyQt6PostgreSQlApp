# TODO доделать класс логер для приложения.
# TODO залогировать тут всё.
# TODO добавить лвл логирования.
# TODO убрать константы в класс.
import datetime
from pathlib import Path
import json
import os
import sys


class Logger:
    """Класс логирования программы."""

    # Конструктор класса.
    def __init__(self):

        self.log_lvl = 10
        # Словарь хранения логов на время выполнения программы.
        self.logs = {}

        # Имя файла логов на время выполнения программы, чтобы новые не создавать.
        self.SAVE_LOG = self._name_of_logs()
        # Указание файловой системы для программы
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_DIR = os.path.dirname(os.path.dirname(self.CURRENT_DIR))
        self.SAVE_DIR = Path(os.path.join(self.PROJECT_DIR, "logs"))
        # Текущая дата
        self.DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"

        self._initialize_files()

    def _name_of_logs(self):
        """Создание имени для логов."""
        try:
            logs_list = os.listdir(self.SAVE_DIR)
            # Если файла в директории нет задаём имя с 01.
            if len(logs_list) < 1:
                save_file_name = Path(f"{self.SAVE_DIR}/{self.DATE}-{"01"}.json")
            else:  # Иначе выдаём имя + 1 от существующего максимального в директории.
                # Создание листа с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # Если последовательное значение меньше 10, к числу добавляем 0, например 02.
                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(f"{self.SAVE_DIR}/{self.DATE}-0{int(max(name_logs_list)) + 1}.json")
                else:  # Иначе просто убираем ноль.
                    save_file_name = Path(f"{self.SAVE_DIR}/{self.DATE}-{int(max(name_logs_list)) + 1}.json")

            return save_file_name
        except Exception as e:
            pass

    def _initialize_files(self):
        """Инициализация файлов и директорий для программы."""
        try:
            # Создаём директорию.
            self.SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not self.SAVE_LOG.exists():
                self._save_to_log()
        except Exception as e:
            pass

    def _load_from_log(self):
        """Загрузка данных с файла логов."""
        try:
            with open(self.SAVE_LOG, "r") as f:
                self.logs = json.load(f)
        except Exception as e:
            pass

    def _save_to_log(self):
        """Загрузка в файл логов."""
        try:
            with open(self.SAVE_LOG, "w") as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            pass

    # Универсальный шаблон, чтобы не повторять код.
    def _univ_log(self, message: str, tag: str):
        try:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] [{tag}]: {message}", file=sys.stderr)

            self._load_from_log()
            self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
            self._save_to_log()
        except Exception as e:
            pass

    # Уровни логов.
    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        if self.log_lvl >= 10:
            self._univ_log(message=message, tag=tag)

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        if self.log_lvl >= 20:
            self._univ_log(message=message, tag=tag)

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        if self.log_lvl >= 30:
            self._univ_log(message=message, tag=tag)

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        if self.log_lvl >= 40:
            self._univ_log(message=message, tag=tag)

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        if self.log_lvl >= 50:
            self._univ_log(message=message, tag=tag)


# Проверка работоспособности.
if __name__ == '__main__':
    logger = Logger()

    logger.debug()
    logger.info()
    logger.warning()
    logger.error()
    logger.critical()
