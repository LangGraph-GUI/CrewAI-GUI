import React, { useState, useCallback, useRef } from 'react';
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

const initialElements = [];

function App() {
  const [nodes, setNodes] = useState(initialElements);
  const [edges, setEdges] = useState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [menuPosition, setMenuPosition] = useState(null);

  const reactFlowWrapper = useRef(null);

  const onLoad = useCallback((rfi) => {
    console.log('Flow loaded:', rfi);
    setReactFlowInstance(rfi);
    rfi.fitView();
  }, []);

  const onNodesChange = useCallback((changes) =>
    setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes) =>
    setEdges((eds) => applyEdgeChanges(changes, eds)), []);
  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

  const handleAddNode = (event) => {
    event.preventDefault();
    setMenuPosition({
      x: event.clientX,
      y: event.clientY,
    });
  };

  const addNode = () => {
    if (!reactFlowInstance || !menuPosition) {
      console.error('React Flow instance is not available or menu position is not set');
      return;
    }

    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const position = reactFlowInstance.project({
      x: menuPosition.x - reactFlowBounds.left,
      y: menuPosition.y - reactFlowBounds.top,
    });
    const newNode = {
      id: getId(),
      type: 'default',
      position,
      data: { label: 'New Node' },
    };

    setNodes((nds) => nds.concat(newNode));
    setMenuPosition(null);
  };

  let id = 0;
  const getId = () => `dndnode_${id++}`;

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
            onLoad={onLoad}
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
