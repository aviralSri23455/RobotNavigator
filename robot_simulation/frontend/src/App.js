import React from 'react';
import { startSimulation } from './api';

function App() {
  const handleStart = async () => {
    const response = await startSimulation();
    console.log(response.message);
  };

  return (
    <div className="App">
      <h1>Robot Simulation Control</h1>
      <button onClick={handleStart}>Start Simulation</button>
    </div>
  );
}

export default App;
