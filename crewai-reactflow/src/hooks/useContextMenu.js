// src/hooks/useContextMenu.js

import { useState, useCallback } from 'react';

const useContextMenu = ({ nodes, setNodes, setEdges }) => {
  const [contextMenu, setContextMenu] = useState(null);
  const [nodeIdToDelete, setNodeIdToDelete] = useState(null);

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    const reactFlowBounds = event.target.getBoundingClientRect();
    const position = {
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    };
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

  return {
    contextMenu,
    nodeIdToDelete,
    onPaneContextMenu,
    onNodeContextMenu,
    onAddNode,
    onDeleteNode,
    handlePaneClick,
  };
};

export default useContextMenu;
