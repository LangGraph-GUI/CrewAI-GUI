# CrewAI-GUI
crewai frontend gui.

This is node based gui for crewai frontend. that will export to json for better decoupling.

![](./frontend.webp)

### Limitation

Current node types and slots are limited.

Not all crewai var or features have imp the path.

## Environment

### front-end GUI
```
pip install PySide6
```

### back-end
```
pip install 'crewai[tools]' langchain crewai

```

## Usage

### front-end GUI

run

```
python frontend.py
```
and you can read and write json file as DAG graph for crewai.

### back-end

run

```
python backend.py --graph example.json --keys credentials.ini --tee output.log
```
it will parse json file into crewai tasks and agents


## Build

### front-end GUI

```
pip install pyinstaller

pyinstaller --onefile --additional-hooks-dir=. frontend.py
```