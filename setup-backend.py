from cx_Freeze import setup, Executable

# Define the executable and other build options
executables = [Executable("backend.py")]

build_options = {
    'packages': [],
    'excludes': [],
}

setup(
    name="MyApplication",
    version="0.1",
    description="My Python Application",
    options={'build_exe': build_options},
    executables=executables
)
