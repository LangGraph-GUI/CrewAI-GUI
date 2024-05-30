// src/App.js

import React from 'react';
import { ReactFlowProvider } from 'reactflow';
import Flow from './components/Flow';

const App = () => (
  <ReactFlowProvider>
    <Flow />
  </ReactFlowProvider>
);

export default App;
