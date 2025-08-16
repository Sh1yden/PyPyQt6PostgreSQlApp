

# ===== SQL QUERY BUILDER / ГЕНЕРАТОР SQL ЗАПРОСОВ =====
class QueryBuilder:
    """
    Генератор базовых CRUD запросов для таблиц.
    Избегает дублирования кода и обеспечивает единообразие запросов
    """
    
    @staticmethod
    def select_all(table_name: str) -> str:
        """
        Генерирует запрос для получения всех записей из таблицы
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            SQL запрос для SELECT
        """
        return f'SELECT * FROM "{table_name}" ORDER BY id'
    
    @staticmethod
    def select_by_id(table_name: str) -> str:
        """
        Генерирует запрос для получения записи по ID
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            SQL запрос для SELECT по ID
        """
        return f'SELECT * FROM "{table_name}" WHERE id = %s'
    
    @staticmethod
    def insert(table_name: str, columns: list) -> str:
        """
        Генерирует запрос для вставки новой записи
        
        Args:
            table_name: Имя таблицы
            columns: Список названий колонок
            
        Returns:
            SQL запрос для INSERT
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")
            
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        return f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'
    
    @staticmethod
    def update(table_name: str, columns: list) -> str:
        """
        Генерирует запрос для обновления записи
        
        Args:
            table_name: Имя таблицы
            columns: Список названий колонок (без ID)
            
        Returns:
            SQL запрос для UPDATE
        """
        if not columns:
            raise ValueError("Columns list cannot be empty")
            
        set_clause = ', '.join([f'{col} = %s' for col in columns])
        return f'UPDATE "{table_name}" SET {set_clause} WHERE id = %s'
    
    @staticmethod
    def delete(table_name: str) -> str:
        """
        Генерирует запрос для удаления записи
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            SQL запрос для DELETE
        """
        return f'DELETE FROM "{table_name}" WHERE id = %s'
    
    @staticmethod
    def count(table_name: str) -> str:
        """
        Генерирует запрос для подсчета записей
        
        Args:
            table_name: Имя таблицы
            
        Returns:
            SQL запрос для COUNT
        """
        return f'SELECT COUNT(*) FROM "{table_name}"'


# ===== СПЕЦИАЛИЗИРОВАННЫЕ ЗАПРОСЫ / SPECIALIZED QUERIES =====
class AdvancedQueryBuilder(QueryBuilder):
    """
    Расширенный генератор запросов для сложных случаев
    """
    
    @staticmethod
    def search_by_field(table_name: str, field_name: str) -> str:
        """
        Генерирует запрос для поиска по полю
        """
        return f'SELECT * FROM "{table_name}" WHERE {field_name} ILIKE %s ORDER BY id'
    
    @staticmethod
    def select_with_limit(table_name: str, limit: int, offset: int = 0) -> str:
        """
        Генерирует запрос с ограничением количества записей
        """
        return f'SELECT * FROM "{table_name}" ORDER BY id LIMIT {limit} OFFSET {offset}'


# ===== ТЕСТИРОВАНИЕ / TESTING =====
if __name__ == '__main__':
    # Тестирование генератора запросов
    print("=== Тестирование QueryBuilder ===")
    
    # Тест для Teacher
    teacher_columns = ['f_fio', 'f_phone', 'f_email', 'f_comment']
    print("Teacher queries:")
    print(f"SELECT: {QueryBuilder.select_all('Teacher')}")
    print(f"INSERT: {QueryBuilder.insert('Teacher', teacher_columns)}")
    print(f"UPDATE: {QueryBuilder.update('Teacher', teacher_columns)}")
    print(f"DELETE: {QueryBuilder.delete('Teacher')}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест для Student
    student_columns = ['f_fio', 'f_email', 'f_comment']
    print("Student queries:")
    print(f"SELECT: {QueryBuilder.select_all('Student')}")
    print(f"INSERT: {QueryBuilder.insert('Student', student_columns)}")
    print(f"UPDATE: {QueryBuilder.update('Student', student_columns)}")
    print(f"DELETE: {QueryBuilder.delete('Student')}")