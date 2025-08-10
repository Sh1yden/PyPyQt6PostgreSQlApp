# ===== MAIN APPLICATION ENTRY POINT / ГЛАВНАЯ ТОЧКА ВХОДА В ПРИЛОЖЕНИЕ =====

# ===== IMPORTS / ИМПОРТЫ =====
import sys
from src.core.Application import Application
from src.ui.MainWindow import MainWindow


# ===== APPLICATION STARTUP / ЗАПУСК ПРИЛОЖЕНИЯ =====
if __name__ == "__main__":
    # Create application instance / Создание экземпляра приложения
    app = Application(sys.argv)

    # Create and show main window / Создание и отображение главного окна
    main_window = MainWindow()
    main_window.showMaximized()

    # Run application event loop and exit with result / Запуск цикла событий приложения и выход с результатом
    result = app.exec()
    sys.exit(result)