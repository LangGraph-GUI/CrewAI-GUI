# CustomGraphicsView.py

from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap, QPainter
from Node import Node
from NodeData import NodeData

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, main_window):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self._dragging = False
        self._last_mouse_pos = QPointF()
        self.main_window = main_window  # Reference to the MainWindow

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._dragging = True
            self._last_mouse_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.pos() - self._last_mouse_pos
            self._last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self._dragging:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def add_node(self, position):
        unique_id = f"uniq_id_{self.scene().node_counter}"
        node_data = NodeData(name="Node", uniq_id=unique_id)
        node = Node(node_data)
        self.scene().addItem(node)
        node.setPos(position)  # Set the node position to the right-click position
        self.scene().node_counter += 1  # Increment the counter
        self.update_map_view()

    def update_map_view(self):
        rect = self.scene().sceneRect()
        pixmap = QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()
        self.main_window.map_view.update_map(pixmap)  # Update the map view in the MainWindow
