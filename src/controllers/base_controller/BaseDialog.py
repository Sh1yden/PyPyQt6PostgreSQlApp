# ===== BASE DIALOG CLASS FOR DATA INPUT / БАЗОВЫЙ КЛАСС ДИАЛОГА ДЛЯ ВВОДА ДАННЫХ =====
# Universal dialog class for creating and editing database records
# Универсальный класс диалога для создания и редактирования записей базы данных

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QMessageBox,
)
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

        self._FIELD_MAP = {
            "fio": {"label": "Surname N. P.", "widget": QLineEdit},
            "title": {"label": "Title Group", "widget": QLineEdit},
            "phone": {"label": "Phone number", "widget": QLineEdit},
            "email": {"label": "Email", "widget": QLineEdit},
            "comment": {"label": "Comment", "widget": QTextEdit},
            "username": {"label": "Username", "widget": QLineEdit},
            "password": {"label": "Password", "widget": QLineEdit},
        }
        self._fields = {}

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched.")
        self.lg.debug("Logger created.")

        # ===== DIALOG SETUP / НАСТРОЙКА ДИАЛОГА =====
        self.set_window_dialog(window_title, fields)

    # ===== PRIVATE METHODS - UI SETUP / ПРИВАТНЫЕ МЕТОДЫ - НАСТРОЙКА UI =====

    def set_window_dialog(self, window_title: str, privilege: list) -> None:
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

        for field in privilege:
            cfg = self._FIELD_MAP.get(field)
            if not cfg:
                continue

            lbl = QLabel(cfg["label"], parent=self)
            widget = cfg["widget"](parent=self)

            if field == "password" and isinstance(widget, QLineEdit):
                widget.setEchoMode(QLineEdit.EchoMode.Password)

            lay.addWidget(lbl)
            lay.addWidget(widget)
            self._fields[field] = widget

        # ===== BUTTON SETUP / НАСТРОЙКА КНОПОК =====
        ok_btn = QPushButton("OK", parent=self)  # Confirm button / Кнопка подтверждения
        cancel_btn = QPushButton("Cancel", parent=self)  # Cancel button / Кнопка отмены

        # ===== BUTTON LAYOUT / МАКЕТ КНОПОК =====
        lay_for_btn = (
            QHBoxLayout()
        )  # Horizontal layout for buttons / Горизонтальный макет для кнопок
        lay_for_btn.addWidget(ok_btn)
        lay_for_btn.addWidget(cancel_btn)
        lay.addLayout(lay_for_btn)

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        ok_btn.clicked.connect(
            self.finish
        )  # Connect OK button to finish method / Подключить кнопку OK к методу finish
        cancel_btn.clicked.connect(
            self.reject
        )  # Connect Cancel button to reject method / Подключить кнопку Cancel к методу reject

    def get_value(self, field: str) -> str | None:
        """
        Get input value for the given field.
        Получить введённое значение для указанного поля.

        Args:
            field (str): Field name / Имя поля

        Returns:
            str | None: Cleaned input value or None if empty
                        Очищенное введённое значение или None, если пустое
        """
        widget = self._fields.get(field)
        if widget is None:
            return None

        if isinstance(widget, QLineEdit):
            value = widget.text().strip()
        elif isinstance(widget, QTextEdit):
            value = widget.toPlainText().strip()
        else:
            return None

        return value or None

    # ===== SLOT METHODS - EVENT HANDLERS / МЕТОДЫ-СЛОТЫ - ОБРАБОТЧИКИ СОБЫТИЙ =====

    @pyqtSlot()
    def finish(self) -> None:
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
        if self.get_value("fio") is None:
            self.lg.debug("No FIO input provided.")
            QMessageBox.information(
                self,
                "Please input Surname N.P!!!",
                "Please input Surname N.P!!! This is necessary.",
            )
            return

        # ===== DIALOG ACCEPTANCE / ПРИНЯТИЕ ДИАЛОГА =====
        self.accept()  # Close dialog with acceptance / Закрыть диалог с принятием
        self.lg.debug("Dialog accepted successfully.")


# ===== MAIN EXECUTION BLOCK - FOR TESTING / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ДЛЯ ТЕСТИРОВАНИЯ =====
if __name__ == "__main__":
    # This block can be used for testing BaseDialog functionality independently
    # Этот блок может использоваться для независимого тестирования функциональности BaseDialog
    from PyQt6.QtWidgets import QApplication
    import sys

    print("=== BaseDialog Testing Mode / Режим тестирования BaseDialog ===")

    # Create test application / Создание тестового приложения
    app = QApplication(sys.argv)

    # Create test dialog with all field types / Создание тестового диалога со всеми типами полей
    test_dialog = BaseDialog(
        "Test Dialog / Тестовый диалог", ["fio", "phone", "email", "comment"]
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
