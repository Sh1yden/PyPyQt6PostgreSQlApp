# ===== BASE MODEL CLASS FOR DATABASE OPERATIONS / БАЗОВЫЙ КЛАСС МОДЕЛИ ДЛЯ ОПЕРАЦИЙ С БАЗОЙ ДАННЫХ =====
# Universal model class for database table management
# Универсальный класс модели для управления таблицами базы данных

# TODO: Code review of all standard controllers, add hints, redo logs
# TODO: Replace Model, View, Dialog in Teacher.py, Student.py, StGroup.py with base controller classes
# TODO: сделать review кода всех стандартных контроллеров, добавить подсказки, переделать логи
# TODO: Заменить Model, View, Dialog в Teacher.py, Student.py, StGroup.py на базовые классы контроллеров

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
import psycopg2
from src.core.Logger import Logger
from src.database.Connection import Connection
from src.database.queries.QueryBuilder import QueryBuilder


# ===== BASE MODEL CLASS / БАЗОВЫЙ КЛАСС МОДЕЛИ =====
class BaseModel(QStandardItemModel):
    """
    Base model class for data management / Базовый класс модели для управления данными
    Handles database operations and data validation / Обрабатывает операции с БД и валидацию данных

    This class provides a unified interface for database operations across all entities.
    It extends QStandardItemModel to provide table view functionality with database integration.
    Supports CRUD operations, data validation, and automatic UI updates.

    Этот класс предоставляет унифицированный интерфейс для операций с базой данных для всех сущностей.
    Он расширяет QStandardItemModel для предоставления функциональности представления таблицы с интеграцией базы данных.
    Поддерживает операции CRUD, валидацию данных и автоматические обновления UI.
    """

    # ===== SIGNALS / СИГНАЛЫ =====
    # Signal emitted when data changes in the model / Сигнал, испускаемый при изменении данных в модели
    data_changed = pyqtSignal()

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self, table_name: str, columns: list, parent=None):
        """
        Initialize base model with database configuration / Инициализация базовой модели с конфигурацией базы данных

        Sets up the model for a specific database table with defined columns.
        Generates SQL queries automatically and establishes database connection.

        Настраивает модель для определенной таблицы базы данных с определенными столбцами.
        Генерирует SQL запросы автоматически и устанавливает подключение к базе данных.

        Args:
            table_name (str): Name of the database table / Имя таблицы в БД
            columns (list): List of column names (excluding ID) / Список колонок (без ID)
            parent: Parent object / Родительский объект
        """
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched in class BaseModel.")
        self.lg.debug("Logger created in class BaseModel().")

        # ===== CONFIGURATION STORAGE / СОХРАНЕНИЕ КОНФИГУРАЦИИ =====
        # Store table configuration for later use / Сохранение конфигурации таблицы для последующего использования
        self.table_name = table_name
        self.column_names = []  # Will be populated when loading data / Будет заполнено при загрузке данных

        # ===== SQL QUERY GENERATION / ГЕНЕРАЦИЯ SQL ЗАПРОСОВ =====
        # Generate all necessary CRUD queries using QueryBuilder / Генерация всех необходимых CRUD запросов с использованием QueryBuilder
        self.queries = {
            'select': QueryBuilder.select_all(table_name),
            'insert': QueryBuilder.insert(table_name, columns),
            'update': QueryBuilder.update(table_name, columns),
            'delete': QueryBuilder.delete(table_name)
        }

        self.lg.debug(f"BaseModel Generated queries for {table_name}: {self.queries}")

        # ===== DATABASE CONNECTION SETUP / НАСТРОЙКА ПОДКЛЮЧЕНИЯ К БД =====
        self.condb = Connection()

        # ===== INITIAL DATA LOAD / НАЧАЛЬНАЯ ЗАГРУЗКА ДАННЫХ =====
        self.refresh_data()

    # ===== PUBLIC METHODS - DATA OPERATIONS / ПУБЛИЧНЫЕ МЕТОДЫ - ОПЕРАЦИИ С ДАННЫМИ =====

    def refresh_data(self):
        """
        Load data from database into model / Загрузка данных из БД в модель

        Retrieves all records from the database table and populates the model.
        Clears existing data first to ensure consistency.
        Updates the UI automatically after loading.

        Получает все записи из таблицы базы данных и заполняет модель.
        Сначала очищает существующие данные для обеспечения согласованности.
        Автоматически обновляет пользовательский интерфейс после загрузки.
        """
        try:
            # Execute SELECT query to get all table data / Выполнение SELECT запроса для получения всех данных таблицы
            rows = self.condb.execute_query(self.queries['select'])

            # Clear table before loading new data / Очищаем таблицу перед загрузкой новых данных
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)

            if rows:
                # Extract column names from the first row / Извлечение имен колонок из первой строки
                self.column_names = list(rows[0].keys())
                columns = self.column_names

                # Configure table dimensions / Настраиваем размеры таблицы
                self.setRowCount(len(rows))
                self.setColumnCount(len(columns))
                self.setHorizontalHeaderLabels(columns)

                # Populate model with data / Заполняем модель данными
                for row_idx, row in enumerate(rows):
                    for col_idx, column_name in enumerate(columns):
                        cell_value = row[column_name]
                        # Create item with string representation of value / Создание элемента со строковым представлением значения
                        item = QStandardItem(str(cell_value) if cell_value is not None else "")
                        self.setItem(row_idx, col_idx, item)

                self.lg.debug("BaseModel refresh data successfully. In DEF refresh_data().")

        except psycopg2.Error as e:
            # Handle PostgreSQL specific errors / Обработка специфических ошибок PostgreSQL
            self.lg.error(f"BaseModel psycopg2 internal error: {e}. In DEF refresh_data().")
        except Exception as e:
            # Handle general exceptions / Обработка общих исключений
            self.lg.critical(f"BaseModel internal error: {e}. In DEF refresh_data().")

    def add(self, *args):
        """
        Add new record to database / Добавление новой записи в БД

        Inserts a new record with the provided data into the database table.
        Automatically refreshes the model after successful insertion.

        Вставляет новую запись с предоставленными данными в таблицу базы данных.
        Автоматически обновляет модель после успешной вставки.

        ! May throw error if no data entered! / ! Может выдавать ошибку если не ввести данные!!!

        Args:
            *args: Variable number of arguments matching table columns / Переменное количество аргументов, соответствующих столбцам таблицы

        Returns:
            bool: True if successful, False otherwise / True при успехе, False в противном случае
        """
        try:
            # Establish connection and execute INSERT query / Установка соединения и выполнение INSERT запроса
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries["insert"], args)
            # Refresh model to show new data / Обновление модели для отображения новых данных
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("BaseModel add data successfully. In DEF add().")
            return True
        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF add().")
            return False

    def delete_record(self, record_id):
        """
        Delete record from database / Удаление записи из БД

        Removes a record with the specified ID from the database table.
        Automatically refreshes the model after successful deletion.

        Удаляет запись с указанным ID из таблицы базы данных.
        Автоматически обновляет модель после успешного удаления.

        Args:
            record_id: ID of the record to delete / ID записи для удаления

        Returns:
            bool: True if successful, False otherwise / True при успехе, False в противном случае
        """
        try:
            # Establish connection and execute DELETE query / Установка соединения и выполнение DELETE запроса
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries["delete"], (record_id,))
            # Refresh model to reflect deletion / Обновление модели для отражения удаления
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("BaseModel delete data successfully. In DEF delete_record().")
            return True
        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF delete_record().")
            return False

    # ===== OVERRIDE METHODS - EDITING OPERATIONS / ПЕРЕОПРЕДЕЛЕННЫЕ МЕТОДЫ - ОПЕРАЦИИ РЕДАКТИРОВАНИЯ =====

    def flags(self, index):
        """
        Determine which cells can be edited / Определяет какие ячейки можно редактировать

        Controls the editing behavior of individual cells in the table view.
        ID column (first column) is read-only, other columns are editable.

        Управляет поведением редактирования отдельных ячеек в представлении таблицы.
        Столбец ID (первый столбец) только для чтения, остальные столбцы редактируемы.

        Args:
            index: Model index of the cell / Индекс модели ячейки

        Returns:
            Qt.ItemFlag: Flags determining cell behavior / Флаги, определяющие поведение ячейки
        """
        try:
            if not index.isValid():
                return Qt.ItemFlag.NoItemFlags

            # ID column cannot be edited (assuming it's the first column) / ID колонку нельзя редактировать (предполагаем что это первая колонка)
            if index.column() == 0:
                return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

            # Other columns can be edited / Остальные колонки можно редактировать
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable
        except Exception as e:
            self.lg.error(f"BaseModel internal error: {e}. In DEF flags().")
            return Qt.ItemFlag.NoItemFlags

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """
        Handle cell data changes / Обработка изменения данных в ячейке

        Processes user edits in table cells and updates the corresponding database record.
        Validates the index and value before executing the update query.
        Emits data_changed signal on successful update.

        Обрабатывает пользовательские правки в ячейках таблицы и обновляет соответствующую запись базы данных.
        Проверяет индекс и значение перед выполнением запроса обновления.
        Испускает сигнал data_changed при успешном обновлении.

        Args:
            index: Model index of the edited cell / Индекс модели редактируемой ячейки
            value: New value for the cell / Новое значение для ячейки
            role: Data role (usually EditRole) / Роль данных (обычно EditRole)

        Returns:
            bool: True if update successful, False otherwise / True если обновление успешно, False в противном случае
        """
        # Only process edit role changes on valid indices / Обрабатывать только изменения роли редактирования для действительных индексов
        if role != Qt.ItemDataRole.EditRole or not index.isValid():
            return False

        try:
            # Clean and validate new value / Очистка и валидация нового значения
            new_value = str(value).strip()
            column_name = self.column_names[index.column()]

            # TODO: Add data validation / TODO добавить валидацию данных
            # ! Data validation placeholder / ! Заглушка валидации данных
            # if not self._validate_data(column_name, new_value):
            #     return False

            # Get record ID from first column / Получаем ID записи (первая колонка)
            id_item = self.item(index.row(), 0)
            if not id_item:
                self.lg.error(f"BaseModel {self.table_name} Model: no id item in setData")
                return False

            record_id = id_item.text()

            # Collect all row data for update query / Сбор всех данных строки для запроса обновления
            row_data = []
            for col_idx in range(1, self.columnCount()):  # Skip ID column (column 0) / Пропускаем ID (колонка 0)
                if col_idx == index.column():
                    row_data.append(new_value)  # Use new value / Используем новое значение
                else:
                    item = self.item(index.row(), col_idx)
                    row_data.append(item.text() if item else "")

            # Execute database update / Выполнение обновления базы данных
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries['update'], (*row_data, record_id))
            self.condb.close_connection()

            # Update model and emit signal / Обновление модели и испускание сигнала
            result = super().setData(index, value, role)
            if result:
                self.data_changed.emit()
                self.lg.debug(f"BaseModel {self.table_name} Model: updated {column_name} for record {record_id}")

            return result

        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF setData().")
            # Show user-friendly error message / Показать удобное для пользователя сообщение об ошибке
            QMessageBox.warning(None, "Update error", f"Record could not be updated: {str(e)}")
            return False