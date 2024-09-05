import os
import sys
import shutil
import pdoc
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath('src'))

def create_docs_folder():
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs')

def copy_non_python_files(src_dir, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if not file.endswith('.py'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_dir)
                dest_path = os.path.join(dest_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)

def generate_documentation():
    # Specify the modules to document
    modules = [
        'Tee',
        'ExecCommandDialog',
        'Edge',
        'NodeLayout',
        'CustomGraphicsView',
        'MainWindow',
        'WorkFlow',
        'file_operations',
        'MapView',
        'NodeData',
        'Node',
        'frontend',
        'backend'
    ]

    # Generate the documentation
    pdoc.pdoc(*modules, output_directory=Path('docs'))

def generate_main_readme():
    with open('docs/index.html', 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrewAI-GUI Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        h1 { color: #333; }
        ul { padding-left: 20px; }
        li { margin-bottom: 10px; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>CrewAI-GUI Documentation</h1>
    <p>This documentation provides an overview of the CrewAI-GUI project structure and components.</p>
    <h2>Project Structure</h2>
    <ul>
        <li><a href="Tee.html">Tee</a></li>
        <li><a href="ExecCommandDialog.html">ExecCommandDialog</a></li>
        <li><a href="Edge.html">Edge</a></li>
        <li><a href="NodeLayout.html">NodeLayout</a></li>
        <li><a href="CustomGraphicsView.html">CustomGraphicsView</a></li>
        <li><a href="MainWindow.html">MainWindow</a></li>
        <li><a href="WorkFlow.html">WorkFlow</a></li>
        <li><a href="file_operations.html">file_operations</a></li>
        <li><a href="MapView.html">MapView</a></li>
        <li><a href="NodeData.html">NodeData</a></li>
        <li><a href="Node.html">Node</a></li>
        <li><a href="frontend.html">frontend</a></li>
        <li><a href="backend.html">backend</a></li>
    </ul>
</body>
</html>
        """)

# Main execution
if __name__ == "__main__":
    create_docs_folder()
    generate_documentation()
    generate_main_readme()
    copy_non_python_files('src', 'docs/src')
    copy_non_python_files('example', 'docs/example')
    shutil.copy2('CHANGELOG.md', 'docs/CHANGELOG.md')
    shutil.copy2('README.md', 'docs/project_README.md')
    print("Enhanced HTML documentation generated successfully in the 'docs' folder.")