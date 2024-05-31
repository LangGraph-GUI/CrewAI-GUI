// FileOperator.js

function saveGraph(graph) {
    var json = JSON.stringify(graph.toJSON());
    localStorage.setItem('graph', json);
    alert('Graph saved!');
}

function loadGraph(graph) {
    var json = localStorage.getItem('graph');
    if (json) {
        graph.fromJSON(JSON.parse(json));
        alert('Graph loaded!');
    } else {
        alert('No saved graph found!');
    }
}
