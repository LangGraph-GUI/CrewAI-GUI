# CustomGraphicsView.py

from PySide6.QtWidgets import QGraphicsView, QMenu, QGraphicsProxyWidget
from PySide6.QtGui import QAction, QPixmap, QPainter
from PySide6.QtCore import Qt, QPointF, QElapsedTimer
from NodeData import NodeData
from Node import Node
from Edge import Edge
from NodeLayout import NodeLayout  # Make sure to import NodeLayout

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, main_window):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self._dragging = False
        self._last_mouse_pos = QPointF()
        self.main_window = main_window  # Reference to the MainWindow
        self.timer = QElapsedTimer()  # Initialize the timer
        self.right_clicked_item = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._last_mouse_pos = event.pos()
            self.timer.start()  # Start the timer

            # Check if the right-click is on an Edge or a Node
            item = self.itemAt(event.pos())
            while item and not isinstance(item, (Node, Edge)) and isinstance(item, (QGraphicsProxyWidget, NodeLayout)):
                item = item.parentItem()

            if isinstance(item, Edge):
                self.right_clicked_item = item
            elif isinstance(item, Node):
                self.right_clicked_item = item
            else:
                self.right_clicked_item = None

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton:
            delta = event.pos() - self._last_mouse_pos
            self._last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._dragging = True
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            elapsed_time = self.timer.elapsed()  # Get the elapsed time
            if elapsed_time < 170:  # If the right-click was shorter than 170 ms
                self.show_context_menu(event.pos())
            self._dragging = False
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

    def remove_node(self):
        if self.right_clicked_item and isinstance(self.right_clicked_item, Node):
            self.right_clicked_item.remove_node()
            self.right_clicked_item = None

    def remove_edge(self):
        if self.right_clicked_item and isinstance(self.right_clicked_item, Edge):
            self.right_clicked_item.remove()
            self.right_clicked_item = None

    def update_map_view(self):
        rect = self.scene().sceneRect()
        pixmap = QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()
        self.main_window.map_view.update_map(pixmap)  # Update the map view in the MainWindow

    def show_context_menu(self, position):
        self.right_click_position = self.mapToScene(position)
        context_menu = QMenu(self)

        if isinstance(self.right_clicked_item, Edge):
            remove_edge_action = QAction("Remove Edge", self)
            remove_edge_action.triggered.connect(self.remove_edge)
            context_menu.addAction(remove_edge_action)
        elif isinstance(self.right_clicked_item, Node):
            remove_node_action = QAction("Remove Node", self)
            remove_node_action.triggered.connect(self.remove_node)
            context_menu.addAction(remove_node_action)
        else:
            add_node_action = QAction("Add Node", self)
            add_node_action.triggered.connect(lambda: self.add_node(self.right_click_position))
            context_menu.addAction(add_node_action)

        context_menu.exec(self.mapToGlobal(position))
