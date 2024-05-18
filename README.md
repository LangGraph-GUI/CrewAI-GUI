# CrewAI-GUI
crewai frontend gui.

This is node based gui for crewai frontend. that will export to json for better decoupling.

## Environment

### front-end GUI
```
pip install PySide6
```

### back-end
```
pip install PySide6
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
python backend.py 
```
it will parse json file into crewai tasks and agents


## Build

### front-end GUI

```
pip install pyinstaller

pyinstaller --onefile --additional-hooks-dir=. frontend.py
```