// ContextMenu.js
import React from 'react';
import './ContextMenu.css';

const ContextMenu = ({ menuPosition, onAddNode }) => {
  if (!menuPosition) return null;

  return (
    <div
      className="context-menu"
      style={{
        top: menuPosition.y,
        left: menuPosition.x,
      }}
    >
      <button onClick={onAddNode}>Add Node</button>
    </div>
  );
};

export default ContextMenu;
