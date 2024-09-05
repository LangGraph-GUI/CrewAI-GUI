# 🤖 CrewAI-GUI

<div align="center">

*A Node-Based Frontend for CrewAI: Revolutionizing AI Workflow Creation*

![CrewAI-GUI Frontend](./frontend.webp)

[![GitHub stars](https://img.shields.io/github/stars/LangGraph-GUI/CrewAI-GUI.svg?style=for-the-badge&logo=github&color=gold)](https://github.com/LangGraph-GUI/CrewAI-GUI)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)

[Features](#-features) • [Installation](#️-installation) • [Usage](#-usage) • [Build](#️-build) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

CrewAI-GUI empowers you to create sophisticated AI workflows with ease:

- 🖱️ **Intuitive Node-Based Interface**: Design complex AI agent interactions through a user-friendly drag-and-drop interface
- 🔗 **JSON Export**: Seamlessly export your CrewAI designs to JSON, enhancing modularity and reusability
- 🧠 **Flexible AI Backend**: Full support for both GPT-4 API and Ollama, catering to various AI needs
- 💻 **Cross-Platform Compatibility**: Create AI workflows on Windows, Linux, or macOS with equal efficiency

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

Launch the CrewAI-GUI interface:
```bash
python frontend.py
```
Create, manipulate, save, and load Directed Acyclic Graph (DAG) structures for CrewAI as JSON files.
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
The backend seamlessly converts JSON files into CrewAI tasks and agents.
</details>

---

## 🏗️ Build

<details>
<summary><b>Frontend GUI</b></summary>

Build a standalone executable with PyInstaller:
```bash
pip install pyinstaller
cd src
pyinstaller --onefile --additional-hooks-dir=. frontend.py
```
</details>

<details>
<summary><b>Backend</b></summary>

Create a distributable package with cx_Freeze:
```bash
pip install cx_Freeze
cd src
python setup-backend.py build
```
</details>

---

## 📚 Documentation

Dive deep into CrewAI-GUI with our comprehensive [GitHub Pages Documentation](https://LangGraph-GUI.github.io/CrewAI-GUI/).

---

## 🧪 Examples

Explore real-world applications of CrewAI-GUI in our [example graph source](https://github.com/HomunMage/AI_Agents/blob/main/crewAI/gpt/agents.py).

---

## ⚠️ Limitations

- 🔒 The current version has a limited set of node types and slots
- 🚧 Some CrewAI variables and advanced features are yet to be implemented

---

## 🤝 Contributing

We welcome contributions to CrewAI-GUI! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Submitting pull requests
- Reporting issues
- Requesting new features

---

## 📄 License

CrewAI-GUI is open-source software, released under the MIT License. See the [LICENSE](LICENSE) file for full details.

---

## 📬 Contact

For questions, suggestions, or collaboration opportunities, please [open an issue](https://github.com/LangGraph-GUI/CrewAI-GUI/issues) on our GitHub repository.

---

<div align="center">

Crafted with ❤️ by the `LangGraph-GUI` Team

<br>

[⬆ Back to Top](#-crewai-gui)

</div>

<!-- Keywords: CrewAI, GUI, Node-Based Interface, AI Workflows, GPT-4, Ollama, Python, Drag-and-Drop, JSON Export, Cross-Platform -->