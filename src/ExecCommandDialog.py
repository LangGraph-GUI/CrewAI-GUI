from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QMessageBox, QComboBox
from PySide6.QtCore import Qt, QProcess
import sys

class ExecCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Execute Command")
        self.setModal(True)
        self.setMinimumSize(400, 400)

        print("Initializing ExecCommandDialog")  # Debug print

        self.layout = QVBoxLayout()

        self.backend_input = QLineEdit(self)
        self.backend_input.setPlaceholderText("Enter the backend executable")
        self.backend_input.setText("backend.exe")

        self.graph_file_input = QLineEdit(self)
        self.graph_file_input.setPlaceholderText("Enter the graph file")
        self.graph_file_input.setText("example.json")

        self.keys_choice = QComboBox(self)
        self.keys_choice.addItem("GPT4o")
        self.keys_choice.addItem("Ollama")
        self.keys_choice.currentIndexChanged.connect(self.update_ui)

        self.keys_input = QLineEdit(self)
        self.keys_input.setPlaceholderText("Enter the keys file")
        self.keys_input.setText("credentials.ini")

        self.llm_input = QLineEdit(self)
        self.llm_input.setPlaceholderText("Enter the LLM model")
        self.llm_input.setText("phi3")
        self.llm_input.hide()  # Hide LLM input by default

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
        self.layout.addWidget(QLabel("Key Files:"))
        self.layout.addWidget(self.keys_choice)
        self.layout.addWidget(self.keys_input)
        self.layout.addWidget(self.llm_input)
        self.layout.addWidget(self.log_to_file_checkbox)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(QLabel("Output:"))
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

        print("ExecCommandDialog initialized")  # Debug print

    def update_ui(self):
        print(f"Updating UI: Keys choice changed to {self.keys_choice.currentText()}")  # Debug print
        if self.keys_choice.currentText() == "Ollama":
            self.keys_input.hide()
            self.llm_input.show()
        else:
            self.keys_input.show()
            self.llm_input.hide()

    def run_command(self):
        print("Run command triggered")  # Debug print
        backend = self.backend_input.text().strip()
        graph_file = self.graph_file_input.text().strip()
        keys_choice = self.keys_choice.currentText()
        log_to_file = self.log_to_file_checkbox.isChecked()

        print(f"Backend: {backend}")  # Debug print
        print(f"Graph file: {graph_file}")  # Debug print
        print(f"Keys choice: {keys_choice}")  # Debug print
        print(f"Log to file: {log_to_file}")  # Debug print

        if backend and graph_file:
            self.output_text.clear()
            if keys_choice == "Ollama":
                llm = self.llm_input.text().strip()
                if not llm:
                    print("Error: LLM model not specified")  # Debug print
                    QMessageBox.warning(self, "Warning", "Please enter the LLM model.")
                    return
                command = [backend, "--graph", graph_file, "--llm", llm]
            else:
                keys_file = self.keys_input.text().strip()
                if not keys_file:
                    print("Error: Keys file not specified")  # Debug print
                    QMessageBox.warning(self, "Warning", "Please enter the keys file.")
                    return
                command = [backend, "--graph", graph_file, "--keys", keys_file]

            if log_to_file:
                command.append("--tee")
                command.append("output.log")

            print(f"Executing command: {' '.join(command)}")  # Debug print
            self.process.start(command[0], command[1:])
            if not self.process.waitForStarted():
                print("Error: Failed to start the command")  # Debug print
                QMessageBox.critical(self, "Error", "Failed to start the command.")
                self.output_text.append("Failed to start the command.")
        else:
            print("Error: Backend or graph file not specified")  # Debug print
            QMessageBox.warning(self, "Warning", "Please enter all required fields.")

    def read_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = data.data().decode()
        print(f"Process stdout: {stdout}")  # Debug print
        self.output_text.append(stdout)

    def read_stderr(self):
        data = self.process.readAllStandardError()
        stderr = data.data().decode()
        print(f"Process stderr: {stderr}", file=sys.stderr)  # Debug print to stderr
        self.output_text.append(stderr)

    def process_finished(self):
        exit_code = self.process.exitCode()
        print(f"Process finished with exit code: {exit_code}")  # Debug print
        self.output_text.append("Process finished.")
        self.output_text.append(f"Process exited with code: {exit_code}")