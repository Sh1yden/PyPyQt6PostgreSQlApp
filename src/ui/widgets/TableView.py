# TODO сделать отрисовку всех таблиц бд.
# TODO переписать нахуй
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from src.core.Logger import Logger
import psycopg2
from psycopg2.extras import RealDictCursor
from src.database.Connection import Connection

class TableView(QWidget):
   """Класс для отображения таблицы из базы данных через psycopg2."""

   def __init__(self, table_name, parent=None):
       super().__init__(parent)

       # Инициализация логера
       self.lg = Logger()
       self.lg.debug("Constructor launched in class TableView.")
       self.lg.debug("Logger created in class TableView().")

       self.table_name = table_name
       self.db_config = Connection()
       self.connection = None
       self.table_widget = None
       self.data = []
       self.columns = []

       self._init_ui()
       self._connect_db()
       self._load_data()
       self._populate_table()

   def _init_ui(self):
       """Инициализация пользовательского интерфейса."""
       try:
           layout = QVBoxLayout()
           self.table_widget = QTableWidget()
           layout.addWidget(self.table_widget)
           self.setLayout(layout)

           self.lg.debug("TableView setLayout successfully. In DEF _setup_model()")
       except Exception as e:
           self.lg.critical(f"TableView internal error: {e}. In DEF _setup_model()")

   def _connect_db(self):
       """Подключение к базе данных через psycopg2."""
       try:
           self.connection = psycopg2.connect(**self.db_config.db_set_var)
           self.lg.debug("Database connection established successfully.")
       except Exception as e:
           self.lg.critical(f"Database connection error: {e}")

   def _load_data(self):
       """Загрузка данных из таблицы."""
       if not self.connection:
           return

       try:
           with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
               cursor.execute(f"""
                        SELECT * FROM "{self.table_name}"
               """)
               rows = cursor.fetchall()

               if rows:
                   self.columns = list(rows[0].keys())
                   self.data = [list(row.values()) for row in rows]
               else:
                   # Получаем названия колонок даже если данных нет
                   cursor.execute(f"""
                       SELECT column_name 
                       FROM information_schema.columns 
                       WHERE table_name = "{self.table_name}"
                       ORDER BY ordinal_position
                   """)
                   self.columns = [row[0] for row in cursor.fetchall()]
                   self.data = []

           self.lg.debug(f"Data loaded successfully from {self.table_name}")
       except Exception as e:
           self.lg.error(f"Error loading data from {self.table_name}: {e}")

   def _populate_table(self):
       """Заполнение QTableWidget данными."""
       try:
           # Установка размеров таблицы
           self.table_widget.setRowCount(len(self.data))
           self.table_widget.setColumnCount(len(self.columns))

           # Установка заголовков
           self.table_widget.setHorizontalHeaderLabels(self.columns)

           # Заполнение данными
           for row_idx, row_data in enumerate(self.data):
               for col_idx, cell_data in enumerate(row_data):
                   item = QTableWidgetItem(str(cell_data) if cell_data is not None else "")
                   self.table_widget.setItem(row_idx, col_idx, item)

           self._configure_view()
           self.lg.debug("Table populated successfully.")
       except Exception as e:
           self.lg.error(f"Error populating table: {e}")

   def _configure_view(self):
       """Настройка внешнего вида таблицы."""
       try:
           # Автоматическое изменение размера столбцов
           self.table_widget.resizeColumnsToContents()
           # Включение сортировки
           self.table_widget.setSortingEnabled(True)
           # Выделение целых строк
           self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
           # Альтернативные цвета строк
           self.table_widget.setAlternatingRowColors(True)
           # Растягивание последнего столбца
           self.table_widget.horizontalHeader().setStretchLastSection(True)
           # Запрет редактирования
           self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

           self.lg.debug("Table view configured successfully.")
       except Exception as e:
           self.lg.error(f"Error configuring table view: {e}")

   def refresh_data(self):
       """Обновление данных в таблице."""
       self._load_data()
       self._populate_table()

   def closeeEvent(self, event):
       """Закрытие соединения при закрытии виджета."""
       if self.connection:
           self.connection.close()
           self.lg.debug("Database connection closed.")
       event.accept()