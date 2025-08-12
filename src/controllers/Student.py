# Imports / Импорты
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QShortcut, QKeySequence
from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QLabel, QHBoxLayout, QHeaderView
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QPushButton, QVBoxLayout
import re
import psycopg2
from src.core.Logger import Logger
from src.database.Connection import Connection


# SQL Queries / SQL запросы
INSERT = """
    INSERT INTO "Student" ( f_fio, f_email, f_comment )
        values ( %s, %s, %s ) ;
"""

SELECT_ALL = """
    SELECT * FROM "Student" ORDER by id
"""

UPDATE = """
    UPDATE "Student" 
    SET f_fio = %s, f_email = %s, f_comment = %s
    WHERE id = %s ;
"""

DELETE = """
    DELETE FROM "Student" 
    WHERE id = %s ;
"""


# ===== MODEL CLASS / КЛАСС МОДЕЛИ =====
class Model(QStandardItemModel):
    """
    Model class for Student data / Класс модели для данных учеников
    Handles database operations and data validation / Обрабатывает операции с БД и валидацию данных
    """

    # Signals / Сигналы
    data_changed = pyqtSignal()  # Add signal / Добавьте сигнал

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Student Model.")
        self.lg.debug("Logger created in class Student Model().")

        # Column names storage / Хранение названий колонок
        self.column_names = []

        # Database connection / Подключение к БД
        self.condb = Connection()
        self.refresh_data()

    # ===== DATA OPERATIONS / ОПЕРАЦИИ С ДАННЫМИ =====
    def refresh_data(self):
        """Load data from database into model / Загрузка данных из БД в модель"""
        try:
            rows = self.condb.execute_query(SELECT_ALL)

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

                self.lg.debug("Student Model refresh data successfully. In DEF refresh_data().")
        except psycopg2.Error as e:
            self.lg.error(f"Student Model internal error: {e}. In DEF refresh_data().")
        except Exception as e:
            self.lg.critical(f"Student Model internal error: {e}. In DEF refresh_data().")

    def add(self, fio, email, comment):
        """Add new record to database / Добавление новой записи в БД"""
        # ! May throw error if no data entered! / ! Может выдавать ошибку если не ввести данные!!!
        try:
            self.condb.connect_to_db()
            self.condb.execute_query(INSERT, (fio, email, comment))
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("Student Model add data successfully. In DEF add().")
        except Exception as e:
            self.lg.critical(f"Student Model internal error: {e}. In DEF add().")

    def delete_record(self, record_id):
        """Delete record from database / Удаление записи из БД"""
        try:
            self.condb.connect_to_db()
            self.condb.execute_query(DELETE, (record_id,))
            self.refresh_data()
            self.condb.close_connection()

            self.lg.debug("Student Model delete data successfully. In DEF add().")
            return True
        except Exception as e:
            self.lg.critical(f"Student Model internal error: {e}. In DEF add().")

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
            self.lg.error(f"Student Model internal error: {e}. In DEF flags().")

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """Handle cell data changes / Обработка изменения данных в ячейке"""
        if role != Qt.ItemDataRole.EditRole:
            return False

        if not index.isValid():
            return False

        # Get value and validate / Получаем значение и проводим валидацию
        new_value = str(value).strip()
        column_name = self.column_names[index.column()]

        # Validation depending on column / Валидация в зависимости от колонки
        if not self._validate_data(column_name, new_value):
            return False

        # Get record ID (assuming ID is in first column) / Получаем ID записи (предполагаем что ID в первой колонке)
        id_item = self.item(index.row(), 0)
        if not id_item:
            self.lg.error("Student Model internal error: no id item. In DEF setData().")
            return False

        record_id = id_item.text()

        # Get all row data for update / Получаем все данные строки для обновления
        row_data = []
        for col_idx in range(1, self.columnCount()):  # Skip ID (column 0) / Пропускаем ID (колонка 0)
            if col_idx == index.column():
                row_data.append(new_value)  # New value / Новое значение
            else:
                item = self.item(index.row(), col_idx)
                row_data.append(item.text() if item else "")

        # Update in database / Обновляем в базе данных
        self.lg.debug("Student Model try to update db. In DEF setData().")
        try:
            self.condb.connect_to_db()
            self.condb.execute_query(UPDATE, (*row_data, record_id))
            self.condb.close_connection()

            # Update model / Обновляем модель
            result = super().setData(index, value, role)
            if result:
                self.data_changed.emit()
                self.lg.debug(
                    f"Student Model successfully updated {column_name} for record {record_id}. In DEF setData()."
                )
            return result
        except Exception as e:
            self.lg.error(f"Student Model internal error: {e}. In DEF setData().")
            QMessageBox.warning(None, "Update error",
                              f"Failed to update record: {str(e)}")
            return False

    # ===== VALIDATION / ВАЛИДАЦИЯ =====
    def _validate_data(self, column_name, value):
        """Data validation depending on column type / Валидация данных в зависимости от типа колонки"""
        if column_name == 'f_fio':
            if not value or len(value.strip()) < 2:
                self.lg.error(f"Student Model internal error: Validation error in FIO. In DEF _validate_data().")
                QMessageBox.warning(None, "Validation error",
                                  "The full name must contain at least 2 characters.")
                return False

        elif column_name == 'f_email':
            if value and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                self.lg.error(f"Student Model internal error: Validation error in EMAIL. In DEF _validate_data().")
                QMessageBox.warning(None, "Validation error",
                                  "Invalid email address format")
                return False
        return True


