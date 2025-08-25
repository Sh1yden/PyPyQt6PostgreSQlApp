# ===== BASE VIEW CLASS FOR DATA DISPLAY / БАЗОВЫЙ КЛАСС ПРЕДСТАВЛЕНИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ =====
# Universal table view class for displaying database data
# Универсальный класс представления таблицы для отображения данных базы данных

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QTableView, QMessageBox, QHeaderView
from src.core.Logger import Logger


# ===== BASE VIEW CLASS / БАЗОВЫЙ КЛАСС ПРЕДСТАВЛЕНИЯ =====
class BaseView(QTableView):
    """
    Base view class for displaying data / Базовый класс представления для отображения данных
    Handles user interface and interactions / Обрабатывает пользовательский интерфейс и взаимодействия

    This class provides a unified table view interface for all database entities.
    It handles data display, user interactions, keyboard shortcuts, and CRUD operations.
    Extends QTableView with enhanced functionality for database management.

    Этот класс предоставляет унифицированный интерфейс представления таблицы для всех сущностей базы данных.
    Он обрабатывает отображение данных, взаимодействия с пользователем, горячие клавиши и операции CRUD.
    Расширяет QTableView с улучшенной функциональностью для управления базой данных.
    """

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(
        self,
        model_class: type,
        index_last_stretch_colum: int | None = None,
        parent=None,
    ):
        """
        Initialize base view with model configuration / Инициализация базового представления с конфигурацией модели

        Sets up the table view with the specified model class and configures display properties.
        Establishes keyboard shortcuts and connects signals for data updates.

        Настраивает представление таблицы с указанным классом модели и конфигурирует свойства отображения.
        Устанавливает горячие клавиши и подключает сигналы для обновления данных.

        Args:
            model_class: Model class for this view / Класс модели для данного представления
            index_last_stretch_colum: Index of column to stretch to fill remaining space / Индекс колонки для растягивания на оставшееся пространство
            parent: Parent object / Родительский объект
        """
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched.")
        self.lg.debug("Logger created.")

        # ===== CONFIGURATION STORAGE / СОХРАНЕНИЕ КОНФИГУРАЦИИ =====
        self.model_class = model_class
        self.index_stretch = index_last_stretch_colum

        # ===== MODEL SETUP / НАСТРОЙКА МОДЕЛИ =====
        # Create and configure model instance / Создание и настройка экземпляра модели
        self._model = model_class(parent=self)
        self.setModel(self._model)

        # ===== UI CONFIGURATION / НАСТРОЙКА ПОЛЬЗОВАТЕЛЬСКОГО ИНТЕРФЕЙСА =====
        self.setup_table_view()
        self.setup_shortcuts()

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        self._model.data_changed.connect(self.on_data_changed)

        self.lg.debug("Setup shortcuts and view completed successfully.")

    # ===== PRIVATE METHODS - UI SETUP / ПРИВАТНЫЕ МЕТОДЫ - НАСТРОЙКА UI =====

    def setup_table_view(self) -> None:
        """
        Table appearance configuration / Настройка внешнего вида таблицы

        Configures table display properties including column sizing, selection behavior,
        editing triggers, sorting, and visual enhancements for better user experience.

        Настраивает свойства отображения таблицы, включая размеры колонок, поведение выбора,
        триггеры редактирования, сортировку и визуальные улучшения для лучшего пользовательского опыта.
        """
        try:
            # ===== COLUMN SIZING / РАЗМЕРЫ КОЛОНОК =====
            # Resize columns to content by default / Изменение размера колонок под содержимое по умолчанию
            self.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents
            )

            # Stretch specified column to fill remaining space / Растягивание указанной колонки для заполнения оставшегося пространства
            if self.index_stretch is not None:
                self.horizontalHeader().setSectionResizeMode(
                    self.index_stretch, QHeaderView.ResizeMode.Stretch
                )

            # ===== SELECTION AND EDITING BEHAVIOR / ПОВЕДЕНИЕ ВЫБОРА И РЕДАКТИРОВАНИЯ =====
            # Allow row selection mode / Разрешить режим выбора строк
            self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            # Enable editing on double-click / Включить редактирование по двойному клику
            self.setEditTriggers(QTableView.EditTrigger.DoubleClicked)

            # ===== SORTING AND DISPLAY / СОРТИРОВКА И ОТОБРАЖЕНИЕ =====
            # Enable column sorting / Включить сортировку колонок
            self.setSortingEnabled(True)
            self.sortByColumn(1, Qt.SortOrder.DescendingOrder)
            # Hide ID column (first column) from user view / Скрыть ID колонку (первая колонка) от пользователя
            self.hideColumn(0)

            # ===== VISUAL ENHANCEMENTS / ВИЗУАЛЬНЫЕ УЛУЧШЕНИЯ =====
            # Enable alternating row colors for better readability / Включить чередующиеся цвета строк для лучшей читаемости
            self.setAlternatingRowColors(True)
            # Disable word wrap for consistent display / Отключить перенос слов для согласованного отображения
            self.setWordWrap(False)

            self.lg.debug("Table setup successfully.")
        except Exception as e:
            self.lg.critical(f"Internal error: {e}.")

    def setup_shortcuts(self) -> None:
        """
        Keyboard shortcuts configuration / Настройка горячих клавиш

        Establishes keyboard shortcuts for common operations:
        - Delete: Remove single selected record
        - Ctrl+Delete: Remove multiple selected records
        - Ctrl+A: Select all records

        Устанавливает горячие клавиши для общих операций:
        - Delete: Удаление одной выбранной записи
        - Ctrl+Delete: Удаление нескольких выбранных записей
        - Ctrl+A: Выбор всех записей
        """
        try:
            # ===== SINGLE RECORD DELETION / УДАЛЕНИЕ ОДНОЙ ЗАПИСИ =====
            # Delete key for single record deletion / Клавиша Delete для удаления одной записи
            delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
            delete_shortcut.activated.connect(self.delete)

            # ===== MULTIPLE RECORD DELETION / УДАЛЕНИЕ МНОЖЕСТВЕННЫХ ЗАПИСЕЙ =====
            # Ctrl+Delete for multiple record deletion / Ctrl+Delete для удаления множественных записей
            delete_multiple_shortcut = QShortcut(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Delete), self
            )
            delete_multiple_shortcut.activated.connect(self.delete_selected)

            # ===== SELECT ALL RECORDS / ВЫБОР ВСЕХ ЗАПИСЕЙ =====
            # Ctrl+A for selecting all rows / Ctrl+A для выбора всех строк
            select_all_shortcut = QShortcut(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_A), self
            )
            select_all_shortcut.activated.connect(self.selectAll)

            self.lg.debug("Shortcuts setup successfully.")
        except Exception as e:
            self.lg.error(f"Internal error: {e}.")

    # ===== PUBLIC METHODS - CRUD OPERATIONS / ПУБЛИЧНЫЕ МЕТОДЫ - ОПЕРАЦИИ CRUD =====

    def add(self) -> None:
        """
        Add new record operation / Операция добавления новой записи

        This method should be overridden in child classes to provide entity-specific
        dialog creation and data input functionality.

        Этот метод должен быть переопределен в дочерних классах для предоставления
        специфичной для сущности функциональности создания диалогов и ввода данных.
        """
        QMessageBox.information(
            self, "Information", "The add() method must be redefined in the inheritor"
        )
        self.lg.warning(
            "BaseView add() method called but not implemented in child class"
        )

    def uppdate(self) -> None:
        """
        Show information about direct table editing / Информация о редактировании напрямую в таблице

        Displays user instructions for editing records directly in the table view
        and available keyboard shortcuts for various operations.

        Отображает пользовательские инструкции для редактирования записей напрямую в представлении таблицы
        и доступные горячие клавиши для различных операций.
        """
        QMessageBox.information(
            self,
            "Edit",
            "For editing:\n"
            "• Double-click on the cell\n"
            "• Record ID cannot be edited\n\n"
            "Keyboard shortcuts:\n"
            "• F5 - update data\n"
            "• Delete - delete selected record\n"
            "• Ctrl+Delete - delete selected records\n"
            "• Ctrl+A - select all",
        )

    def delete(self) -> None:
        """
        Delete single selected record / Удаление выбранной записи

        Prompts user for confirmation before deleting the selected record.
        Shows detailed information about the record being deleted.
        Updates the view automatically after successful deletion.

        Запрашивает подтверждение пользователя перед удалением выбранной записи.
        Показывает подробную информацию о удаляемой записи.
        Автоматически обновляет представление после успешного удаления.
        """
        try:
            # ===== SELECTION VALIDATION / ПРОВЕРКА ВЫБОРА =====
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Delete", "Select an entry to delete")
                return

            # ===== RECORD DATA EXTRACTION / ИЗВЛЕЧЕНИЕ ДАННЫХ ЗАПИСИ =====
            selected_row = selection[0].row()

            # Get record ID from first column / Получаем ID записи (первая колонка)
            id_item = self.model().item(selected_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Error", "Record ID could not be retrieved")
                return

            record_id = id_item.text()

            # Get main field for confirmation dialog / Получаем основное поле для диалога подтверждения
            main_field_item = self.model().item(
                selected_row, 1
            )  # Second column / Вторая колонка
            main_field_value = main_field_item.text() if main_field_item else "Unknown"

            # ===== CONFIRMATION DIALOG / ДИАЛОГ ПОДТВЕРЖДЕНИЯ =====
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete the entry?:\n\n"
                f"ID: {record_id}\n"
                f"Name: {main_field_value}\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            # ===== DELETION EXECUTION / ВЫПОЛНЕНИЕ УДАЛЕНИЯ =====
            if reply == QMessageBox.StandardButton.Yes:
                if self.model().delete_record(record_id):
                    QMessageBox.information(
                        self,
                        "Deletion",
                        f"Record '{main_field_value}' successfully deleted",
                    )
                    self.lg.debug(f"BaseView Successfully deleted record {record_id}")
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "The record could not be deleted.\n"
                        "Check the log for details.",
                    )
        except Exception as e:
            self.lg.error(f"BaseView internal error: {e}. In DEF delete().")

    def delete_selected(self) -> None:
        """
        Delete all selected records / Удаление всех выбранных записей

        Allows bulk deletion of multiple selected records with confirmation.
        Provides detailed feedback on the number of successfully and unsuccessfully deleted records.
        Processes deletions in reverse order to maintain index consistency.

        Позволяет массовое удаление нескольких выбранных записей с подтверждением.
        Предоставляет подробную обратную связь о количестве успешно и неуспешно удаленных записей.
        Обрабатывает удаления в обратном порядке для поддержания согласованности индексов.
        """
        try:
            # ===== SELECTION VALIDATION / ПРОВЕРКА ВЫБОРА =====
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Delete", "Select entries to delete")
                return

            # ===== CONFIRMATION DIALOG / ДИАЛОГ ПОДТВЕРЖДЕНИЯ =====
            count = len(selection)
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete {count} records?\n\n"
                f"This action cannot be canceled!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            # ===== BULK DELETION EXECUTION / ВЫПОЛНЕНИЕ МАССОВОГО УДАЛЕНИЯ =====
            if reply == QMessageBox.StandardButton.Yes:
                deleted_count = 0
                failed_count = 0

                # Sort indices in descending order to prevent index shifting during deletion
                # Сортируем индексы по убыванию, чтобы удаление не сбивало нумерацию
                sorted_selection = sorted(
                    selection, key=lambda x: x.row(), reverse=True
                )

                for index in sorted_selection:
                    row = index.row()
                    id_item = self.model().item(row, 0)

                    if id_item:
                        record_id = id_item.text()
                        if self.model().delete_record(record_id):
                            deleted_count += 1
                        else:
                            failed_count += 1

                # ===== RESULTS REPORTING / ОТЧЕТ О РЕЗУЛЬТАТАХ =====
                message = f"Deleted entries: {deleted_count}"
                if failed_count > 0:
                    message += f"\nFailed to delete: {failed_count}"
                    QMessageBox.warning(self, "Deletion result", message)
                else:
                    QMessageBox.information(self, "Deletion result", message)

                self.lg.debug(
                    f"BaseView: Multiple delete - success: {deleted_count}, failed: {failed_count}"
                )
        except Exception as e:
            self.lg.error(f"BaseView delete_selected error: {e}")

    def on_data_changed(self):
        """Обрабатывает изменения данных в таблице и применяет новые настройки при изменении"""
        self.resizeColumnsToContents()
        self.setup_table_view()


# ===== MAIN EXECUTION BLOCK - FOR TESTING / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ДЛЯ ТЕСТИРОВАНИЯ =====
if __name__ == "__main__":
    # This block can be used for testing BaseView functionality independently
    # Этот блок может использоваться для независимого тестирования функциональности BaseView
    print("=== BaseView Testing Mode / Режим тестирования BaseView ===")
    print(
        "BaseView is a base class and should be inherited by specific view implementations."
    )
    print(
        "BaseView является базовым классом и должен наследоваться конкретными реализациями представлений."
    )
