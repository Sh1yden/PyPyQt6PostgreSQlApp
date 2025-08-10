# ===== DATABASE CONNECTION CLASS / КЛАСС ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ =====

# ===== IMPORTS / ИМПОРТЫ =====
import psycopg2
from psycopg2.extras import RealDictCursor
from src.core.Logger import Logger
from src.config.AppConfig import AppConfig


# ===== CONNECTION CLASS / КЛАСС ПОДКЛЮЧЕНИЯ =====
class Connection:
    """
    Database connection class / Класс подключения базы данных
    Handles PostgreSQL database operations / Обрабатывает операции с базой данных PostgreSQL
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self):
        """Class constructor / Конструктор класса"""
        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Connection.")
        self.lg.debug("Logger created in class Connection().")

        # Program files management / Работа с файлами программы
        self.appcfg = AppConfig()

        # Database connection object / Объект подключения к базе данных
        self.connection = None

    # ===== DATABASE OPERATIONS / ОПЕРАЦИИ С БАЗОЙ ДАННЫХ =====
    def connect_to_db(self):
        """
        Connect to database / Соединение к базе данных
        
        Returns:
            Connection object / Объект соединения
        """
        try:
            if not self.connection or self.connection.closed:
                # Connect to database / Подключение к базе данных
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
        """
        Execute database query / Выполнение запроса
        
        Args:
            query: SQL query string / SQL запрос
            params: Query parameters / Параметры запроса
            
        Returns:
            Query results or None / Результаты запроса или None
        """
        try:
            with self.connect_to_db() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    
                    # ! Fix for internal error: / ! Для исправления внутренней ошибки:
                    # ! "Connection internal error: no results to fetch. In DEF execute_query()."
                    # Executed for queries without parameters, i.e. just to display table / Выполняется при запросе без параметров, то есть просто для отображения таблицы
                    if params is None:
                        return cursor.fetchall()
        except Exception as e:
            self.lg.error(f"Connection internal error: {e}. In DEF execute_query().")

    def close_connection(self):
        """Close database connection / Закрытие соединения базы данных"""
        try:
            if self.connection:
                self.connection.close()
                self.lg.debug("Connection Connection CLOSED. In DEF close_connection().")
        except Exception as e:
            self.lg.error(f"Connection internal error: {e}. In DEF close_connection().")


# ===== FUNCTIONALITY TESTING / ПРОВЕРКА РАБОТОСПОСОБНОСТИ =====
if __name__ == '__main__':
    # Test database connection / Тестирование подключения к базе данных
    connection_to_db = Connection()
    connection_to_db.connect_to_db()
    # connection_to_db.execute_query()
    connection_to_db.close_connection()