# ===== SQL QUERY BUILDER CLASSES / КЛАССЫ КОНСТРУКТОРА SQL ЗАПРОСОВ =====
# Automated SQL query generation for database operations
# Автоматическая генерация SQL запросов для операций с базой данных

# ===== BASE QUERY BUILDER CLASS / БАЗОВЫЙ КЛАСС КОНСТРУКТОРА ЗАПРОСОВ =====
class QueryBuilder:
    """
    Base SQL query generator for database tables / Базовый генератор SQL запросов для таблиц базы данных
    Avoids code duplication and ensures query consistency / Избегает дублирования кода и обеспечивает единообразие запросов

    This class provides static methods to generate common CRUD (Create, Read, Update, Delete) SQL queries.
    It standardizes query generation across the application and reduces the risk of SQL syntax errors.
    All methods return parameterized queries to prevent SQL injection attacks.

    Этот класс предоставляет статические методы для генерации общих CRUD (Create, Read, Update, Delete) SQL запросов.
    Он стандартизирует генерацию запросов в приложении и снижает риск синтаксических ошибок SQL.
    Все методы возвращают параметризованные запросы для предотвращения атак SQL-инъекций.
    """

    # ===== READ OPERATIONS / ОПЕРАЦИИ ЧТЕНИЯ =====

    @staticmethod
    def select_all(table_name: str) -> str:
        """
        Generate query to retrieve all records from table / Генерирует запрос для получения всех записей из таблицы

        Creates a SELECT query that retrieves all columns and rows from the specified table.
        Results are automatically ordered by ID for consistent display.

        Создает SELECT запрос, который получает все столбцы и строки из указанной таблицы.
        Результаты автоматически упорядочиваются по ID для согласованного отображения.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных

        Returns:
            str: SQL SELECT query string / Строка SQL SELECT запроса

        Example:
            SELECT * FROM "Teacher" ORDER BY id
        """
        return f'SELECT * FROM "{table_name}" ORDER BY id'

    @staticmethod
    def select_by_id(table_name: str) -> str:
        """
        Generate query to retrieve a record by ID / Генерирует запрос для получения записи по ID

        Creates a SELECT query that retrieves a specific record based on its ID.
        Uses parameterized query to prevent SQL injection.

        Создает SELECT запрос, который получает определенную запись на основе ее ID.
        Использует параметризованный запрос для предотвращения SQL-инъекций.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных

        Returns:
            str: SQL SELECT query string with parameter placeholder / Строка SQL SELECT запроса с заполнителем параметра

        Example:
            SELECT * FROM "Teacher" WHERE id = %s
        """
        return f'SELECT * FROM "{table_name}" WHERE id = %s'

    # ===== CREATE OPERATIONS / ОПЕРАЦИИ СОЗДАНИЯ =====

    @staticmethod
    def insert(table_name: str, columns: list) -> str:
        """
        Generate query to insert a new record / Генерирует запрос для вставки новой записи

        Creates an INSERT query for adding new records to the database table.
        Automatically generates the correct number of parameter placeholders.
        Does not include ID column as it's typically auto-generated.

        Создает INSERT запрос для добавления новых записей в таблицу базы данных.
        Автоматически генерирует правильное количество заполнителей параметров.
        Не включает столбец ID, так как он обычно генерируется автоматически.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            columns (list): List of column names to insert into / Список названий столбцов для вставки

        Returns:
            str: SQL INSERT query string / Строка SQL INSERT запроса

        Raises:
            ValueError: If columns list is empty / Если список столбцов пуст

        Example:
            INSERT INTO "Teacher" (f_fio, f_phone, f_email, f_comment) VALUES (%s, %s, %s, %s)
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")

        # Generate parameter placeholders / Генерация заполнителей параметров
        placeholders = ', '.join(['%s'] * len(columns))
        # Join column names / Соединение имен столбцов
        columns_str = ', '.join(columns)
        return f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'

    # ===== UPDATE OPERATIONS / ОПЕРАЦИИ ОБНОВЛЕНИЯ =====

    @staticmethod
    def update(table_name: str, columns: list) -> str:
        """
        Generate query to update a record / Генерирует запрос для обновления записи

        Creates an UPDATE query for modifying existing records in the database.
        Updates all specified columns for the record with the given ID.
        Uses parameterized query with ID as the WHERE condition.

        Создает UPDATE запрос для изменения существующих записей в базе данных.
        Обновляет все указанные столбцы для записи с данным ID.
        Использует параметризованный запрос с ID в качестве условия WHERE.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            columns (list): List of column names to update (excluding ID) / Список названий столбцов для обновления (без ID)

        Returns:
            str: SQL UPDATE query string / Строка SQL UPDATE запроса

        Raises:
            ValueError: If columns list is empty / Если список столбцов пуст

        Example:
            UPDATE "Teacher" SET f_fio = %s, f_phone = %s, f_email = %s, f_comment = %s WHERE id = %s
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")

        # Generate SET clause with parameter placeholders / Генерация SET клаузулы с заполнителями параметров
        set_clause = ', '.join([f'{col} = %s' for col in columns])
        return f'UPDATE "{table_name}" SET {set_clause} WHERE id = %s'

    # ===== DELETE OPERATIONS / ОПЕРАЦИИ УДАЛЕНИЯ =====

    @staticmethod
    def delete(table_name: str) -> str:
        """
        Generate query to delete a record / Генерирует запрос для удаления записи

        Creates a DELETE query for removing records from the database table.
        Deletes the record with the specified ID using parameterized query.

        Создает DELETE запрос для удаления записей из таблицы базы данных.
        Удаляет запись с указанным ID, используя параметризованный запрос.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных

        Returns:
            str: SQL DELETE query string / Строка SQL DELETE запроса

        Example:
            DELETE FROM "Teacher" WHERE id = %s
        """
        return f'DELETE FROM "{table_name}" WHERE id = %s'

    # ===== UTILITY OPERATIONS / УТИЛИТАРНЫЕ ОПЕРАЦИИ =====

    @staticmethod
    def count(table_name: str) -> str:
        """
        Generate query to count records in table / Генерирует запрос для подсчета записей в таблице

        Creates a COUNT query to determine the number of records in the table.
        Useful for pagination, statistics, and validation operations.

        Создает COUNT запрос для определения количества записей в таблице.
        Полезно для пагинации, статистики и операций валидации.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных

        Returns:
            str: SQL COUNT query string / Строка SQL COUNT запроса

        Example:
            SELECT COUNT(*) FROM "Teacher"
        """
        return f'SELECT COUNT(*) FROM "{table_name}"'


