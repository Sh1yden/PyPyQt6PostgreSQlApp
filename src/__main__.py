# ===== MAIN APPLICATION ENTRY POINT / ГЛАВНАЯ ТОЧКА ВХОДА В ПРИЛОЖЕНИЕ =====

# ===== IMPORTS / ИМПОРТЫ =====
# Standard library imports / Импорты стандартной библиотеки
import sys

# Local application imports / Импорты локального приложения
from src.core.Application import Application
from src.ui.MainWindow import MainWindow


# ===== APPLICATION STARTUP / ЗАПУСК ПРИЛОЖЕНИЯ =====
if __name__ == "__main__":
    # Create application instance with command line arguments /
    # Создание экземпляра приложения с аргументами командной строки
    app = Application(sys.argv)

    # Create main window instance and configure display /
    # Создание экземпляра главного окна и настройка отображения
    main_window = MainWindow()
    # Show window in maximized state for better user experience /
    # Отображение окна в развернутом состоянии для лучшего пользовательского опыта
    main_window.showMaximized()

    # Start application event loop and capture exit code /
    # Запуск цикла событий приложения и захват кода выхода
    result = app.exec()

    # Exit application with proper cleanup and return code /
    # Выход из приложения с правильной очисткой и кодом возврата
    sys.exit(result)
