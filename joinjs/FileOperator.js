// FileOperator.js

function saveGraphToFile(graph) {
    const json = JSON.stringify(graph.toJSON());
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'graph.json';

    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
}

function loadGraphFromFile(graph, file) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const json = event.target.result;
        graph.fromJSON(JSON.parse(json));
        alert('Graph loaded!');
    };
    reader.readAsText(file);
}

function loadGraphFromFileInput(graph) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.style.display = 'none';

    input.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            loadGraphFromFile(graph, file);
        }
    });

    document.body.appendChild(input);
    input.click();
    document.body.removeChild(input);
}
