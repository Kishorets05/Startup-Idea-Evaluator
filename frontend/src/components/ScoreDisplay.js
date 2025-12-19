import React from 'react';
import './ScoreDisplay.css';

function ScoreDisplay({ score }) {
  const getScoreColor = (score) => {
    if (score >= 70) return '#27ae60'; // Green
    if (score >= 50) return '#f39c12'; // Orange
    return '#e74c3c'; // Red
  };

  const getScoreLabel = (score) => {
    if (score >= 70) return 'High Potential';
    if (score >= 50) return 'Moderate Potential';
    return 'Needs Improvement';
  };

  const scoreColor = getScoreColor(score);
  const scoreLabel = getScoreLabel(score);

  return (
    <div className="score-display">
      <div className="score-circle" style={{ borderColor: scoreColor }}>
        <div className="score-value" style={{ color: scoreColor }}>
          {score}
        </div>
        <div className="score-max">/ 100</div>
      </div>
      <div className="score-label" style={{ color: scoreColor }}>
        {scoreLabel}
      </div>
      <div className="score-description">
        Feasibility Score
      </div>
    </div>
  );
}

export default ScoreDisplay;

