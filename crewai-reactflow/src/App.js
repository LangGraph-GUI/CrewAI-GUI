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

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Node 1' },
    position: { x: 250, y: 5 },
    draggable: true, // Ensure node is draggable
  },
];

const Flow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const onLoad = (rfi) => {
    setReactFlowInstance(rfi);
    rfi.fitView();
  };

  const onPaneContextMenu = (event) => {
    event.preventDefault();

    const newNode = {
      id: `${+new Date()}`,
      data: { label: `Node ${nodes.length + 1}` },
      position: { x: 250, y: 5 }, // Fixed position
      draggable: true, // Ensure new nodes are draggable
    };

    setNodes((nds) => nds.concat(newNode));
  };

  return (
    <ReactFlowProvider>
      <div style={{ width: '100%', height: '100vh' }} onContextMenu={onPaneContextMenu}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onLoad={onLoad}
          fitView
        >
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </ReactFlowProvider>
  );
};

export default Flow;
