// App.js

import React, { useState, useCallback, useRef, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  Background,
  Controls,
  MiniMap
} from 'reactflow';
import 'reactflow/dist/style.css';
import './App.css';
import ContextMenu from './ContextMenu';
import CustomNode from './CustomNode';
import CustomEdge from './CustomEdge';

const initialElements = [];

const nodeTypes = {
  customNode: CustomNode,
};

const edgeTypes = {
  customEdge: CustomEdge,
};

function App() {
  const [nodes, setNodes] = useState(initialElements);
  const [edges, setEdges] = useState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [menuPosition, setMenuPosition] = useState(null);
  const [isInstanceLoaded, setIsInstanceLoaded] = useState(false);

  const reactFlowWrapper = useRef(null);
  const idRef = useRef(0);  // Use ref for ID generation

  const onLoad = useCallback((rfi) => {
    console.log('Flow loaded:', rfi);
    setReactFlowInstance(rfi);
    setIsInstanceLoaded(true);
    rfi.fitView();
  }, []);

  const onNodesChange = useCallback((changes) =>
    setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes) =>
    setEdges((eds) => applyEdgeChanges(changes, eds)), []);
  const onConnect = useCallback((params) => setEdges((eds) => addEdge({ ...params, type: 'customEdge' }, eds)), []);

  const handleAddNode = (event) => {
    event.preventDefault();
    setMenuPosition({
      x: event.clientX,
      y: event.clientY,
    });
  };

  const addNode = () => {
    if (!isInstanceLoaded || !reactFlowInstance) {
      console.error('React Flow instance is not available');
      return;
    }

    if (!menuPosition) {
      console.error('Menu position is not set');
      return;
    }

    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const position = reactFlowInstance.project({
      x: menuPosition.x - reactFlowBounds.left,
      y: menuPosition.y - reactFlowBounds.top,
    });
    const newNode = {
      id: `dndnode_${idRef.current++}`,  // Generate unique ID
      type: 'customNode',
      position,
      data: { label: 'New Custom Node' },
    };

    setNodes((nds) => [...nds, newNode]);
    setMenuPosition(null); // Hide the context menu after adding the node
  };

  return (
    <div className="App">
      <ReactFlowProvider>
        <div
          className="reactflow-wrapper"
          ref={reactFlowWrapper}
          style={{ width: '100vw', height: '100vh' }}
          onContextMenu={handleAddNode}
        >
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onLoad={onLoad}  // Ensure onLoad is set
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
          >
            <Background color="#aaa" gap={16} />
            <Controls />
            <MiniMap />
          </ReactFlow>
          <ContextMenu menuPosition={menuPosition} onAddNode={addNode} />
        </div>
      </ReactFlowProvider>
    </div>
  );
}

export default App;
