import sys
from src.core.Application import Application
from src.ui.MainWindow import MainWindow

app = Application(sys.argv)

main_window = MainWindow()
main_window.showMaximized()

result = app.exec()
sys.exit(result)
