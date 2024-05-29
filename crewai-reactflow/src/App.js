// App.js

import React, { useState } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './ContextMenu.css'; // Import the CSS for the context menu
import ContextMenu from './ContextMenu'; // Import the ContextMenu component

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Node 1' },
    position: { x: 250, y: 5 },
    draggable: true,
  },
];

const Flow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [contextMenu, setContextMenu] = useState(null);

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    setContextMenu({ x: event.clientX, y: event.clientY });
  };

  const onAddNode = () => {
    const newNode = {
      id: `${+new Date()}`,
      data: { label: `Node ${nodes.length + 1}` },
      position: { x: 250, y: 5 },
      draggable: true,
    };

    setNodes((nds) => nds.concat(newNode));
    setContextMenu(null);
  };

  return (
    <ReactFlowProvider>
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
          fitView
        >
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
        {contextMenu && (
          <ContextMenu
            x={contextMenu.x}
            y={contextMenu.y}
            onAddNode={onAddNode}
          />
        )}
      </div>
    </ReactFlowProvider>
  );
};

export default Flow;
