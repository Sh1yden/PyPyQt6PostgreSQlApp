# Imports / Импорты
from src.controllers.base_controller.BaseModel import BaseModel
from src.controllers.base_controller.BaseView import BaseView
from src.controllers.base_controller.BaseDialog import BaseDialog
from src.core.Logger import Logger


# ===== MODEL CLASS / КЛАСС МОДЕЛИ =====
class Model(BaseModel):
    """
    Model class for data / Класс модели для данных
    Handles database operations and data validation / Обрабатывает операции с БД и валидацию данных
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        # Инициализация базовой модели
        super().__init__("Teacher",
                         ['f_fio', 'f_phone', 'f_email', 'f_comment'],
                         parent)


# ===== VIEW CLASS / КЛАСС ПРЕДСТАВЛЕНИЯ =====
class View(BaseView):
    """
    View class for displaying data / Класс представления для отображения данных
    Handles user interface and interactions / Обрабатывает пользовательский интерфейс и взаимодействия
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        super().__init__(Model,
                         4,
                         parent)

    def add(self):
        """Add new cell to model / Добавление новой ячейки в модель"""
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio,
                             dia.phone,
                             dia.email,
                             dia.comment)


# ===== DIALOG CLASS / КЛАСС ДИАЛОГА =====
class Dialog(BaseDialog):
    """
    Dialog class for adding new records / Класс диалога для добавления новых записей
    Provides input form for data / Предоставляет форму ввода для данных
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        super().__init__("Teacher",
                               ["fio", "phone", "email", "comment"],
                                       parent)