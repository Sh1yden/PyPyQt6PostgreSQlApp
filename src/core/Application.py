# ===== MAIN APPLICATION CLASS / ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ =====

# ===== IMPORTS / ИМПОРТЫ =====
# PyQt6 core imports for application framework /
# Импорты PyQt6 для фреймворка приложения
from PyQt6.QtWidgets import QApplication

# Local logging system import / Импорт локальной системы логирования
from src.core.Logger import Logger


# ===== APPLICATION CLASS / КЛАСС ПРИЛОЖЕНИЯ =====
class Application(QApplication):
    """
    Main application class extending QApplication / Главный класс приложения, расширяющий QApplication
    Handles application-wide functionality and logging / Обрабатывает общую функциональность приложения и логирование

    This class serves as the foundation for the entire application, providing:
    - Centralized logging initialization / Централизованная инициализация логирования
    - Application-wide resource management / Управление ресурсами в масштабе приложения
    - Event loop management / Управление циклом событий
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, argv):
        """
        Initialize application with logging support / Инициализация приложения с поддержкой логирования

        Args:
            argv: Command line arguments passed to the application /
                  Аргументы командной строки, переданные в приложение
        """
        # Initialize parent QApplication class / Инициализация родительского класса QApplication
        super().__init__(argv)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГГЕРА =====
        # Create logger instance for application-wide logging /
        # Создание экземпляра логгера для логирования всего приложения
        self.lg = Logger()

        # Log application startup events for debugging /
        # Логирование событий запуска приложения для отладки
        self.lg.debug("Constructor launched in class Application.")
        self.lg.debug("Logger created in class Application().")