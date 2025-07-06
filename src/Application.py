import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase
import Settings as st


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        # Не подлючение к базе данных, а задание параметров для неё
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(st.db_params["host"])
        db.setDatabaseName(st.db_params["dbname"])
        db.setPort(st.db_params["port"])
        db.setUserName(st.db_params["user"])
        db.setPassword(st.db_params["password"])
        # Подключение к базе данных
        ok = db.open()
        # Отладка
        if ok:
            print("Connected to database", file=sys.stderr)
        else:
            print("Connection FAILED", file=sys.stderr)