# TODO добавить логи в класс, логирование исключений и ошибок
import json
from pathlib import Path
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
SAVE_DIR = Path(os.path.join(PROJECT_DIR, "media"))
SAVE_FILE = Path(f"{SAVE_DIR}/db_settings.json")


class Settings:
    def __init__(self):
        self.settings = {}
        self._initialize_files()

    def _initialize_files(self):
        try:
            # Создаём директорию
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый
            if not SAVE_FILE.exists():
                self._save_to_file()
        except Exception as e:
            pass

    def load_from_file(self):
        try:
            with open(SAVE_FILE, "r") as f:
                self.settings = json.load(f)
        except Exception as e:
            pass

    def _save_to_file(self):
        try:
            # TODO сделать авто ввод данных бд на выбор, либо пользователь, либо авто
            with open(SAVE_FILE, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            pass
