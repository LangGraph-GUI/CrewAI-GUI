from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QProcess

class ExecCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Execute Command")
        self.setModal(True)
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter your command here")
        self.command_input.setText("backend.exe --graph example.json --keys credentials.ini --tee output.log")
        
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
        
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

    def run_command(self):
        command = self.command_input.text().strip()
        if command:
            self.output_text.clear()
            parts = command.split()
            program = parts[0]
            arguments = parts[1:]
            self.process.start(program, arguments)
            if not self.process.waitForStarted():
                QMessageBox.critical(self, "Error", "Failed to start the command.")
                self.output_text.append("Failed to start the command.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter a command.")

    def read_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = data.data().decode()
        self.output_text.append(stdout)

    def read_stderr(self):
        data = self.process.readAllStandardError()
        stderr = data.data().decode()
        self.output_text.append(stderr)
        
    def process_finished(self):
        self.output_text.append("Process finished.")
        exit_code = self.process.exitCode()
        self.output_text.append(f"Process exited with code: {exit_code}")

