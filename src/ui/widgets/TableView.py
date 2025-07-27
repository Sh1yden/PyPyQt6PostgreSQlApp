# TODO сделать отрисовку всех таблиц бд.
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase
from src.core.Logger import Logger


class TableView(QWidget):
   """Класс для отображения таблицы из базы данных."""

   def __init__(self, table_name, parent=None):
       super().__init__(parent)

       # Инициализация логера
       self.lg = Logger()
       self.lg.debug("Constructor launched in class TableView.")
       self.lg.debug("Logger created in class TableView().")

       self.table_name = table_name
       self.model = None
       self.table_view = None

       self._init_ui()
       self._setup_model()

   def _init_ui(self):
       """Инициализация пользовательского интерфейса."""
       try:
           # Создание layout
           layout = QVBoxLayout()
           # Создание QTableView
           self.table_view = QTableView()
           layout.addWidget(self.table_view)

           self.setLayout(layout)
           self.lg.debug("UI initialized in TableView.")
       except Exception as e:
           self.lg.critical(f"TableView UI initialization error: {e}")

   def _setup_model(self):
       """Настройка модели данных."""
       try:
           # Получение соединения с БД (используется дефолтное соединение)
           db = QSqlDatabase.database()

           if not db.isOpen():
               self.lg.error("Database connection is not open in TableView.")
               return
           # Создание модели
           self.model = QSqlTableModel(db=db, parent=self)
           self.model.setTable(self.table_name)
           # Стратегия редактирования - сохранение при смене поля
           self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
           # Загрузка данных
           if not self.model.select():
               self.lg.error(f"Failed to select data from table {self.table_name}")
               return
           # Связывание модели с представлением
           self.table_view.setModel(self.model)
           # Настройка представления
           self._configure_view()

           self.lg.debug(f"Model setup completed for table {self.table_name}.")
       except Exception as e:
           self.lg.critical(f"TableView model setup error: {e}")

   def _configure_view(self):
       """Настройка внешнего вида таблицы."""
       try:
           # Автоматическое изменение размера столбцов под содержимое
           self.table_view.resizeColumnsToContents()
           # Включение сортировки по клику на заголовок
           self.table_view.setSortingEnabled(True)
           # Выделение целых строк при клике
           self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
           # Альтернативные цвета строк для лучшей читаемости
           self.table_view.setAlternatingRowColors(True)
           # Растягивание последнего столбца на всю ширину
           self.table_view.horizontalHeader().setStretchLastSection(True)

           self.lg.debug("Table view configured successfully.")
       except Exception as e:
           self.lg.critical(f"TableView configuration error: {e}")
