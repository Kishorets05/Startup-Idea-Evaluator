import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-overlay">
      <div className="spinner-container">
        <div className="spinner"></div>
        <p>Analyzing your startup idea...</p>
      </div>
    </div>
  );
}

export default LoadingSpinner;

