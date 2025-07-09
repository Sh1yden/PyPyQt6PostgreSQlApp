import sys
from PyQt6.QtSql import QSqlDatabase
from src.config import Settings as St


class Connection():
    """Класс подключения базы данных."""

    # * Сделано по быстрому на время.
    # TODO переделать колхоз класс, в нормальный.

    # Конструктор класса.
    def __init__(self):
        # Получение данных из файла.
        self.st = St.Settings()
        self.st.load_from_file()
        # Подключение к бд.
        self.connect(self.st)

    def connect(self, st):
        print(st.settings["db_settings"]["db_host_name"])
        # Не подлючение к базе данных, а задание параметров для неё.
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(st.settings["db_settings"]["db_host_name"])
        db.setDatabaseName(st.settings["db_settings"]["db_name"])
        db.setPort(st.settings["db_settings"]["db_port"])
        db.setUserName(st.settings["db_settings"]["db_user"])
        db.setPassword(st.settings["db_settings"]["db_password"])
        # Подключение к базе данных.
        ok = db.open()
        # Отладка.
        # TODO переделать через класс логер.
        if ok:
            print("Connected to database", file=sys.stderr)
        else:
            print("Connection FAILED", file=sys.stderr)
