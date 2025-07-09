from PyQt6.QtSql import QSqlQueryModel


class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
