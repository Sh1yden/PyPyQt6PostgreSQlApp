from PyQt6.QtWidgets import QApplication
from src.core.Logger import Logger


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Application.")
        self.lg.debug("Logger created in class Application().")
