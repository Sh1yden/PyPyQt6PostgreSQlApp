# TODO доделать класс логер для приложения.
# TODO залогировать тут всё.
import datetime
from pathlib import Path
import json
import os

# Константы для работы класса.
DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
SAVE_DIR = Path(os.path.join(PROJECT_DIR, "logs"))
DEFAULT_FILE = {}


class Logger:
    """Класс логирования программы."""

    # Конструктор класса.
    def __init__(self):
        # Словарь хранения логов на время выполнения программы.
        self.logs = {}
        # Имя файла логов на время выполнения программы, чтобы новые не создавать.
        self.SAVE_FILE = self._name_logs()
        self._initialize_files()

    def _name_logs(self):
        """Создание имени для логов."""
        try:
            logs_list = os.listdir(SAVE_DIR)
            # Если файла в директории нет задаём имя с 01.
            if len(logs_list) < 1:
                save_file_name = Path(f"{SAVE_DIR}/{DATE}-{"01"}.json")
            else:  # Иначе выдаём имя + 1 от существующего максимального в директории.
                # Создание листа с последовательными значениями 01, 02 и т.д.
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                # Если последовательное значение меньше 10, к числу добавляем 0, например 02.
                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(f"{SAVE_DIR}/{DATE}-0{int(max(name_logs_list)) + 1}.json")
                else:  # Иначе просто убираем ноль.
                    save_file_name = Path(f"{SAVE_DIR}/{DATE}-{int(max(name_logs_list)) + 1}.json")

            return save_file_name
        except Exception as e:
            pass

    def _initialize_files(self):
        """Инициализация файлов и директорий для программы."""
        try:
            # Создаём директорию.
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not self.SAVE_FILE.exists():
                self._save_to_file()
        except Exception as e:
            pass

    def _load_from_file(self):
        """Загрузка данных с файла логов."""
        try:
            with open(self.SAVE_FILE, "r") as f:
                self.logs = json.load(f)
        except Exception as e:
            pass

    def _save_to_file(self):
        """Загрузка в файл логов."""
        try:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            pass

    # Уровни логов
    def debug(self, message="TEST, INPUT VALUE!!!", tag="DEBUG"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

        self._load_from_file()
        self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
        self._save_to_file()

    def info(self, message="TEST, INPUT VALUE!!!", tag="INFO"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

        self._load_from_file()
        self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
        self._save_to_file()

    def warning(self, message="TEST, INPUT VALUE!!!", tag="WARN"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

        self._load_from_file()
        self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
        self._save_to_file()

    def error(self, message="TEST, INPUT VALUE!!!", tag="ERROR"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

        self._load_from_file()
        self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
        self._save_to_file()

    def critical(self, message="TEST, INPUT VALUE!!!", tag="CRIT"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

        self._load_from_file()
        self.logs.update({f"[{current_time}] [{tag}]": f"{message}"})
        self._save_to_file()


# Проверка работоспособности.
if __name__ == '__main__':
    logger = Logger()

    logger.info()
    logger.debug()
    logger.warning()
    logger.error()
    logger.critical()
