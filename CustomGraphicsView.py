from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self._space_pressed = False
        self._dragging = False
        self._last_mouse_pos = QPointF()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self._space_pressed = True
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            self._space_pressed = False
        else:
            super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        if self._space_pressed:
            self._dragging = True
            self._last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
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
        if self._dragging:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)
