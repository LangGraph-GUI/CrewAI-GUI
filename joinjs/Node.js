function addNode(graph) {
    var rect = new joint.shapes.standard.Rectangle();
    rect.position(100, 100); // Set the position of the rectangle
    rect.resize(100, 40); // Set the size of the rectangle
    rect.attr({
        body: {
            fill: 'blue' // Fill color of the rectangle
        },
        label: {
            text: 'Node', // Label text
            fill: 'white' // Label text color
        }
    });
    rect.addTo(graph); // Add the rectangle to the graph
}
