# ===== MAIN APPLICATION CLASS / ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ =====

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtWidgets import QApplication
from src.core.Logger import Logger


# ===== APPLICATION CLASS / КЛАСС ПРИЛОЖЕНИЯ =====
class Application(QApplication):
    """
    Main application class extending QApplication / Главный класс приложения, расширяющий QApplication
    Handles application-wide functionality and logging / Обрабатывает общую функциональность приложения и логирование
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, argv):
        """
        Initialize application with logging / Инициализация приложения с логированием
        
        Args:
            argv: Command line arguments / Аргументы командной строки
        """
        super().__init__(argv)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Application.")
        self.lg.debug("Logger created in class Application().")