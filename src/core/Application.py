from PyQt6.QtWidgets import QApplication
from src.database.Connection import Connection


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        Connection()
