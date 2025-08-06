import psycopg2
from psycopg2.extras import RealDictCursor
from src.core.Logger import Logger
from src.config.AppConfig import AppConfig


class Connection:
    """Класс подключения базы данных."""

    # Конструктор класса.
    def __init__(self):
        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Connection.")
        self.lg.debug("Logger created in class Connection().")

        # Работа с файлами программы
        self.appcfg = AppConfig()

        self.connection = None

    def connect_to_db(self):
        """Соединение к базе данных."""
        try:
            if not self.connection or self.connection.closed:
                # Подключение к базе данных.
                self.connection = (
                    psycopg2.connect(
                        **self.appcfg.load_from_file(self.appcfg.save_set_db_file)
                    )
                )
                self.lg.debug("Connection Connected to DB. In DEF connect_to_db().")
            return self.connection
        except Exception as e:
            self.lg.critical(f"Connection internal error: {e}. In DEF connect_to_db().")

    def execute_query(self, query, params=None):
        """Выполнение запроса."""
        try:
            with self.connect_to_db() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    # ! Для исправления внутренней ошибки:
                    # ! "Connection internal error: no results to fetch. In DEF execute_query()."
                    # Выполняется при запросе без параметров, то есть просто для отображения таблицы
                    if params is None:
                        return cursor.fetchall()
        except Exception as e:
            self.lg.error(f"Connection internal error: {e}. In DEF execute_query().")

    def close_connection(self):
        """Закрытие соединения базы данных."""
        try:
            if self.connection:
                self.connection.close()
                self.lg.debug("Connection Connection CLOSED. In DEF close_connection().")
        except Exception as e:
            self.lg.error(f"Connection internal error: {e}. In DEF close_connection().")


if __name__ == '__main__':
    connection_to_db = Connection()
    connection_to_db.connect_to_db()
    # connection_to_db.execute_query()
    connection_to_db.close_connection()
