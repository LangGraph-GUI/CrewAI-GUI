// src/components/Flow.js

import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import ContextMenu from './ContextMenu';
import CustomNode from './CustomNode';
import useContextMenu from '../hooks/useContextMenu';
import '../components/ContextMenu.css';
import '../components/CustomNode.css';

const nodeTypes = {
  custom: CustomNode,
};

const Flow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const {
    contextMenu,
    nodeIdToDelete,
    onPaneContextMenu,
    onNodeContextMenu,
    onAddNode,
    onDeleteNode,
    handlePaneClick,
  } = useContextMenu({ nodes, setNodes, setEdges });

  const { project } = useReactFlow();

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

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

export default Flow;