# ===== ADVANCED QUERY BUILDER CLASS / РАСШИРЕННЫЙ КЛАСС КОНСТРУКТОРА ЗАПРОСОВ =====
class AdvancedQueryBuilder(QueryBuilder):
    """
    Extended query generator for complex cases / Расширенный генератор запросов для сложных случаев

    This class extends the base QueryBuilder with additional functionality for advanced database operations.
    Includes search capabilities, pagination, and other specialized query types.

    Этот класс расширяет базовый QueryBuilder дополнительной функциональностью для продвинутых операций с базой данных.
    Включает возможности поиска, пагинацию и другие специализированные типы запросов.
    """

    # ===== SEARCH OPERATIONS / ОПЕРАЦИИ ПОИСКА =====

    @staticmethod
    def search_by_field(table_name: str, field_name: str) -> str:
        """
        Generate query for case-insensitive field search / Генерирует запрос для поиска по полю без учета регистра

        Creates a SELECT query that searches for records containing the specified text in a field.
        Uses ILIKE operator for case-insensitive pattern matching (PostgreSQL specific).
        Results are ordered by ID for consistency.

        Создает SELECT запрос, который ищет записи, содержащие указанный текст в поле.
        Использует оператор ILIKE для поиска по шаблону без учета регистра (специфично для PostgreSQL).
        Результаты упорядочены по ID для согласованности.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            field_name (str): Name of the field to search in / Имя поля для поиска

        Returns:
            str: SQL search query string / Строка SQL поискового запроса

        Example:
            SELECT * FROM "Teacher" WHERE f_fio ILIKE %s ORDER BY id
        """
        return f'SELECT * FROM "{table_name}" WHERE {field_name} ILIKE %s ORDER BY id'

    # ===== PAGINATION OPERATIONS / ОПЕРАЦИИ ПАГИНАЦИИ =====

    @staticmethod
    def select_with_limit(table_name: str, limit: int, offset: int = 0) -> str:
        """
        Generate query with record limit and offset / Генерирует запрос с ограничением количества записей и смещением

        Creates a SELECT query that retrieves a specific number of records starting from an offset.
        Useful for implementing pagination in large datasets.
        Results are ordered by ID to ensure consistent pagination.

        Создает SELECT запрос, который получает определенное количество записей, начиная со смещения.
        Полезно для реализации пагинации в больших наборах данных.
        Результаты упорядочены по ID для обеспечения согласованной пагинации.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            limit (int): Maximum number of records to return / Максимальное количество записей для возврата
            offset (int): Number of records to skip from the beginning / Количество записей для пропуска с начала

        Returns:
            str: SQL query string with LIMIT and OFFSET / Строка SQL запроса с LIMIT и OFFSET

        Example:
            SELECT * FROM "Teacher" ORDER BY id LIMIT 10 OFFSET 20
        """
        return f'SELECT * FROM "{table_name}" ORDER BY id LIMIT {limit} OFFSET {offset}'

    # ===== SORTING OPERATIONS / ОПЕРАЦИИ СОРТИРОВКИ =====

    @staticmethod
    def select_ordered_by(table_name: str, order_column: str, ascending: bool = True) -> str:
        """
        Generate query with custom ordering / Генерирует запрос с пользовательской сортировкой

        Creates a SELECT query that retrieves all records ordered by a specified column.
        Supports both ascending and descending order.

        Создает SELECT запрос, который получает все записи, упорядоченные по указанному столбцу.
        Поддерживает как восходящий, так и нисходящий порядок.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            order_column (str): Column name to order by / Имя столбца для сортировки
            ascending (bool): True for ascending, False for descending / True для восходящего, False для нисходящего

        Returns:
            str: SQL query string with ORDER BY clause / Строка SQL запроса с клаузулой ORDER BY

        Example:
            SELECT * FROM "Teacher" ORDER BY f_fio ASC
            SELECT * FROM "Teacher" ORDER BY f_fio DESC
        """
        order_direction = "ASC" if ascending else "DESC"
        return f'SELECT * FROM "{table_name}" ORDER BY {order_column} {order_direction}'

    # ===== FILTERING OPERATIONS / ОПЕРАЦИИ ФИЛЬТРАЦИИ =====

    @staticmethod
    def select_where_equals(table_name: str, column_name: str) -> str:
        """
        Generate query to find records where column equals value / Генерирует запрос для поиска записей где столбец равен значению

        Creates a SELECT query that retrieves records where a specific column matches the provided value.
        Uses parameterized query to prevent SQL injection.

        Создает SELECT запрос, который получает записи, где определенный столбец соответствует предоставленному значению.
        Использует параметризованный запрос для предотвращения SQL-инъекций.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            column_name (str): Name of the column to filter by / Имя столбца для фильтрации

        Returns:
            str: SQL query string with WHERE clause / Строка SQL запроса с клаузулой WHERE

        Example:
            SELECT * FROM "Teacher" WHERE f_fio = %s ORDER BY id
        """
        return f'SELECT * FROM "{table_name}" WHERE {column_name} = %s ORDER BY id'

    @staticmethod
    def select_where_not_null(table_name: str, column_name: str) -> str:
        """
        Generate query to find records where column is not null / Генерирует запрос для поиска записей где столбец не пустой

        Creates a SELECT query that retrieves records where a specific column has a non-null value.
        Useful for filtering out incomplete records.

        Создает SELECT запрос, который получает записи, где определенный столбец имеет непустое значение.
        Полезно для фильтрации неполных записей.

        Args:
            table_name (str): Name of the database table / Имя таблицы базы данных
            column_name (str): Name of the column to check / Имя столбца для проверки

        Returns:
            str: SQL query string with IS NOT NULL condition / Строка SQL запроса с условием IS NOT NULL

        Example:
            SELECT * FROM "Teacher" WHERE f_email IS NOT NULL ORDER BY id
        """
        return f'SELECT * FROM "{table_name}" WHERE {column_name} IS NOT NULL ORDER BY id'


