# MainWindow.py

from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QMenu, QFileDialog, QDockWidget
from PySide6.QtGui import QAction, QPixmap, QPainter
from PySide6.QtCore import Qt, QTimer, QPointF
from Node import Node
from NodeData import NodeData
from MapView import MapView
import file_operations
from CustomGraphicsView import CustomGraphicsView
from ExecCommandDialog import ExecCommandDialog  # Import the new dialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = CustomGraphicsScene()
        self.view = CustomGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.right_click_position = QPointF()  # Store the right-click position
        self.create_dock_widgets()
        self.create_actions_and_menus()

    def create_actions_and_menus(self):
        actions = {
            "File": {
                "New": self.new,
                "Save": self.save,
                "Load": self.load,
            },
            "Tools": {
                "Map View": self.toggle_map_view,
                "Exec Command": self.exec_command,
            }
        }

        self.menu_bar = self.menuBar()
        self.actions = {}

        for menu_name, actions_dict in actions.items():
            menu = self.menu_bar.addMenu(menu_name)
            for action_name, method in actions_dict.items():
                action = QAction(action_name, self)
                action.triggered.connect(method)
                self.actions[action_name.lower().replace(" ", "_") + "_action"] = action
                menu.addAction(action)

    def create_dock_widgets(self):
        self.map_view = MapView()
        self.dock_widget = QDockWidget("Map View", self)
        self.dock_widget.setWidget(self.map_view)
        self.dock_widget.setFloating(True)
        
        # Move the dock widget to the bottom-left corner of the screen
        screen_geometry = self.screen().geometry()
        screen_height = screen_geometry.height()
        self.dock_widget.move(0, screen_height - 200)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)

    def contextMenuEvent(self, event):
        self.right_click_position = self.view.mapToScene(event.pos())
        context_menu = QMenu(self)
        add_node_action = QAction("Add Node", self)
        add_node_action.triggered.connect(self.add_node)
        context_menu.addAction(add_node_action)
        context_menu.exec(event.globalPos())

    def add_node(self):
        unique_id = f"uniq_id_{self.scene.node_counter}"
        node_data = NodeData(name="Node", uniq_id=unique_id)
        node = Node(node_data)
        self.scene.addItem(node)
        node.setPos(self.right_click_position)  # Set the node position to the right-click position
        self.scene.node_counter += 1  # Increment the counter
        self.update_map_view()

    def new(self):
        self.scene.clear()  # Clears all items from the scene
        self.scene.node_counter = 1  # Reset the node counter
        self.update_map_view()  # Refresh the view

    def save(self):
        file_operations.save(self.scene)

    def load(self):
        self.new()
        file_operations.load(self.scene)
        self.update_map_view()  # Refresh the view after loading

    def exec_command(self):
        self.exec_command_dialog = ExecCommandDialog(self)
        self.exec_command_dialog.show()

    def toggle_map_view(self):
        is_visible = self.dock_widget.isVisible()
        self.dock_widget.setVisible(not is_visible)

    def update_map_view(self):
        rect = self.scene.sceneRect()
        pixmap = QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene.render(painter)
        painter.end()
        self.map_view.update_map(pixmap)

class CustomGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.node_counter = 1  # Initialize the counter
