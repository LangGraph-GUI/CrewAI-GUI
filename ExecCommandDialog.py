from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QMessageBox
from PySide6.QtCore import Qt, QProcess

class ExecCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Execute Command")
        self.setModal(True)
        self.setMinimumSize(400, 400)

        self.layout = QVBoxLayout()

        self.backend_input = QLineEdit(self)
        self.backend_input.setPlaceholderText("Enter the backend executable")
        self.backend_input.setText("backend.exe")

        self.graph_file_input = QLineEdit(self)
        self.graph_file_input.setPlaceholderText("Enter the graph file")
        self.graph_file_input.setText("example.json")

        self.keys_input = QLineEdit(self)
        self.keys_input.setPlaceholderText("Enter the keys file")
        self.keys_input.setText("credentials.ini")

        self.log_to_file_checkbox = QCheckBox("Log to file", self)
        self.log_to_file_checkbox.setChecked(True)

        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_command)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        self.layout.addWidget(QLabel("Backend:"))
        self.layout.addWidget(self.backend_input)
        self.layout.addWidget(QLabel("Graph File:"))
        self.layout.addWidget(self.graph_file_input)
        self.layout.addWidget(QLabel("Keys File:"))
        self.layout.addWidget(self.keys_input)
        self.layout.addWidget(self.log_to_file_checkbox)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(QLabel("Output:"))
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

    def run_command(self):
        backend = self.backend_input.text().strip()
        graph_file = self.graph_file_input.text().strip()
        keys_file = self.keys_input.text().strip()
        log_to_file = self.log_to_file_checkbox.isChecked()

        if backend and graph_file and keys_file:
            self.output_text.clear()
            command = [backend, "--graph", graph_file, "--keys", keys_file]
            if log_to_file:
                command.append("--tee")
                command.append("output.log")
            self.process.start(command[0], command[1:])
            if not self.process.waitForStarted():
                QMessageBox.critical(self, "Error", "Failed to start the command.")
                self.output_text.append("Failed to start the command.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter all required fields.")

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

