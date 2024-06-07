# hook-pyside6.py

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('PySide6')
datas = collect_data_files('PySide6', include_py_files=True)
