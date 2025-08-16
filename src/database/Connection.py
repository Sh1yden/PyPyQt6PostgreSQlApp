# ===== DATABASE CONNECTION CLASS / КЛАСС ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ =====

# ===== IMPORTS / ИМПОРТЫ =====
# PostgreSQL database adapter imports / Импорты адаптера базы данных PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor

# Local application imports / Импорты локального приложения
from src.core.Logger import Logger
from src.config.AppConfig import AppConfig


# ===== CONNECTION CLASS / КЛАСС ПОДКЛЮЧЕНИЯ =====
class Connection:
    """
    Database connection class for PostgreSQL operations / Класс подключения к базе данных для операций PostgreSQL

    Handles all database connectivity and query execution functionality:
    - Connection management and pooling / Управление соединениями и пулинг
    - Query execution with parameter binding / Выполнение запросов с привязкой параметров
    - Error handling and logging / Обработка ошибок и логирование
    - Transaction management / Управление транзакциями
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self):
        """
        Initialize database connection handler / Инициализация обработчика подключения к базе данных

        Sets up logging, configuration, and connection state management.
        Настраивает логирование, конфигурацию и управление состоянием соединения.
        """
        # ===== LOGGING SETUP / НАСТРОЙКА ЛОГИРОВАНИЯ =====
        # Initialize logger for database operations / Инициализация логгера для операций с БД
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Connection.")
        self.lg.debug("Logger created in class Connection().")

        # ===== CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ =====
        # Load application configuration for database settings /
        # Загрузка конфигурации приложения для настроек базы данных
        self.appcfg = AppConfig()

        # ===== CONNECTION STATE / СОСТОЯНИЕ СОЕДИНЕНИЯ =====
        # Initialize connection object as None (lazy connection) /
        # Инициализация объекта соединения как None (ленивое соединение)
        self.connection = None

    # ===== CONNECTION MANAGEMENT / УПРАВЛЕНИЕ СОЕДИНЕНИЯМИ =====
    def connect_to_db(self):
        """
        Establish connection to PostgreSQL database / Установление соединения с базой данных PostgreSQL

        Uses lazy connection pattern - creates connection only when needed.
        Использует паттерн ленивого соединения - создает соединение только при необходимости.

        Returns:
            psycopg2.connection: Active database connection object /
                                Активный объект соединения с базой данных
        """
        try:
            # Check if connection exists and is still active /
            # Проверка существования соединения и его активности
            if not self.connection or self.connection.closed:
                # Load database configuration from settings file /
                # Загрузка конфигурации базы данных из файла настроек
                db_config = self.appcfg.load_from_file(self.appcfg.save_set_db_file)

                # Establish new connection with configuration parameters /
                # Установление нового соединения с параметрами конфигурации
                self.connection = psycopg2.connect(**db_config)

                self.lg.debug("Connection Connected to DB. In DEF connect_to_db().")

            return self.connection

        except Exception as e:
            # Log critical error for connection failure /
            # Логирование критической ошибки при неудаче соединения
            self.lg.critical(f"Connection internal error: {e}. In DEF connect_to_db().")
            raise

    def close_connection(self):
        """
        Safely close database connection / Безопасное закрытие соединения с базой данных

        Ensures proper cleanup of database resources.
        Обеспечивает правильную очистку ресурсов базы данных.
        """
        try:
            # Check if connection exists before attempting to close /
            # Проверка существования соединения перед попыткой закрытия
            if self.connection and not self.connection.closed:
                self.connection.close()
                self.connection = None  # Reset connection reference / Сброс ссылки на соединение
                self.lg.debug("Connection Connection CLOSED. In DEF close_connection().")

        except Exception as e:
            # Log error but don't raise to prevent cleanup issues /
            # Логирование ошибки без поднятия исключения для предотвращения проблем очистки
            self.lg.error(f"Connection internal error: {e}. In DEF close_connection().")

    # ===== QUERY EXECUTION / ВЫПОЛНЕНИЕ ЗАПРОСОВ =====
    def execute_query(self, query, params=None):
        """
        Execute SQL query with optional parameters / Выполнение SQL запроса с опциональными параметрами

        Handles both SELECT and DML operations with proper transaction management.
        Обрабатывает как SELECT, так и DML операции с правильным управлением транзакциями.

        Args:
            query (str): SQL query string to execute / SQL запрос для выполнения
            params (tuple, optional): Query parameters for safe binding / Параметры запроса для безопасной привязки

        Returns:
            list: Query results for SELECT operations, None for DML operations /
                  Результаты запроса для SELECT операций, None для DML операций
        """
        try:
            # Use context manager for automatic connection and cursor cleanup /
            # Использование контекстного менеджера для автоматической очистки соединения и курсора
            with self.connect_to_db() as conn:
                # RealDictCursor provides dict-like access to query results /
                # RealDictCursor предоставляет словарный доступ к результатам запроса
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Execute query with parameter binding for SQL injection prevention /
                    # Выполнение запроса с привязкой параметров для предотвращения SQL инъекций
                    cursor.execute(query, params)

                    # Commit transaction to ensure data persistence /
                    # Подтверждение транзакции для обеспечения сохранности данных
                    conn.commit()

                    # Return results only for SELECT queries (when params is None) /
                    # Возврат результатов только для SELECT запросов (когда params равен None)
                    # Fix for internal error: "no results to fetch" /
                    # Исправление внутренней ошибки: "нет результатов для получения"
                    if params is None:
                        return cursor.fetchall()

        except Exception as e:
            # Log query execution errors for debugging /
            # Логирование ошибок выполнения запросов для отладки
            self.lg.error(f"Connection internal error: {e}. In DEF execute_query().")
            raise


# ===== FUNCTIONALITY TESTING / ПРОВЕРКА РАБОТОСПОСОБНОСТИ =====
if __name__ == '__main__':
    # Test database connection functionality / Тестирование функциональности подключения к базе данных
    print("Testing database connection...")

    connection_to_db = Connection()

    # Test connection establishment / Тестирование установления соединения
    connection_to_db.connect_to_db()
    print("Connection established successfully.")

    # Test connection closure / Тестирование закрытия соединения
    connection_to_db.close_connection()
    print("Connection closed successfully.")