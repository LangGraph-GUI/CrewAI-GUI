# Node.py

from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush
from Edge import Edge
from NodeData import NodeData
from NodeLayout import NodeLayout

class Node(QGraphicsItem):
    def __init__(self, node_data: NodeData):
        super().__init__()
        self.data = node_data
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.rect = QRectF(0, 0, self.data.width, self.data.height)
        self.resizeHandleSize = 10
        self.resizing = False
        self.resizeDirection = None
        self.content = NodeLayout(self)
        self.input_port = Port(self, QPointF(0, 25), "input")
        self.output_port = Port(self, QPointF(self.rect.width(), 25), "output")
        self.setPos(self.data.pos_x, self.data.pos_y)  # Set initial position from NodeData
        self.setAcceptHoverEvents(True)
        self.hovered = False  # Track hover state

    def setWidth(self, width):
        self.rect.setWidth(width)
        self.output_port.setPos(width, 25)
        self.prepareGeometryChange()
        self.content.update_proxy_widget_geometry()  # Ensure the content size is updated
        self.data.width = width

    def setHeight(self, height):
        self.rect.setHeight(height)
        self.prepareGeometryChange()
        self.content.update_proxy_widget_geometry()  # Ensure the content size is updated
        self.data.height = height

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 2)
        if self.hovered:
            pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.drawRect(self.rect)
        self.content.paint(painter, option, widget)  # Delegate the painting to NodeLayout

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for port in [self.input_port, self.output_port]:
                for edge in port.edges:
                    edge.update_position()
            # Sync position with NodeData
            self.data.pos_x = value.x()
            self.data.pos_y = value.y()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        pos = event.pos()
        if pos.x() >= self.rect.right() - self.resizeHandleSize and \
                pos.y() >= self.rect.bottom() - self.resizeHandleSize:
            self.resizing = True
            self.resizeDirection = "bottom_right"
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.resizing = False
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.pos() - event.lastPos()
            if self.resizeDirection == "bottom_right":
                self.setWidth(self.rect.width() + delta.x())
                self.setHeight(self.rect.height() + delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def remove_node(self):
        # Remove all edges connected to this node
        for edge in self.input_port.edges[:]:
            edge.remove()
        for edge in self.output_port.edges[:]:
            edge.remove()

        # Update prevs and nexts of connected nodes
        for prev_id in self.data.prevs:
            prev_node = self.scene().get_node_by_id(prev_id)
            if prev_node:
                prev_node.data.nexts.remove(self.data.uniq_id)

        for next_id in self.data.nexts:
            next_node = self.scene().get_node_by_id(next_id)
            if next_node:
                next_node.data.prevs.remove(self.data.uniq_id)

        # Finally, remove this node from the scene
        self.scene().removeItem(self)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()  # Trigger a repaint
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()  # Trigger a repaint
        super().hoverLeaveEvent(event)

class Port(QGraphicsEllipseItem):
    def __init__(self, parent, position, port_type):
        super().__init__(-5, -5, 10, 10, parent)
        self.setBrush(Qt.black)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setPos(position)
        self.port_type = port_type
        self.edges = []

    def mousePressEvent(self, event):
        if self.port_type == "output":
            edge = Edge(self)
            self.edges.append(edge)
            self.scene().addItem(edge)

    def mouseMoveEvent(self, event):
        if self.edges:
            self.edges[-1].update_position(event.scenePos())

    def mouseReleaseEvent(self, event):
        if self.edges:
            items = self.scene().items(event.scenePos())
            for item in items:
                if isinstance(item, Port) and item != self:
                    if self.port_type == "output" and item.port_type == "input":
                        self.edges[-1].set_destination(item)
                        item.edges.append(self.edges[-1])
                        break
            else:
                self.scene().removeItem(self.edges[-1])
                self.edges.pop()
