# TODO сделать review кода всех стандартных контроллеров, добавить подсказки, переделать логи.
#  TODO Заменить Model, View, Dialog в Teacher.py, Student.py, StGroup.py на базовые классы контроллеров
# Imports / Импорты
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
import psycopg2
from src.core.Logger import Logger
from src.database.Connection import Connection
from src.database.queries.QueryBuilder import QueryBuilder


# ===== MODEL CLASS / КЛАСС МОДЕЛИ =====
class BaseModel(QStandardItemModel):
    """
    Model class for data / Класс модели для данных
    Handles database operations and data validation / Обрабатывает операции с БД и валидацию данных
    """

    # Signals / Сигналы
    data_changed = pyqtSignal()

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, table_name: str, columns: list, parent=None):
        """
        Инициализация базовой модели

        Args:
            table_name: Имя таблицы в БД
            columns: Список колонок (без ID)
            parent: Родительский объект
        """
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class BaseModel.")
        self.lg.debug("Logger created in class BaseModel().")

        # Сохранение конфигурации
        self.table_name = table_name
        self.column_names = []  # Будет заполнено при загрузке данных

        # Генерация SQL запросов
        self.queries = {
            'select': QueryBuilder.select_all(table_name),
            'insert': QueryBuilder.insert(table_name, columns),
            'update': QueryBuilder.update(table_name, columns),
            'delete': QueryBuilder.delete(table_name)
        }

        self.lg.debug(f"BaseModel Generated queries for {table_name}: {self.queries}")

        # Database connection / Подключение к БД
        self.condb = Connection()

        # Загрузка данных
        self.refresh_data()

    # ===== DATA OPERATIONS / ОПЕРАЦИИ С ДАННЫМИ =====
    def refresh_data(self):
        """Load data from database into model / Загрузка данных из БД в модель"""
        try:
            rows = self.condb.execute_query(self.queries['select'])

            # Clear table before loading / Очищаем таблицу перед загрузкой
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)

            if rows:
                # Get column names / Получаем названия колонок
                self.column_names = list(rows[0].keys())
                columns = self.column_names

                # Configure table dimensions / Настраиваем размеры таблицы
                self.setRowCount(len(rows))
                self.setColumnCount(len(columns))
                self.setHorizontalHeaderLabels(columns)

                # Fill with data / Заполняем данными
                for row_idx, row in enumerate(rows):
                    for col_idx, column_name in enumerate(columns):
                        cell_value = row[column_name]
                        item = QStandardItem(str(cell_value) if cell_value is not None else "")
                        self.setItem(row_idx, col_idx, item)

                self.lg.debug("BaseModel refresh data successfully. In DEF refresh_data().")
        except psycopg2.Error as e:
            self.lg.error(f"BaseModel psycopg2 internal error: {e}. In DEF refresh_data().")
        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF refresh_data().")

    def add(self, *args):
        """Add new record to database / Добавление новой записи в БД"""
        # ! May throw error if no data entered! / ! Может выдавать ошибку если не ввести данные!!!
        try:
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries["insert"], args)
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("BaseModel add data successfully. In DEF add().")
            return True
        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF add().")
            return False

    def delete_record(self, record_id):
        """Delete record from database / Удаление записи из БД"""
        try:
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries["delete"], (record_id,))
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("BaseModel delete data successfully. In DEF delete_record().")
            return True
        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF delete_record().")
            return False

    # ===== EDITING OPERATIONS / ОПЕРАЦИИ РЕДАКТИРОВАНИЯ =====
    def flags(self, index):
        """Determine which cells can be edited / Определяет какие ячейки можно редактировать"""
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
        """Handle cell data changes / Обработка изменения данных в ячейке"""
        if role != Qt.ItemDataRole.EditRole or not index.isValid():
            return False

        try:
            new_value = str(value).strip()
            column_name = self.column_names[index.column()]

            # TODO добавить валидацию
            # ! Валидация данных
            # if not self._validate_data(column_name, new_value):
            #     return False

            # Получаем ID записи (первая колонка)
            id_item = self.item(index.row(), 0)
            if not id_item:
                self.lg.error(f"BaseModel {self.table_name} Model: no id item in setData")
                return False

            record_id = id_item.text()

            # Получаем все данные строки для обновления
            row_data = []
            for col_idx in range(1, self.columnCount()):  # Пропускаем ID (колонка 0)
                if col_idx == index.column():
                    row_data.append(new_value)  # Новое значение
                else:
                    item = self.item(index.row(), col_idx)
                    row_data.append(item.text() if item else "")

            # Обновляем в базе данных
            self.condb.connect_to_db()
            self.condb.execute_query(self.queries['update'], (*row_data, record_id))
            self.condb.close_connection()

            # Обновляем модель
            result = super().setData(index, value, role)
            if result:
                self.data_changed.emit()
                self.lg.debug(f"BaseModel {self.table_name} Model: updated {column_name} for record {record_id}")

            return result

        except Exception as e:
            self.lg.critical(f"BaseModel internal error: {e}. In DEF setData().")
            QMessageBox.warning(None, "Update error", f"Record could not be updated: {str(e)}")
