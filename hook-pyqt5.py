from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('PyQt6')
datas = collect_data_files('PyQt6', include_py_files=True)