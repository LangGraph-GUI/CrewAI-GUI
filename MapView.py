# MapView.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QTransform

class MapView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map View")
        self.layout = QVBoxLayout(self)
        
        self.map_label = QLabel(self)
        self.map_label.setFixedSize(200, 200)  # Set fixed size for the map view
        self.layout.addWidget(self.map_label)
        self.setLayout(self.layout)

    def update_map(self, pixmap):
        scaled_pixmap = pixmap.scaled(self.map_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.map_label.setPixmap(scaled_pixmap)
