from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtCore import Qt
import subprocess

class ExecCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Execute Command")
        self.setModal(True)
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter your command here")
        self.command_input.setText("backend.exe --graph example.json --llm phi3 --tee output.log")  # Set default command here
        
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_command)
        
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        
        self.layout.addWidget(QLabel("Command:"))
        self.layout.addWidget(self.command_input)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(QLabel("Output:"))
        self.layout.addWidget(self.output_text)
        
        self.setLayout(self.layout)

    def run_command(self):
        command = self.command_input.text()
        if command:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                self.output_text.setPlainText(result.stdout + result.stderr)
            except Exception as e:
                self.output_text.setPlainText(str(e))