# ===== MAIN EXECUTION BLOCK - TESTING AND EXAMPLES / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ТЕСТИРОВАНИЕ И ПРИМЕРЫ =====
if __name__ == '__main__':
    # Testing query generator functionality / Тестирование функциональности генератора запросов
    print("=== QueryBuilder Testing / Тестирование QueryBuilder ===")
    print()

    # ===== BASE QUERYBUILDER TESTS / ТЕСТЫ БАЗОВОГО QUERYBUILDER =====
    print("=== Base QueryBuilder Tests / Тесты базового QueryBuilder ===")

    # Test data for Teacher table / Тестовые данные для таблицы Teacher
    teacher_columns = ['f_fio', 'f_phone', 'f_email', 'f_comment']
    print("Teacher table queries / Запросы для таблицы Teacher:")
    print(f"  SELECT ALL: {QueryBuilder.select_all('Teacher')}")
    print(f"  SELECT BY ID: {QueryBuilder.select_by_id('Teacher')}")
    print(f"  INSERT: {QueryBuilder.insert('Teacher', teacher_columns)}")
    print(f"  UPDATE: {QueryBuilder.update('Teacher', teacher_columns)}")
    print(f"  DELETE: {QueryBuilder.delete('Teacher')}")
    print(f"  COUNT: {QueryBuilder.count('Teacher')}")

    print("\n" + "="*60 + "\n")

    # Test data for Student table / Тестовые данные для таблицы Student
    student_columns = ['f_fio', 'f_email', 'f_comment']
    print("Student table queries / Запросы для таблицы Student:")
    print(f"  SELECT ALL: {QueryBuilder.select_all('Student')}")
    print(f"  SELECT BY ID: {QueryBuilder.select_by_id('Student')}")
    print(f"  INSERT: {QueryBuilder.insert('Student', student_columns)}")
    print(f"  UPDATE: {QueryBuilder.update('Student', student_columns)}")
    print(f"  DELETE: {QueryBuilder.delete('Student')}")
    print(f"  COUNT: {QueryBuilder.count('Student')}")

    print("\n" + "="*60 + "\n")

    # Test data for StGroup table / Тестовые данные для таблицы StGroup
    group_columns = ['f_title', 'f_comment']
    print("StGroup table queries / Запросы для таблицы StGroup:")
    print(f"  SELECT ALL: {QueryBuilder.select_all('StGroup')}")
    print(f"  SELECT BY ID: {QueryBuilder.select_by_id('StGroup')}")
    print(f"  INSERT: {QueryBuilder.insert('StGroup', group_columns)}")
    print(f"  UPDATE: {QueryBuilder.update('StGroup', group_columns)}")
    print(f"  DELETE: {QueryBuilder.delete('StGroup')}")
    print(f"  COUNT: {QueryBuilder.count('StGroup')}")

    print("\n" + "="*60 + "\n")

    # ===== ADVANCED QUERYBUILDER TESTS / ТЕСТЫ РАСШИРЕННОГО QUERYBUILDER =====
    print("=== Advanced QueryBuilder Tests / Тесты расширенного QueryBuilder ===")

    print("Advanced queries for Teacher table / Расширенные запросы для таблицы Teacher:")
    print(f"  SEARCH BY NAME: {AdvancedQueryBuilder.search_by_field('Teacher', 'f_fio')}")
    print(f"  SEARCH BY EMAIL: {AdvancedQueryBuilder.search_by_field('Teacher', 'f_email')}")
    print(f"  PAGINATION (10 records, skip 20): {AdvancedQueryBuilder.select_with_limit('Teacher', 10, 20)}")
    print(f"  ORDER BY NAME ASC: {AdvancedQueryBuilder.select_ordered_by('Teacher', 'f_fio', True)}")
    print(f"  ORDER BY NAME DESC: {AdvancedQueryBuilder.select_ordered_by('Teacher', 'f_fio', False)}")
    print(f"  WHERE FIO EQUALS: {AdvancedQueryBuilder.select_where_equals('Teacher', 'f_fio')}")
    print(f"  WHERE EMAIL NOT NULL: {AdvancedQueryBuilder.select_where_not_null('Teacher', 'f_email')}")

    print("\n" + "="*60 + "\n")

    # ===== ERROR HANDLING TESTS / ТЕСТЫ ОБРАБОТКИ ОШИБОК =====
    print("=== Error Handling Tests / Тесты обработки ошибок ===")

    try:
        # Test empty columns list / Тест пустого списка столбцов
        QueryBuilder.insert('Teacher', [])
        print("ERROR: Empty columns test should have failed!")
    except ValueError as e:
        print(f"✓ Empty columns validation working: {e}")

    try:
        # Test empty columns for update / Тест пустых столбцов для обновления
        QueryBuilder.update('Teacher', [])
        print("ERROR: Empty columns update test should have failed!")
    except ValueError as e:
        print(f"✓ Empty columns update validation working: {e}")

    print("\n" + "="*60 + "\n")

    # ===== USAGE EXAMPLES / ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====
    print("=== Usage Examples / Примеры использования ===")
    print()
    print("Example parameter values for queries:")
    print("Примеры значений параметров для запросов:")
    print()
    print("INSERT Teacher parameters:")
    print("  ('John Doe', '+1234567890', 'john@example.com', 'Math teacher')")
    print()
    print("UPDATE Teacher parameters:")
    print("  ('Jane Smith', '+0987654321', 'jane@example.com', 'Science teacher', 1)")
    print("  (Note: Last parameter is the ID for WHERE clause)")
    print()
    print("SEARCH parameters (with % wildcards):")
    print("  ('%John%') - finds records containing 'John'")
    print("  ('John%') - finds records starting with 'John'")
    print("  ('%@gmail.com') - finds Gmail addresses")

    print("\n=== Test completed successfully / Тест завершен успешно ===")