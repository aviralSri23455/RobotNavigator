// src/api.js
export const startSimulation = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/start-simulation', {
        method: 'POST',
      });
      return await response.json();
    } catch (error) {
      console.error('Error starting simulation:', error);
    }
  };
  