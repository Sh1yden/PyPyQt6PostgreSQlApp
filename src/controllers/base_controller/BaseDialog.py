from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QTextEdit, QPushButton, QMessageBox)
import re
from src.core.Logger import Logger


# ===== BASE DIALOG CLASS / БАЗОВЫЙ КЛАСС ДИАЛОГА =====
class BaseDialog(QDialog):
    """
    Базовый класс диалога для всех сущностей
    Обеспечивает унифицированный интерфейс ввода данных
    """

    def __init__(self, window_title: str, fields: list, parent=None):
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Teacher Dialog.")
        self.lg.debug("Logger created in class Teacher Dialog().")

        self.set_window_dialog(window_title, fields)

    def set_window_dialog(self, window_title: str, privilege: list):

        # Настройка диалога
        self.setWindowTitle(window_title)
        self.setModal(True)
        self.resize(400, 300)

        # Layout setup / Настройка макета
        lay = QVBoxLayout(self)

        # Form labels and inputs / Метки и поля формы
        if "fio" in privilege:
            fio_lbl = QLabel("Surname N. P.", parent=self)
            self.__fio_edit = QLineEdit(parent=self)

            lay.addWidget(fio_lbl)
            lay.addWidget(self.__fio_edit)

        if "title" in privilege:
            fio_lbl = QLabel("Title Group", parent=self)
            self.__fio_edit = QLineEdit(parent=self)

            lay.addWidget(fio_lbl)
            lay.addWidget(self.__fio_edit)

        if "phone" in privilege:
            phone_lbl = QLabel("Phone number", parent=self)
            self.__phone_edit = QLineEdit(parent=self)

            lay.addWidget(phone_lbl)
            lay.addWidget(self.__phone_edit)

        if "email" in privilege:
            email_lbl = QLabel("Email", parent=self)
            self.__email_edit = QLineEdit(parent=self)

            lay.addWidget(email_lbl)
            lay.addWidget(self.__email_edit)

        if "comment" in privilege:
            comment_lbl = QLabel("Comment", parent=self)
            self.__comment_edit = QTextEdit(parent=self)

            lay.addWidget(comment_lbl)
            lay.addWidget(self.__comment_edit)

        # Dialog buttons / Кнопки диалога
        ok_btn = QPushButton("OK", parent=self)
        cancel_btn = QPushButton("Cancel", parent=self)

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
            self.lg.debug("Teacher Dialog not fio input. In DEF finish().")
            QMessageBox.information(self,
                                    "Please input Surname N.P!!!",
                                    "Please input Surname N.P!!! This is necessarily.")
            return
        self.accept()
        self.lg.debug("Teacher Dialog self.accept(). In DEF finish().")

    # ===== PROPERTY METHODS / МЕТОДЫ-СВОЙСТВА =====
    @property
    def fio(self):
        """Get FIO input value / Получение значения ввода ФИО"""
        result = self.__fio_edit.text().strip()
        if result == "":
            return None
        else:
            self.lg.debug("Teacher Dialog fio successfully. In DEF fio().")
            return result

    @property
    def phone(self):
        """Get phone input value / Получение значения ввода телефона"""
        result = self.__phone_edit.text().strip()
        if result == "":
            self.lg.debug("Teacher Dialog not phone input. In DEF phone().")
            return None
        else:
            self.lg.debug("Teacher Dialog phone successfully. In DEF phone().")
            return result

    @property
    def email(self):
        """Get email input value / Получение значения ввода email"""
        result = self.__email_edit.text().strip()
        if result == "":
            self.lg.debug("Teacher Dialog not email input. In DEF email().")
            return None
        else:
            self.lg.debug("Teacher Dialog email successfully. In DEF email().")
            return result

    @property
    def comment(self):
        """Get comment input value / Получение значения ввода комментария"""
        result = self.__comment_edit.toPlainText().strip()
        if result == "":
            self.lg.debug("Teacher Dialog not comment input. In DEF comment().")
            return None
        else:
            self.lg.debug("Teacher Dialog comment successfully. In DEF comment().")
            return result