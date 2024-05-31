# NodeLayout.py

from PySide6.QtWidgets import QGraphicsItem, QLineEdit, QGraphicsProxyWidget, QVBoxLayout, QWidget, QLabel, QComboBox, QTextEdit, QHBoxLayout
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QBrush, QPen

class Slot:
    def __init__(self, data_attr, parent, layout, widget_class=QTextEdit):
        self.data_attr = data_attr
        self.parent = parent
        self.layout = layout
        self.widget_class = widget_class

        self.create_widgets()
        self.add_to_layout()
        self.connect_signals()

    def create_widgets(self):
        self.label = QLabel(self.data_attr.capitalize())
        self.edit = self.widget_class(getattr(self.parent.data, self.data_attr))

    def add_to_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

    def connect_signals(self):
        if isinstance(self.edit, QTextEdit):
            self.edit.textChanged.connect(self.update_data)
        elif isinstance(self.edit, QLineEdit):
            self.edit.textChanged.connect(self.update_data)

    def update_data(self):
        if isinstance(self.edit, QTextEdit):
            setattr(self.parent.data, self.data_attr, self.edit.toPlainText())
        elif isinstance(self.edit, QLineEdit):
            setattr(self.parent.data, self.data_attr, self.edit.text())

    def show(self):
        self.label.show()
        self.edit.show()

    def hide(self):
        self.label.hide()
        self.edit.hide()

class NodeLayout(QGraphicsItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Save the reference to the parent node

        # Create a widget to hold the QLineEdit widgets
        self.container_widget = QWidget()
        self.layout = QVBoxLayout()
        self.container_widget.setLayout(self.layout)

        # Type Label and Combo Box
        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["None", "Start", "Agent", "Task", "Step", "Team"])
        self.type_combo.setCurrentText(self.parent.data.type)
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.type_combo)
        self.layout.addLayout(self.type_layout)
        self.type_combo.currentTextChanged.connect(self.update_data_type)

        # Initialize slots
        self.slots = {}
        self.add_slot("name", QLineEdit)

        # Agent
        self.add_slot("role", QTextEdit)
        self.add_slot("goal", QTextEdit)
        self.add_slot("backstory", QTextEdit)
        
        # Task
        self.add_slot("agent", QTextEdit)
        self.add_slot("description", QTextEdit)
        self.add_slot("expected_output", QTextEdit)
        
        # Step
        self.add_slot("tool", QTextEdit)
        self.add_slot("arg", QTextEdit)
        self.add_slot("output_var", QTextEdit)
        
        self.proxy_widget = QGraphicsProxyWidget(self)
        self.proxy_widget.setWidget(self.container_widget)

        # Initialize visibility based on the current type
        self.update_field_visibility()

        # Call update_proxy_widget_geometry once to ensure layout is correct
        self.update_proxy_widget_geometry()

    def add_slot(self, data_attr, widget_class):
        slot = Slot(data_attr, self.parent, self.layout, widget_class)
        self.slots[data_attr] = slot

    def boundingRect(self):
        return self.parent.rect

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black))
        painter.drawRect(rect)

        # Draw right-bottom square
        painter.setBrush(QBrush(Qt.black))
        painter.drawRect(rect.right() - 10, rect.bottom() - 10, 10, 10)

    def update_proxy_widget_geometry(self):
        rect = self.boundingRect()
        self.proxy_widget.setGeometry(rect.adjusted(5, 5, -5, -5))

    def update_data_type(self):
        self.parent.data.type = self.type_combo.currentText()
        self.update_field_visibility()  # Update field visibility when type changes

    def update_field_visibility(self):
        node_type = self.parent.data.type
        for slot in self.slots.values():
            slot.hide()

        if node_type in ["Start", "None"]:
            pass
        elif node_type == "Team":
            self.slots["name"].show()
        elif node_type == "Agent":
            self.slots["name"].show()
            self.slots["role"].show()
            self.slots["goal"].show()
            self.slots["backstory"].show()
        elif node_type == "Task":
            self.slots["agent"].show()
            self.slots["description"].show()
            self.slots["expected_output"].show()
        elif node_type == "Step":
            self.slots["tool"].show()
            self.slots["arg"].show()
            self.slots["output_var"].show()



        # Update geometry after setting visibility
        self.update_proxy_widget_geometry()
