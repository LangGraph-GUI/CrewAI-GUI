// ContextMenu.js

import React from 'react';
import './ContextMenu.css'; // Import the CSS for the context menu

const ContextMenu = ({ x, y, onAddNode, onDeleteNode }) => {
  return (
    <div className="context-menu" style={{ top: y, left: x }}>
      <button onClick={onAddNode}>Add Node</button>
      <button onClick={onDeleteNode}>Delete Node</button>
    </div>
  );
};

export default ContextMenu;
