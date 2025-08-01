# TODO сделать отрисовку всех таблиц бд.
# TODO переписать нахуй
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from src.core.Logger import Logger
import psycopg2
from src.database.Connection import Connection

class TableView(QTableWidget):
   """Класс для отображения таблицы из базы данных через psycopg2."""

   # Конструктор класса.
   def __init__(self, parent=None):
       super().__init__(parent)

       # Инициализация логера
       self.lg = Logger()
       self.lg.debug("Constructor launched in class TableView.")
       self.lg.debug("Logger created in class TableView().")

       self.condb = Connection()

       self.load_data("""
       SELECT * FROM "Teacher" ORDER by id
       """)

   def load_data(self, query, params=None):
        try:
            self.lg.debug("load_data ON")

            rows = self.condb.execute_query(query)

            # Очищаем таблицу перед загрузкой
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)

            if rows:
                # Получаем названия колонок
                columns = list(rows[0].keys())

                # Настраиваем размеры таблицы
                self.setRowCount(len(rows))
                self.setColumnCount(len(columns))
                self.setHorizontalHeaderLabels(columns)

                # Заполняем данными
                for row_idx, row in enumerate(rows):
                    for col_idx, column_name in enumerate(columns):
                        cell_value = row[column_name]
                        item = QTableWidgetItem(str(cell_value) if cell_value is not None else "")
                        self.setItem(row_idx, col_idx, item)
        except psycopg2.Error as e:
            print(f"Ошибка PostgreSQL: {e}")
        except Exception as e:
            print(f"Общая ошибка: {e}")

   def refresh(self):
       self.model.select()