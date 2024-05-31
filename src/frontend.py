# main.py

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer  # Import QTimer
from MainWindow import MainWindow

def initialize_main_window():
    window = MainWindow()
    window.setWindowTitle("Json Node Editor")
    window.setGeometry(100, 100, 800, 600)  # Set initial size to 800x600
    
    # Set up a timer to refresh the map view periodically
    window.timer = QTimer(window)
    window.timer.timeout.connect(window.view.update_map_view)
    window.timer.start(1000)  # Refresh every second

    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = initialize_main_window()
    window.show()
    sys.exit(app.exec())
