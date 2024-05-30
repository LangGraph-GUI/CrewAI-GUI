// App.js

import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './ContextMenu.css'; // Import the CSS for the context menu
import './CustomNode.css'; // Import the CSS for the custom node
import ContextMenu from './ContextMenu'; // Import the ContextMenu component
import CustomNode from './CustomNode'; // Import the CustomNode component

const nodeTypes = {
  custom: CustomNode,
};

const Flow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [contextMenu, setContextMenu] = useState(null);
  const [nodeIdToDelete, setNodeIdToDelete] = useState(null);
  const { project } = useReactFlow();

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    const reactFlowBounds = event.target.getBoundingClientRect();
    const position = project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });
    setContextMenu({
      type: 'pane',
      x: position.x,
      y: position.y,
      clientX: event.clientX,
      clientY: event.clientY,
    });
  };

  const onNodeContextMenu = (event, node) => {
    event.preventDefault();
    setNodeIdToDelete(node.id);
    setContextMenu({
      type: 'node',
      clientX: event.clientX,
      clientY: event.clientY,
    });
  };

  const onAddNode = () => {
    const newNode = {
      id: `${+new Date()}`,
      type: 'custom',
      data: { label: `Node ${nodes.length + 1}` },
      position: { x: contextMenu.x, y: contextMenu.y },
      draggable: true,
    };

    setNodes((nds) => nds.concat(newNode));
    setContextMenu(null);
  };

  const onDeleteNode = () => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeIdToDelete));
    setEdges((eds) => eds.filter((edge) => edge.source !== nodeIdToDelete && edge.target !== nodeIdToDelete));
    setContextMenu(null);
  };

  const handlePaneClick = useCallback((event) => {
    if (contextMenu) {
      setContextMenu(null);
    }
  }, [contextMenu]);

  useEffect(() => {
    const paneElement = document.querySelector('.react-flow__pane');
    paneElement.addEventListener('mousedown', handlePaneClick);

    return () => {
      paneElement.removeEventListener('mousedown', handlePaneClick);
    };
  }, [handlePaneClick]);

  return (
    <div
      style={{ width: '100%', height: '100vh', position: 'relative' }}
      onContextMenu={onPaneContextMenu}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        onNodeContextMenu={onNodeContextMenu}
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
      {contextMenu && (
        <ContextMenu
          x={contextMenu.clientX}
          y={contextMenu.clientY}
          onAddNode={onAddNode}
          onDeleteNode={onDeleteNode}
        />
      )}
    </div>
  );
};

const App = () => (
  <ReactFlowProvider>
    <Flow />
  </ReactFlowProvider>
);

export default App;
