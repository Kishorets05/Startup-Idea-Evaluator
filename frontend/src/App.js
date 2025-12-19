import React, { useState } from 'react';
import './App.css';
import IdeaInput from './components/IdeaInput';
import EvaluationResults from './components/EvaluationResults';
import LoadingSpinner from './components/LoadingSpinner';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://startup-idea-evaluator-bryf.onrender.com';

function App() {
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async (ideaText) => {
    setLoading(true);
    setError(null);
    setEvaluation(null);

    try {
      const response = await fetch(`${API_BASE_URL}/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea: ideaText }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to evaluate startup idea');
      }

      if (data.success && data.evaluation) {
        setEvaluation(data.evaluation);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while evaluating your idea');
      console.error('Evaluation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setEvaluation(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="app-header">
          <h1>🚀 Startup Evaluator</h1>
          <p className="subtitle">AI-Powered Startup Idea Analysis</p>
        </header>

        {!evaluation ? (
          <IdeaInput onEvaluate={handleEvaluate} loading={loading} error={error} />
        ) : (
          <EvaluationResults 
            evaluation={evaluation} 
            onReset={handleReset}
            apiBaseUrl={API_BASE_URL}
          />
        )}

        {loading && <LoadingSpinner />}
      </div>
    </div>
  );
}

export default App;

