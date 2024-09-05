<div align="center">

# 🤖 CrewAI-GUI

*A Node-Based Frontend for CrewAI*

![CrewAI-GUI Frontend](./frontend.webp)

[![GitHub stars](https://img.shields.io/github/stars/YourUsername/CrewAI-GUI.svg?style=for-the-badge&logo=github&color=gold)](https://github.com/YourUsername/CrewAI-GUI)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)

[Features](#-features) • [Installation](#️-installation) • [Usage](#-usage) • [Build](#️-building) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

- 🖱️ **Intuitive Node-Based GUI**: Drag-and-drop interface for effortless AI workflow creation
- 🔗 **JSON Export**: Seamlessly export designs to JSON for enhanced decoupling
- 🧠 **Flexible Backend**: Full support for both GPT-4 API and Ollama
- 💻 **Cross-Platform Compatibility**: Runs smoothly on Windows, Linux, and macOS

---

## 🎥 Video Introduction

<div align="center">

[![CrewAI-GUI Introduction](https://img.youtube.com/vi/P5tkYJ-AgSc/0.jpg)](https://www.youtube.com/watch?v=P5tkYJ-AgSc)

</div>

---

## 🛠️ Installation

<details>
<summary><b>Frontend GUI</b></summary>

```bash
pip install PySide6
```
</details>

<details>
<summary><b>Backend</b></summary>

For Linux:
```bash
pip install 'crewai[tools]' langchain crewai networkx
```

For Windows:
```bash
pip install crewai[tools] langchain crewai networkx
```
</details>

---

## 🚀 Usage

<details>
<summary><b>Frontend GUI</b></summary>

Launch the GUI:
```bash
python frontend.py
```
Create, manipulate, save, and load DAG graphs for CrewAI as JSON files.
</details>

<details>
<summary><b>Backend</b></summary>

For GPT-4:
```bash
python backend.py --graph example.json --keys credentials.ini --tee output.log
```

For Ollama (e.g., Mistral):
```bash
python backend.py --graph example.json --llm mistral --tee output.log
```
The backend converts JSON files into CrewAI tasks and agents.
</details>

---

## 🏗️ Building

<details>
<summary><b>Frontend GUI</b></summary>

Build with PyInstaller:
```bash
pip install pyinstaller
cd src
pyinstaller --onefile --additional-hooks-dir=. frontend.py
```
</details>

<details>
<summary><b>Backend</b></summary>

Build with cx_Freeze:
```bash
pip install cx_Freeze
cd src
python setup-backend.py build
```
</details>

---

## 📚 Documentation

Explore our comprehensive [GitHub Pages](https://yourusername.github.io/CrewAI-GUI/) for in-depth documentation.

---

## 🧪 Examples

Dive into our [example graph source](https://github.com/HomunMage/AI_Agents/blob/main/crewAI/gpt/agents.py) to see CrewAI-GUI in action.

---

## ⚠️ Limitations

- 🔒 Current node types and slots are limited
- 🚧 Some CrewAI variables and features are yet to be implemented

---

## 🤝 Contributing

We enthusiastically welcome contributions! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting pull requests, reporting issues, or requesting features.

---

## 📄 License

CrewAI-GUI is proudly released under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

## 📬 Contact

For inquiries, suggestions, or collaboration opportunities, please [open an issue](https://github.com/YourUsername/CrewAI-GUI/issues) on our GitHub repository.

---

<div align="center">

Made with ❤️ by [Your Name/Organization]

<br>

[⬆ Back to Top](#-crewai-gui)

</div>

<!-- Keywords: CrewAI, GUI, Node-Based Interface, AI Workflows, GPT-4, Ollama, Python -->