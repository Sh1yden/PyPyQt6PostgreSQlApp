# TODO сделать отрисовку таблицы в главном окне.
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtCore import QAbstractTableModel


class TableView(QAbstractTableModel):
    """Отрисовка таблиц в приложении."""

    def __init__(self):
        super().__init__()
        self.data = []
        self._headers = []

    def load_data(self):
        pass
