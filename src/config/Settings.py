# TODO добавить логи в класс, логирование исключений и ошибок.
import json
from pathlib import Path
import os


class Settings:
    """Класс базовых настроек для программы."""

    # Конструктор класса.
    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.SAVE_DIR = Path(f"{self.CURRENT_DIR}/settings/")
        self.SAVE_FILE = Path(f"{self.SAVE_DIR}/db_settings.json")

        # Начальный словарь настроек.
        self.settings = {}
        self._initialize_files()

    def _initialize_files(self):
        """Инициализация файлов и директорий для программы."""
        try:
            # Создаём директорию.
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not SAVE_FILE.exists():
                self._save_to_file()
        except Exception as e:
            pass

    def load_from_file(self):
        """Загрузка данных из файла настроек."""
        try:
            with open(SAVE_FILE, "r") as f:
                self.settings = json.load(f)
        except Exception as e:
            pass

    def _save_to_file(self):
        """Загрузка данных в файл настроек."""
        try:
            # TODO сделать авто ввод данных бд на выбор, либо пользователь, либо авто
            with open(SAVE_FILE, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            pass
