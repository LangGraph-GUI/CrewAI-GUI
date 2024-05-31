$(document).ready(function() {
    function resizePaper() {
        var width = $(window).width();
        var height = $(window).height();
        paper.setDimensions(width, height);
    }

    // Create a JointJS graph
    var graph = new joint.dia.Graph();

    // Create a JointJS paper (view)
    var paper = new joint.dia.Paper({
        el: $('#paper'),
        model: graph,
        gridSize: 10,
        drawGrid: true
    });

    // Initial resize to fit the window
    resizePaper();

    // Add a node to the graph
    addNode(graph);

    // Resize the paper when the window is resized
    $(window).resize(function() {
        resizePaper();
    });

    // Variables to track the drag state
    var rightClickPan = false;
    var startX, startY;

    // Right mouse button down event
    $('#paper').on('mousedown', function(event) {
        if (event.which === 3) { // Right mouse button
            rightClickPan = true;
            startX = event.pageX;
            startY = event.pageY;
        }
    });

    // Mouse move event
    $(document).on('mousemove', function(event) {
        if (rightClickPan) {
            var dx = event.pageX - startX;
            var dy = event.pageY - startY;
            startX = event.pageX;
            startY = event.pageY;

            var translate = paper.translate();
            paper.translate(translate.tx + dx, translate.ty + dy);
        }
    });

    // Mouse up event
    $(document).on('mouseup', function(event) {
        if (event.which === 3) { // Right mouse button
            rightClickPan = false;
        }
    });

    // Disable the default context menu on the paper
    $('#paper').on('contextmenu', function(event) {
        event.preventDefault();
    });
});
