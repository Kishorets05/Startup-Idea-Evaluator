import React from 'react';
import './EvaluationResults.css';
import ScoreDisplay from './ScoreDisplay';
import EvaluationSections from './EvaluationSections';
import Charts from './Charts';
import PDFDownload from './PDFDownload';

function EvaluationResults({ evaluation, onReset, apiBaseUrl }) {
  return (
    <div className="evaluation-results">
      <div className="results-header">
        <h2>Evaluation Results</h2>
        <button onClick={onReset} className="reset-button">
          Evaluate Another Idea
        </button>
      </div>

      <ScoreDisplay score={evaluation.feasibility_score} />

      <Charts evaluation={evaluation} />

      <EvaluationSections evaluation={evaluation} />

      <PDFDownload evaluation={evaluation} apiBaseUrl={apiBaseUrl} />
    </div>
  );
}

export default EvaluationResults;

