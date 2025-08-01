from PyQt6.QtCore import pyqtSlot
from PyQt6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QLabel, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QPushButton, QVBoxLayout
import psycopg2
from src.core.Logger import Logger
from src.database.Connection import Connection
from src.ui.widgets.TableView import TableView


INSERT = """
    INSERT INTO "Teacher" ( f_fio, f_phone, f_email, f_comment )
        values ( %s, %s, %s, %s ) ;
"""

class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Model.")
        self.lg.debug("Logger created in class Model().")

        self.condb = Connection()
        self.tabv = TableView()

    # ! Может выдавать ошибку если не ввести данные!!!
    def add(self, fio, phone, email, comment):
        try:
            # TODO connection to db добавить сюда нахуй
            conn = self.condb.connect_to_db()
            cursor = conn.cursor()
            data = (fio, phone, email, comment)
            cursor.execute(INSERT, data)
            conn.commit()
            # ! будущее место для обновления
            self.tabv.load_data("""
       SELECT * FROM "Teacher"
       """)
            conn.close()
        except Exception as e:
            self.lg.critical(f"Model internal error: {e}. In DEF add()")


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class View.")
        self.lg.debug("Logger created in class View().")

        model = Model(parent=self)
        self.setModel(model)

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
