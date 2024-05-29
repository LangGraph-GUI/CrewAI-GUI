// CustomNode.js

import React from 'react';
import { Handle } from 'reactflow';
import './CustomNode.css';

const CustomNode = ({ data }) => {
  console.log('CustomNode rendered with data:', data);

  return (
    <div className="custom-node">
      <div>{data.label}</div>
      <Handle type="source" position="right" id="a" style={{ top: 10, background: '#555' }} />
      <Handle type="source" position="right" id="b" style={{ bottom: 10, top: 'auto', background: '#555' }} />
      <Handle type="target" position="left" style={{ background: '#555' }} />
    </div>
  );
};

export default CustomNode;
