from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QTableView, QMessageBox, QHeaderView
from src.core.Logger import Logger


# ===== BASE VIEW CLASS / БАЗОВЫЙ КЛАСС ПРЕДСТАВЛЕНИЯ =====
class BaseView(QTableView):
    """
    View class for displaying data / Класс представления для отображения данных
    Handles user interface and interactions / Обрабатывает пользовательский интерфейс и взаимодействия
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, model_class, index_last_stretch_colum: int | None = None, parent=None):
        """
        Инициализация базового представления

        Args:
            model_class: Класс модели для данного представления
            parent: Родительский объект
        """
        super().__init__(parent)

        # Logger initialization / Инициализация логера
        self.lg = Logger()
        self.lg.debug("Constructor launched in class BaseView.")
        self.lg.debug("Logger created in class BaseView().")

        # Сохранение параметров
        self.model_class = model_class
        self.index_stretch = index_last_stretch_colum

        # Создание и настройка модели
        self._model = model_class(parent=self)
        self.setModel(self._model)

        # Table view setup / Настройка представления таблицы
        self.setup_table_view()
        # Настройка горячих клавиш
        self.setup_shortcuts()

        # Signal connections / Подключение сигналов
        self._model.data_changed.connect(self.on_data_changed)

        self.lg.debug("BaseView setup completed successfully.")

    def setup_table_view(self):
        """Table appearance configuration / Настройка внешнего вида таблицы"""
        try:
            # Растягиваем колонки по содержимому
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

            # Растягиваем указанную колонку до конца экрана
            if self.index_stretch is not None:
                self.horizontalHeader().setSectionResizeMode(
                    self.index_stretch,
                    QHeaderView.ResizeMode.Stretch
                )

            # Разрешаем выделение строк
            self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

            # Редактирование по двойному клику
            self.setEditTriggers(QTableView.EditTrigger.DoubleClicked)

            # Включаем сортировку
            self.setSortingEnabled(True)

            # Скрываем ID колонку (первая колонка)
            self.hideColumn(0)

            # Настройки для лучшего UX
            self.setAlternatingRowColors(True)  # Чередующиеся цвета строк
            self.setWordWrap(False)  # Отключаем перенос слов

            self.lg.debug("BaseView table setup successfully.")
        except Exception as e:
            self.lg.critical(f"BaseView internal error: {e}. In DEF setup_table_view().")

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        try:
            # Delete для удаления одной записи
            delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
            delete_shortcut.activated.connect(self.delete)

            # Ctrl+Delete для удаления множественного выбора
            delete_multiple_shortcut = QShortcut(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Delete), self
            )
            delete_multiple_shortcut.activated.connect(self.delete_selected)

            # Ctrl+A для выделения всех строк
            select_all_shortcut = QShortcut(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_A), self
            )
            select_all_shortcut.activated.connect(self.selectAll)

            self.lg.debug("BaseView shortcuts setup successfully.")
        except Exception as e:
            self.lg.error(f"BaseView internal error: {e}. In DEF setup_shortcuts().")

    # ===== SLOT METHODS / МЕТОДЫ-СЛОТЫ =====
    @pyqtSlot()
    def on_data_changed(self):
        """Обработка изменения данных в модели"""
        self.lg.debug("BaseView data changed in model, refreshing view.")
        self.resizeColumnsToContents()

    # ===== CRUD OPERATIONS / ОПЕРАЦИИ CRUD =====
    def add(self):
        """
        Добавление новой записи
        Должно быть переопределено в наследниках для создания специфичного диалога
        """
        QMessageBox.information(self, "Information",
                              "The add() method must be redefined in the inheritor")
        self.lg.warning("BaseView add() method called but not implemented in child class")

    def uppdate(self):
        """Информация о редактировании напрямую в таблице"""
        QMessageBox.information(self, "Edit",
                                "For editing:\n"
                                "• Double-click on the cell\n"
                                "• Record ID cannot be edited\n\n"
                                "Keyboard shortcuts:\n"
                                "• F5 - update data\n"
                                "• Delete - delete selected record\n"
                                "• Ctrl+Delete - delete selected records\n"
                                "• Ctrl+A - select all")

    def delete(self):
        """Удаление выбранной записи"""
        try:
            # Получаем выбранную строку
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Delete",
                                        "Select an entry to delete")
                return

            # Получаем индекс выбранной строки
            selected_row = selection[0].row()

            # Получаем ID записи (первая колонка)
            id_item = self.model().item(selected_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Error",
                                    "Record ID could not be retrieved")
                return

            record_id = id_item.text()

            # Получаем основную информацию для диалога подтверждения
            main_field_item = self.model().item(selected_row, 1)  # Вторая колонка
            main_field_value = main_field_item.text() if main_field_item else "Неизвестно"

            # Диалог подтверждения удаления
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete the entry?:\n\n"
                f"ID: {record_id}\n"
                f"Name: {main_field_value}\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Execute deletion / Выполняем удаление
                if self.model().delete_record(record_id):
                    QMessageBox.information(self, "Deletion",
                                          f"Record '{main_field_value}' successfully deleted")
                    self.lg.debug(f"BaseView Successfully deleted record {record_id}")
                else:
                    QMessageBox.critical(self, "Error",
                                       "The record could not be deleted.\n"
                                       "Check the log for details.")
        except Exception as e:
            self.lg.error(f"BaseView internal error: {e}. In DEF delete().")

    def delete_selected(self):
        """Удаление всех выбранных записей"""
        try:
            selection = self.selectionModel().selectedRows()

            if not selection:
                QMessageBox.information(self, "Delete",
                                        "Select entries to delete")
                return

            # Подтверждение удаления множественных записей
            count = len(selection)
            reply = QMessageBox.question(
                self,
                "Confirmation of deletion",
                f"Are you sure you want to delete {count} records?\n\n"
                f"This action cannot be canceled!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                deleted_count = 0
                failed_count = 0

                # Сортируем индексы по убыванию, чтобы удаление не сбивало нумерацию
                sorted_selection = sorted(selection, key=lambda x: x.row(), reverse=True)

                for index in sorted_selection:
                    row = index.row()
                    id_item = self.model().item(row, 0)

                    if id_item:
                        record_id = id_item.text()
                        if self.model().delete_record(record_id):
                            deleted_count += 1
                        else:
                            failed_count += 1

                # Отчет о результатах
                message = f"Deleted entries: {deleted_count}"
                if failed_count > 0:
                    message +=f"Failed to delete: {failed_count}"
                    QMessageBox.warning(self, "Deletion result", message)
                else:
                    QMessageBox.information(self, "Deletion result", message)

                self.lg.debug(f"BaseView: Multiple delete - success: {deleted_count}, failed: {failed_count}")
        except Exception as e:
            self.lg.error(f"BaseView delete_selected error: {e}")
