# Edge.py

from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QPainterPath

class Edge(QGraphicsPathItem):
    def __init__(self, source_port):
        super().__init__()
        self.source_port = source_port
        self.source_id = source_port.parentItem().data.uniq_id
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(-1)
        self.destination_port = None
        self.destination_id = None
        self.update_position()
        self.setAcceptHoverEvents(True)

    def update_position(self, end_point=None):
        path = QPainterPath()
        start_point = self.source_port.scenePos()
        if end_point:
            control_point_1 = QPointF(start_point.x() + 50, start_point.y())
            control_point_2 = QPointF(end_point.x() - 50, end_point.y())
            path.moveTo(start_point)
            path.cubicTo(control_point_1, control_point_2, end_point)
        elif self.destination_port:
            end_point = self.destination_port.scenePos()
            control_point_1 = QPointF(start_point.x() + 50, start_point.y())
            control_point_2 = QPointF(end_point.x() - 50, end_point.y())
            path.moveTo(start_point)
            path.cubicTo(control_point_1, control_point_2, end_point)
        else:
            path.moveTo(start_point)
            path.cubicTo(start_point, start_point, start_point)
        self.setPath(path)

    def set_destination(self, destination_port):
        self.destination_port = destination_port
        self.destination_id = destination_port.parentItem().data.uniq_id
        self.update_position()
        source_node = self.source_port.parentItem().data
        dest_node = self.destination_port.parentItem().data
        source_node.nexts.append(self.destination_id)
        dest_node.prevs.append(self.source_id)  # Add to prevs

    def remove(self):
        if self in self.source_port.edges:
            self.source_port.edges.remove(self)
        if self in self.destination_port.edges:
            self.destination_port.edges.remove(self)
        if self.destination_id in self.source_port.parentItem().data.nexts:
            self.source_port.parentItem().data.nexts.remove(self.destination_id)
        if self.source_id in self.destination_port.parentItem().data.prevs:
            self.destination_port.parentItem().data.prevs.remove(self.source_id)  # Remove from prevs
        self.scene().removeItem(self)
        
    def hoverEnterEvent(self, event):
        self.setPen(QPen(Qt.red, 2))  # Change color on hover
        self.setCursor(Qt.PointingHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(Qt.black, 2))  # Revert color on hover exit
        self.unsetCursor()
        super().hoverLeaveEvent(event)
