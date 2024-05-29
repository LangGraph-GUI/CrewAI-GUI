import React, { useState } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  MiniMap,
  Controls,
  Background,
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Node 1' },
    position: { x: 250, y: 5 },
  },
];

const Flow = () => {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const onNodesChange = (changes) => setNodes((nds) => nds.map((node) => ({ ...node, ...changes })));

  const onEdgesChange = (changes) => setEdges((eds) => eds.map((edge) => ({ ...edge, ...changes })));

  const onLoad = (rfi) => {
    setReactFlowInstance(rfi);
    rfi.fitView();
  };

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    const newNode = {
      id: `${+new Date()}`,
      data: { label: `Node ${nodes.length + 1}` },
      position: reactFlowInstance.project({ x: event.clientX, y: event.clientY }),
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
