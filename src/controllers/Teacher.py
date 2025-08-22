# ===== TEACHER CONTROLLER MODULE / МОДУЛЬ КОНТРОЛЛЕРА УЧИТЕЛЯ =====
# Teacher entity MVC implementation / Реализация MVC для сущности Учитель

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
    Teacher model class for data management / Класс модели учителя для управления данными

    Handles database operations and data validation for teachers:
    Обрабатывает операции с БД и валидацию данных для учителей:
    - CRUD operations with teacher table / CRUD операции с таблицей учителей
    - Data validation and business logic / Валидация данных и бизнес-логика
    - Database connection management / Управление соединениями с базой данных
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize teacher model with database configuration / Инициализация модели учителя с конфигурацией БД

        Args:
            parent: Parent object for Qt hierarchy / Родительский объект для иерархии Qt
        """
        # Initialize base model with teacher-specific configuration /
        # Инициализация базовой модели с конфигурацией, специфичной для учителя
        super().__init__(
            table_name="Teacher",
            columns=['f_fio', 'f_phone', 'f_email', 'f_comment'],
            parent=parent
        )


# ===== VIEW CLASS / КЛАСС ПРЕДСТАВЛЕНИЯ =====
class View(BaseView):
    """
    Teacher view class for user interface / Класс представления учителя для пользовательского интерфейса

    Handles user interface and interactions for teacher management:
    Обрабатывает пользовательский интерфейс и взаимодействия для управления учителями:
    - Table display and formatting / Отображение и форматирование таблицы
    - User interaction handling / Обработка пользовательских взаимодействий
    - CRUD operation coordination / Координация CRUD операций
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize teacher view with model configuration / Инициализация представления учителя с конфигурацией модели

        Args:
            parent: Parent widget for Qt hierarchy / Родительский виджет для иерархии Qt
        """
        # Initialize base view with teacher model and comment column stretch /
        # Инициализация базового представления с моделью учителя и растяжением колонки комментариев
        super().__init__(
            model_class=Model,
            index_last_stretch_colum=4,  # Comment column index for stretching / Индекс колонки комментариев для растяжения
            parent=parent
        )

    # ===== CRUD OPERATIONS / ОПЕРАЦИИ CRUD =====
    def add(self) -> None:
        """
        Add new teacher record through dialog / Добавление новой записи учителя через диалог

        Opens teacher input dialog and processes the data if confirmed.
        Открывает диалог ввода учителя и обрабатывает данные при подтверждении.
        """
        # Create and show teacher input dialog / Создание и отображение диалога ввода учителя
        dialog = Dialog(parent=self)

        # Process dialog result if user confirms / Обработка результата диалога при подтверждении пользователя
        if dialog.exec():
            # Add new teacher with dialog data / Добавление нового учителя с данными из диалога
            self.model().add(
                dialog.get_value("fio"),      # Full name / Полное имя
                dialog.get_value("phone"),    # Phone number / Номер телефона
                dialog.get_value("email"),    # Email address / Email адрес
                dialog.get_value("comment")   # Additional comments / Дополнительные комментарии
            )


# ===== DIALOG CLASS / КЛАСС ДИАЛОГА =====
class Dialog(BaseDialog):
    """
    Teacher input dialog class / Класс диалога ввода учителя

    Provides input form for teacher data entry:
    Предоставляет форму ввода для ввода данных учителя:
    - Form validation and data collection / Валидация формы и сбор данных
    - User-friendly input interface / Дружественный интерфейс ввода
    - Data preparation for model operations / Подготовка данных для операций модели
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize teacher input dialog / Инициализация диалога ввода учителя

        Args:
            parent: Parent widget for modal dialog / Родительский виджет для модального диалога
        """
        # Initialize base dialog with teacher-specific fields /
        # Инициализация базового диалога с полями, специфичными для учителя
        super().__init__(
            window_title="Teacher",
            fields=["fio", "phone", "email", "comment"],  # Required input fields / Обязательные поля ввода
            parent=parent
        )