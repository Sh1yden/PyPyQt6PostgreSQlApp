from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QLabel, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QPushButton, QVBoxLayout
import psycopg2
from src.core.Logger import Logger
from src.database.Connection import Connection


INSERT = """
    INSERT INTO "Teacher" ( f_fio, f_phone, f_email, f_comment )
        values ( %s, %s, %s, %s ) ;
"""

class Model(QStandardItemModel):

    # Добавьте сигнал
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Model.")
        self.lg.debug("Logger created in class Model().")

        self.condb = Connection()
        self.refresh_data()

    def refresh_data(self):
        """Загрузка данных из БД в модель"""
        try:
            rows = self.condb.execute_query("""SELECT * FROM "Teacher" ORDER by id""")

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
                        item = QStandardItem(str(cell_value) if cell_value is not None else "")
                        self.setItem(row_idx, col_idx, item)

                self.lg.debug("Model refresh data successfully. In DEF refresh_data()")
        except psycopg2.Error as e:
            self.lg.error(f"Model internal error: {e}. In DEF refresh_data()")
        except Exception as e:
            self.lg.critical(f"Model internal error: {e}. In DEF refresh_data()")

    # ! Может выдавать ошибку если не ввести данные!!!
    def add(self, fio, phone, email, comment):
        try:
            conn = self.condb.connect_to_db()
            cursor = conn.cursor()
            data = (fio, phone, email, comment)
            cursor.execute(INSERT, data)
            conn.commit()
            conn.close()
            self.refresh_data()
            self.lg.debug("Model add data successfully. In DEF add()")
        except Exception as e:
            self.lg.critical(f"Model internal error: {e}. In DEF add()")


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class View.")
        self.lg.debug("Logger created in class View().")

        self.teacher_model = Model(parent=self)
        self.setModel(self.teacher_model)

        self.setup_table_view()

    def setup_table_view(self):
        """Настройка внешнего вида таблицы"""
        # Растягиваем колонки по содержимому
        self.resizeColumnsToContents()

        # Разрешаем выделение строк
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # Запрещаем редактирование напрямую в таблице
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Включаем сортировку
        self.setSortingEnabled(True)

    def add(self):
        # Заглушка
        # QMessageBox.information(self, "Teacher", "Add")
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio,
                             dia.phone,
                             dia.email,
                             dia.comment)

    def uppdate(self):
        QMessageBox.information(self, "Teacher", "Edit")

    def delete(self):
        QMessageBox.information(self, "Teacher", "Delete")

class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Dialog.")
        self.lg.debug("Logger created in class Dialog().")

        fio_lbl = QLabel("Surname N. P.", parent=self)
        self.__fio_edit = QLineEdit(parent=self)
        phone_lbl = QLabel("Phone number", parent=self)
        self.__phone_edit = QLineEdit(parent=self)
        email_lbl = QLabel("Email", parent=self)
        self.__email_edit = QLineEdit(parent=self)
        comment_lbl = QLabel("Comment", parent=self)
        self.__comment_edit = QTextEdit(parent=self)

        ok_btn = QPushButton("OK", parent=self)
        cancel_btn = QPushButton("Cancel", parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edit)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.__phone_edit)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edit)
        lay.addWidget(comment_lbl)
        lay.addWidget(self.__comment_edit)

        lay_for_btn = QHBoxLayout()
        lay_for_btn.addWidget(ok_btn)
        lay_for_btn.addWidget(cancel_btn)
        lay.addLayout(lay_for_btn)

        ok_btn.clicked.connect(self.finish)
        cancel_btn.clicked.connect(self.reject)

    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            self.lg.debug("FIO not input")
            return
        self.lg.debug("FIO accepted")
        self.accept()

    @property
    def fio(self):
        result = self.__fio_edit.text().strip()
        if result == "":
            return None
        else:
            return result

    @property
    def phone(self):
        result = self.__phone_edit.text().strip()
        if result == "":
            return None
        else:
            return result

    @property
    def email(self):
        result = self.__email_edit.text().strip()
        if result == "":
            return None
        else:
            return result

    @property
    def comment(self):
        result = self.__comment_edit.toPlainText().strip()
        if result == "":
            return None
        else:
            return result