# ===== VIEW CLASS / КЛАСС ПРЕДСТАВЛЕНИЯ =====
class View(QTableView):
    """
    View class for displaying Student data / Класс представления для отображения данных учеников
    Handles user interface and interactions / Обрабатывает пользовательский интерфейс и взаимодействия
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Student View.")
        self.lg.debug("Logger created in class Student View().")

        # Model setup / Настройка модели
        self.student_model = Model(parent=self)
        self.setModel(self.student_model)

        # Table view setup / Настройка представления таблицы
        self.setup_table_view()

        # Signal connections / Подключение сигналов
        self.student_model.data_changed.connect(self.on_data_changed)

        # Keyboard shortcuts / Горячие клавиши
        # Delete key for deletion / Delete key для удаления
        delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
        delete_shortcut.activated.connect(self.delete)

        # Ctrl+Delete for multiple deletion / Ctrl+Delete для удаления нескольких записей
        delete_multiple_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Delete), self)
        delete_multiple_shortcut.activated.connect(self.delete_selected)

    # ===== SETUP METHODS / МЕТОДЫ НАСТРОЙКИ =====
    def setup_table_view(self):
        """Table appearance configuration / Настройка внешнего вида таблицы"""
        # Stretch columns to content / Растягиваем колонки по содержимому
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # And the last column to the end of the screen / И последнюю колонку до конца экрана
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        # Allow row selection / Разрешаем выделение строк
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # Direct table editing / Редактирование прямо в таблице
        self.setEditTriggers(QTableView.EditTrigger.DoubleClicked)

        # Enable sorting / Включаем сортировку
        self.setSortingEnabled(True)

        # Скрываем id / Скрываем id
        self.hideColumn(0)

        # Settings for better UX / Настройки для лучшего UX
        self.setAlternatingRowColors(True)  # Alternating row colors / Чередующиеся цвета строк
        self.setWordWrap(False)  # Disable word wrap / Отключаем перенос слов

        self.lg.debug("Student View setup table successfully. In DEF setup_table_view().")

    # ===== SLOT METHODS / МЕТОДЫ-СЛОТЫ =====
    @pyqtSlot()
    def on_data_changed(self):
        """Handle model data changes / Обработка изменения данных в модели"""
        self.lg.debug("Student View data changed in model, refreshing view. In DEF on_data_changed()")
        self.resizeColumnsToContents()

    # ===== CRUD OPERATIONS / ОПЕРАЦИИ CRUD =====
    def add(self):
        """Add new cell to model / Добавление новой ячейки в модель"""
        # Stub / Заглушка
        # QMessageBox.information(self, "Student", "Add")
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio,
                             dia.email,
                             dia.comment)

    def uppdate(self):
        """Information about direct table editing / Информация о редактировании напрямую в таблице"""
        QMessageBox.information(self, "Editing",
                              "For editing purposes:\n"
                              "• Double-click on the cell\n"
                              "The record ID cannot be edited")

    def delete(self):
        """Delete selected record / Удаление выбранной записи"""
        try:
            # Get selected row / Получаем выбранную строку
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Deletion",
                                      "Select an entry to delete")
                return

            # Get selected row index / Получаем индекс выбранной строки
            selected_row = selection[0].row()

            # Get record ID (assuming ID is in first column) / Получаем ID записи (предполагаем что ID в первой колонке)
            id_item = self.model().item(selected_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Error",
                                  "Couldn't get the record ID")
                return

            record_id = id_item.text()

            # Get FIO for confirmation dialog / Получаем ФИО для отображения в диалоге подтверждения
            fio_item = self.model().item(selected_row, 1)  # Assuming FIO is in second column / Предполагаем что ФИО во второй колонке
            fio = fio_item.text() if fio_item else "Is unknown"

            # Deletion confirmation dialog / Диалог подтверждения удаления
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete the entry?:\n\n"
                f"ID: {record_id}\n"
                f"FIO: {fio}\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Execute deletion / Выполняем удаление
                if self.model().delete_record(record_id):
                    QMessageBox.information(self, "Deletion",
                                          f"Record '{fio}' successfully deleted")
                    self.lg.debug(f"Student View: Successfully deleted record {record_id}")
                else:
                    QMessageBox.critical(self, "Error",
                                       "The record could not be deleted.\n"
                                       "Check the log for details.")
        except Exception as e:
            self.lg.error(f"Student View internal error: {e}. In DEF delete().")

    def delete_selected(self):
        try:
            """Delete all selected records / Удаление всех выбранных записей"""
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Deletion",
                                      "Select the entries to delete")
                return

            # Confirmation for multiple deletion / Подтверждение удаления нескольких записей
            count = len(selection)
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete {count} records?\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                deleted_count = 0
                failed_count = 0

                # Sort indices in descending order so deletion doesn't mess up numbering / Сортируем индексы по убыванию, чтобы удаление не сбивало нумерацию
                sorted_selection = sorted(selection, key=lambda x: x.row(), reverse=True)

                for index in sorted_selection:
                    row = index.row()
                    id_item = self.model().item(row, 0)

                    if id_item:
                        record_id = id_item.text()
                        if self.model().delete(record_id):
                            deleted_count += 1
                        else:
                            failed_count += 1

                # Results report / Отчет о результатах
                message = f"Deleted entries: {deleted_count}"
                if failed_count > 0:
                    message += f"\nCouldn't delete: {failed_count}"
                    QMessageBox.warning(self, "Deletion result", message)
                else:
                    QMessageBox.information(self, "Deletion result", message)
        except Exception as e:
            self.lg.error(f"Student View internal error: {e}. In DEF delete_selected().")


# ===== DIALOG CLASS / КЛАСС ДИАЛОГА =====
class Dialog(QDialog):
    """
    Dialog class for adding new student records / Класс диалога для добавления новых записей учеников
    Provides input form for student data / Предоставляет форму ввода для данных ученика
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Student Dialog.")
        self.lg.debug("Logger created in class Student Dialog().")

        self.setWindowTitle("Student")

        # Form labels and inputs / Метки и поля формы
        fio_lbl = QLabel("Surname N. P.", parent=self)
        self.__fio_edit = QLineEdit(parent=self)
        email_lbl = QLabel("Email", parent=self)
        self.__email_edit = QLineEdit(parent=self)
        comment_lbl = QLabel("Comment", parent=self)
        self.__comment_edit = QTextEdit(parent=self)

        # Dialog buttons / Кнопки диалога
        ok_btn = QPushButton("OK", parent=self)
        cancel_btn = QPushButton("Cancel", parent=self)

        # Layout setup / Настройка макета
        lay = QVBoxLayout(self)
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edit)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edit)
        lay.addWidget(comment_lbl)
        lay.addWidget(self.__comment_edit)

        # Button layout / Макет кнопок
        lay_for_btn = QHBoxLayout()
        lay_for_btn.addWidget(ok_btn)
        lay_for_btn.addWidget(cancel_btn)
        lay.addLayout(lay_for_btn)

        # Signal connections / Подключение сигналов
        ok_btn.clicked.connect(self.finish)
        cancel_btn.clicked.connect(self.reject)

    # ===== SLOT METHODS / МЕТОДЫ-СЛОТЫ =====
    @pyqtSlot()
    def finish(self):
        """Dialog completion handler / Обработчик завершения диалога"""
        if self.fio is None:
            self.lg.debug("Student Dialog not fio input. In DEF finish().")
            QMessageBox.information(self,
                                    "Please input Surname N.P!!!",
                                    "Please input Surname N.P!!! This is necessarily.")
            return
        self.accept()
        self.lg.debug("Student Dialog self.accept(). In DEF finish().")

    # ===== PROPERTY METHODS / МЕТОДЫ-СВОЙСТВА =====
    @property
    def fio(self):
        """Get FIO input value / Получение значения ввода ФИО"""
        result = self.__fio_edit.text().strip()
        if result == "":
            return None
        else:
            self.lg.debug("Student Dialog fio successfully. In DEF fio().")
            return result

    @property
    def email(self):
        """Get email input value / Получение значения ввода email"""
        result = self.__email_edit.text().strip()
        if result == "":
            self.lg.debug("Student Dialog not email input. In DEF email().")
            return None
        else:
            self.lg.debug("Student Dialog email successfully. In DEF email().")
            return result

    @property
    def comment(self):
        """Get comment input value / Получение значения ввода комментария"""
        result = self.__comment_edit.toPlainText().strip()
        if result == "":
            self.lg.debug("Student Dialog not comment input. In DEF comment().")
            return None
        else:
            self.lg.debug("Student Dialog comment successfully. In DEF comment().")
            return result