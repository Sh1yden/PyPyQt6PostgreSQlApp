# ===== STUDENT GROUP CONTROLLER MODULE / МОДУЛЬ КОНТРОЛЛЕРА ГРУППЫ СТУДЕНТОВ =====
# Student Group entity MVC implementation / Реализация MVC для сущности Группа студентов

# ===== IMPORTS / ИМПОРТЫ =====
# Base controller classes for MVC pattern / Базовые классы контроллеров для паттерна MVC
from src.controllers.base_controller.BaseModel import BaseModel
from src.controllers.base_controller.BaseView import BaseView
from src.controllers.base_controller.BaseDialog import BaseDialog

# Logging system / Система логирования
from src.core.Logger import Logger


# ===== MODEL CLASS / КЛАСС МОДЕЛИ =====
class Model(BaseModel):
    """
    Student Group model class for data management / Класс модели группы студентов для управления данными

    Handles database operations and data validation for student groups:
    Обрабатывает операции с БД и валидацию данных для групп студентов:
    - CRUD operations with student group table / CRUD операции с таблицей групп студентов
    - Data validation and business logic / Валидация данных и бизнес-логика
    - Database connection management / Управление соединениями с базой данных
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize student group model with database configuration / Инициализация модели группы студентов с конфигурацией БД

        Args:
            parent: Parent object for Qt hierarchy / Родительский объект для иерархии Qt
        """
        # Initialize base model with group-specific configuration /
        # Инициализация базовой модели с конфигурацией, специфичной для группы
        super().__init__(
            table_name="StGroup", columns=["f_title", "f_comment"], parent=parent
        )


# ===== VIEW CLASS / КЛАСС ПРЕДСТАВЛЕНИЯ =====
class View(BaseView):
    """
    Student Group view class for user interface / Класс представления группы студентов для пользовательского интерфейса

    Handles user interface and interactions for student group management:
    Обрабатывает пользовательский интерфейс и взаимодействия для управления группами студентов:
    - Table display and formatting / Отображение и форматирование таблицы
    - User interaction handling / Обработка пользовательских взаимодействий
    - CRUD operation coordination / Координация CRUD операций
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize student group view with model configuration / Инициализация представления группы студентов с конфигурацией модели

        Args:
            parent: Parent widget for Qt hierarchy / Родительский виджет для иерархии Qt
        """
        # Initialize base view with group model and comment column stretch /
        # Инициализация базового представления с моделью группы и растяжением колонки комментариев
        super().__init__(
            model_class=Model,
            index_last_stretch_colum=2,  # Comment column index for stretching / Индекс колонки комментариев для растяжения
            parent=parent,
        )

    # ===== CRUD OPERATIONS / ОПЕРАЦИИ CRUD =====
    def add(self) -> None:
        """
        Add new student group record through dialog / Добавление новой записи группы студентов через диалог

        Opens group input dialog and processes the data if confirmed.
        Открывает диалог ввода группы и обрабатывает данные при подтверждении.
        """
        # Create and show group input dialog / Создание и отображение диалога ввода группы
        dialog = Dialog(parent=self)

        # Process dialog result if user confirms / Обработка результата диалога при подтверждении пользователя
        if dialog.exec():
            # Add new group with dialog data / Добавление новой группы с данными из диалога
            self.model().add(
                dialog.get_value("fio"),  # Group title / Название группы
                dialog.get_value(
                    "comment"
                ),  # Additional comments / Дополнительные комментарии
            )


# ===== DIALOG CLASS / КЛАСС ДИАЛОГА =====
class Dialog(BaseDialog):
    """
    Student Group input dialog class / Класс диалога ввода группы студентов

    Provides input form for student group data entry:
    Предоставляет форму ввода для ввода данных группы студентов:
    - Form validation and data collection / Валидация формы и сбор данных
    - User-friendly input interface / Дружественный интерфейс ввода
    - Data preparation for model operations / Подготовка данных для операций модели
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize student group input dialog / Инициализация диалога ввода группы студентов

        Args:
            parent: Parent widget for modal dialog / Родительский виджет для модального диалога
        """
        # Initialize base dialog with group-specific fields /
        # Инициализация базового диалога с полями, специфичными для группы
        super().__init__(
            window_title="StGroup",
            fields=[
                "title",
                "comment",
            ],  # Required input fields / Обязательные поля ввода
            parent=parent,
        )
