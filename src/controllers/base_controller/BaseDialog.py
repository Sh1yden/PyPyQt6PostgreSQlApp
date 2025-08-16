# ===== BASE DIALOG CLASS FOR DATA INPUT / БАЗОВЫЙ КЛАСС ДИАЛОГА ДЛЯ ВВОДА ДАННЫХ =====
# Universal dialog class for creating and editing database records
# Универсальный класс диалога для создания и редактирования записей базы данных

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QTextEdit, QPushButton, QMessageBox)
import re
from src.core.Logger import Logger


# ===== BASE DIALOG CLASS / БАЗОВЫЙ КЛАСС ДИАЛОГА =====
class BaseDialog(QDialog):
    """
    Base dialog class for all entities / Базовый класс диалога для всех сущностей
    Provides unified input interface for data entry / Обеспечивает унифицированный интерфейс ввода данных
    
    This class creates dynamic input forms based on field specifications.
    It handles validation, user interaction, and data collection for database operations.
    Supports various input types including text fields and text areas.
    
    Этот класс создает динамические формы ввода на основе спецификаций полей.
    Он обрабатывает валидацию, взаимодействие с пользователем и сбор данных для операций с базой данных.
    Поддерживает различные типы ввода, включая текстовые поля и текстовые области.
    """

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self, window_title: str, fields: list, parent=None):
        """
        Initialize base dialog with dynamic field generation / Инициализация базового диалога с динамической генерацией полей
        
        Creates a dialog window with input fields based on the provided field list.
        Sets up validation, layout, and user interaction components.
        
        Создает диалоговое окно с полями ввода на основе предоставленного списка полей.
        Настраивает валидацию, макет и компоненты взаимодействия с пользователем.
        
        Args:
            window_title (str): Title displayed in dialog window / Заголовок, отображаемый в диалоговом окне
            fields (list): List of field names to create input controls for / Список имен полей для создания элементов ввода
            parent: Parent widget / Родительский виджет
        """
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched in class BaseDialog.")
        self.lg.debug("Logger created in class BaseDialog().")

        # ===== DIALOG SETUP / НАСТРОЙКА ДИАЛОГА =====
        self.set_window_dialog(window_title, fields)

    # ===== PRIVATE METHODS - UI SETUP / ПРИВАТНЫЕ МЕТОДЫ - НАСТРОЙКА UI =====
    
    def set_window_dialog(self, window_title: str, privilege: list):
        """
        Configure dialog window and create input fields / Настройка диалогового окна и создание полей ввода
        
        Dynamically creates input controls based on the privilege (field) list.
        Sets up window properties, layouts, and button controls.
        Connects signals for user interaction handling.
        
        Динамически создает элементы ввода на основе списка привилегий (полей).
        Настраивает свойства окна, макеты и элементы управления кнопками.
        Подключает сигналы для обработки взаимодействия с пользователем.
        
        Args:
            window_title (str): Window title / Заголовок окна
            privilege (list): List of field names to create / Список имен полей для создания
        """
        # ===== WINDOW CONFIGURATION / КОНФИГУРАЦИЯ ОКНА =====
        self.setWindowTitle(window_title)
        self.setModal(True)  # Make dialog modal / Сделать диалог модальным
        self.resize(400, 300)  # Set default size / Установить размер по умолчанию

        # ===== LAYOUT SETUP / НАСТРОЙКА МАКЕТА =====
        lay = QVBoxLayout(self)

        # ===== DYNAMIC FIELD CREATION / ДИНАМИЧЕСКОЕ СОЗДАНИЕ ПОЛЕЙ =====
        
        # ===== FIO FIELD (Full Name) / ПОЛЕ ФИО (Полное имя) =====
        if "fio" in privilege:
            fio_lbl = QLabel("Surname N. P.", parent=self)  # Full name label / Метка полного имени
            self.__fio_edit = QLineEdit(parent=self)  # Text input for name / Текстовый ввод для имени

            lay.addWidget(fio_lbl)
            lay.addWidget(self.__fio_edit)

        # ===== TITLE FIELD (Group Title) / ПОЛЕ ЗАГОЛОВКА (Название группы) =====
        if "title" in privilege:
            title_lbl = QLabel("Title Group", parent=self)  # Group title label / Метка названия группы
            self.__fio_edit = QLineEdit(parent=self)  # Reusing fio_edit for title / Повторное использование fio_edit для заголовка

            lay.addWidget(title_lbl)
            lay.addWidget(self.__fio_edit)

        # ===== PHONE FIELD / ПОЛЕ ТЕЛЕФОНА =====
        if "phone" in privilege:
            phone_lbl = QLabel("Phone number", parent=self)  # Phone label / Метка телефона
            self.__phone_edit = QLineEdit(parent=self)  # Text input for phone / Текстовый ввод для телефона

            lay.addWidget(phone_lbl)
            lay.addWidget(self.__phone_edit)

        # ===== EMAIL FIELD / ПОЛЕ EMAIL =====
        if "email" in privilege:
            email_lbl = QLabel("Email", parent=self)  # Email label / Метка email
            self.__email_edit = QLineEdit(parent=self)  # Text input for email / Текстовый ввод для email

            lay.addWidget(email_lbl)
            lay.addWidget(self.__email_edit)

        # ===== COMMENT FIELD / ПОЛЕ КОММЕНТАРИЯ =====
        if "comment" in privilege:
            comment_lbl = QLabel("Comment", parent=self)  # Comment label / Метка комментария
            self.__comment_edit = QTextEdit(parent=self)  # Multi-line text input for comments / Многострочный ввод для комментариев

            lay.addWidget(comment_lbl)
            lay.addWidget(self.__comment_edit)

        # ===== BUTTON SETUP / НАСТРОЙКА КНОПОК =====
        ok_btn = QPushButton("OK", parent=self)  # Confirm button / Кнопка подтверждения
        cancel_btn = QPushButton("Cancel", parent=self)  # Cancel button / Кнопка отмены

        # ===== BUTTON LAYOUT / МАКЕТ КНОПОК =====
        lay_for_btn = QHBoxLayout()  # Horizontal layout for buttons / Горизонтальный макет для кнопок
        lay_for_btn.addWidget(ok_btn)
        lay_for_btn.addWidget(cancel_btn)
        lay.addLayout(lay_for_btn)

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        ok_btn.clicked.connect(self.finish)  # Connect OK button to finish method / Подключить кнопку OK к методу finish
        cancel_btn.clicked.connect(self.reject)  # Connect Cancel button to reject method / Подключить кнопку Cancel к методу reject

    # ===== SLOT METHODS - EVENT HANDLERS / МЕТОДЫ-СЛОТЫ - ОБРАБОТЧИКИ СОБЫТИЙ =====
    
    @pyqtSlot()
    def finish(self):
        """
        Dialog completion handler / Обработчик завершения диалога
        
        Validates required fields before accepting the dialog.
        Shows error messages if validation fails.
        Accepts the dialog if all required data is provided.
        
        Проверяет обязательные поля перед принятием диалога.
        Показывает сообщения об ошибках, если валидация не пройдена.
        Принимает диалог, если все необходимые данные предоставлены.
        """
        # ===== REQUIRED FIELD VALIDATION / ВАЛИДАЦИЯ ОБЯЗАТЕЛЬНЫХ ПОЛЕЙ =====
        if self.fio is None:
            self.lg.debug("BaseDialog: No FIO input provided. In DEF finish().")
            QMessageBox.information(self,
                                    "Please input Surname N.P!!!",
                                    "Please input Surname N.P!!! This is necessary.")
            return
            
        # ===== DIALOG ACCEPTANCE / ПРИНЯТИЕ ДИАЛОГА =====
        self.accept()  # Close dialog with acceptance / Закрыть диалог с принятием
        self.lg.debug("BaseDialog: Dialog accepted successfully. In DEF finish().")

    # ===== PROPERTY METHODS - DATA ACCESS / МЕТОДЫ-СВОЙСТВА - ДОСТУП К ДАННЫМ =====
    
    @property
    def fio(self):
        """
        Get FIO (Full Name) input value / Получение значения ввода ФИО (Полное имя)
        
        Returns the cleaned FIO input or None if empty.
        Performs basic validation and logging.
        
        Возвращает очищенный ввод ФИО или None, если пустой.
        Выполняет базовую валидацию и логирование.
        
        Returns:
            str or None: Cleaned FIO string or None if empty / Очищенная строка ФИО или None если пустая
        """
        result = self.__fio_edit.text().strip()
        if result == "":
            return None
        else:
            self.lg.debug("BaseDialog: FIO input successful. In DEF fio().")
            return result

    @property
    def phone(self):
        """
        Get phone input value / Получение значения ввода телефона
        
        Returns the cleaned phone input or None if empty.
        Performs basic validation and logging.
        
        Возвращает очищенный ввод телефона или None, если пустой.
        Выполняет базовую валидацию и логирование.
        
        Returns:
            str or None: Cleaned phone string or None if empty / Очищенная строка телефона или None если пустая
        """
        result = self.__phone_edit.text().strip()
        if result == "":
            self.lg.debug("BaseDialog: No phone input provided. In DEF phone().")
            return None
        else:
            self.lg.debug("BaseDialog: Phone input successful. In DEF phone().")
            return result

    @property
    def email(self):
        """
        Get email input value / Получение значения ввода email
        
        Returns the cleaned email input or None if empty.
        Could be extended with email format validation.
        
        Возвращает очищенный ввод email или None, если пустой.
        Может быть расширен валидацией формата email.
        
        Returns:
            str or None: Cleaned email string or None if empty / Очищенная строка email или None если пустая
        """
        result = self.__email_edit.text().strip()
        if result == "":
            self.lg.debug("BaseDialog: No email input provided. In DEF email().")
            return None
        else:
            # TODO: Add email format validation / TODO: Добавить валидацию формата email
            self.lg.debug("BaseDialog: Email input successful. In DEF email().")
            return result

    @property
    def comment(self):
        """
        Get comment input value / Получение значения ввода комментария
        
        Returns the cleaned comment input or None if empty.
        Handles multi-line text input from QTextEdit.
        
        Возвращает очищенный ввод комментария или None, если пустой.
        Обрабатывает многострочный текстовый ввод из QTextEdit.
        
        Returns:
            str or None: Cleaned comment string or None if empty / Очищенная строка комментария или None если пустая
        """
        result = self.__comment_edit.toPlainText().strip()
        if result == "":
            self.lg.debug("BaseDialog: No comment input provided. In DEF comment().")
            return None
        else:
            self.lg.debug("BaseDialog: Comment input successful. In DEF comment().")
            return result


# ===== MAIN EXECUTION BLOCK - FOR TESTING / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ДЛЯ ТЕСТИРОВАНИЯ =====
if __name__ == '__main__':
    # This block can be used for testing BaseDialog functionality independently
    # Этот блок может использоваться для независимого тестирования функциональности BaseDialog
    from PyQt6.QtWidgets import QApplication
    import sys
    
    print("=== BaseDialog Testing Mode / Режим тестирования BaseDialog ===")
    
    # Create test application / Создание тестового приложения
    app = QApplication(sys.argv)
    
    # Create test dialog with all field types / Создание тестового диалога со всеми типами полей
    test_dialog = BaseDialog(
        "Test Dialog / Тестовый диалог",
        ["fio", "phone", "email", "comment"]
    )
    
    # Show dialog and handle result / Показать диалог и обработать результат
    if test_dialog.exec():
        print("Dialog accepted with data:")
        print(f"FIO: {test_dialog.fio}")
        print(f"Phone: {test_dialog.phone}")
        print(f"Email: {test_dialog.email}")
        print(f"Comment: {test_dialog.comment}")
    else:
        print("Dialog was cancelled")
    
    print("=== Test completed / Тест завершён ===")