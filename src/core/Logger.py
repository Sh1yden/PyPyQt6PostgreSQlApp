# TODO доделать класс логер для приложения
# TODO залогировать тут всё
import datetime
from pathlib import Path
import json
import os

DATE = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
SAVE_DIR = Path(os.path.join(PROJECT_DIR, "logs"))
DEFAULT_FILE = {}


class Logger:
    def __init__(self):
        self.logs = {}
        self._initialize_files()

    def _name_logs(self):
        try:
            logs_list = os.listdir(SAVE_DIR)
            if len(logs_list) < 1:
                save_file_name = Path(f"{SAVE_DIR}/{DATE}-{"01"}.json")
            else:
                name_logs_list = []
                for i in logs_list:
                    name_logs_list.append(i[11:13])

                if int(max(name_logs_list)) + 1 < 10:
                    save_file_name = Path(f"{SAVE_DIR}/{DATE}-0{int(max(name_logs_list)) + 1}.json")
                else:
                    save_file_name = Path(f"{SAVE_DIR}/{DATE}-{int(max(name_logs_list)) + 1}.json")

            return save_file_name
        except Exception as e:
            pass

    def _initialize_files(self):
        try:
            # Создаём директорию
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый
            if not self._name_logs().exists():
                self._save_to_file()
        except Exception as e:
            pass

    def _load_from_file(self):
        try:
            with open(self._name_logs(), "r") as f:
                self.logs = json.load(f)
        except Exception as e:
            pass

    def _save_to_file(self):
        try:
            with open(self._name_logs(), "w") as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            pass

    def debug(self, tag="DEBUG", message="TEST, INPUT VALUE!!!"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

    def info(self, tag="INFO", message="TEST, INPUT VALUE!!!"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

    def warning(self, tag="WARN", message="TEST, INPUT VALUE!!!"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

    def error(self, tag="ERROR", message="TEST, INPUT VALUE!!!"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")

    def critical(self, tag="CRIT", message="TEST, INPUT VALUE!!!"):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] [{tag}]: {message}")


if __name__ == '__main__':
    logger = Logger()

    logger.info()
    logger.debug()
    logger.warning()
    logger.error()
    logger.critical()
