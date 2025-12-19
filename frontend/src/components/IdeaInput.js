import React, { useState } from 'react';
import './IdeaInput.css';

function IdeaInput({ onEvaluate, loading, error }) {
  const [ideaText, setIdeaText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ideaText.trim()) {
      onEvaluate(ideaText);
    }
  };

  return (
    <div className="idea-input-container">
      <div className="card">
        <h2>Enter Your Startup Idea</h2>
        <p className="instruction-text">
          Describe your startup idea in detail. Include the problem you're solving, 
          your target audience, and your proposed solution.
        </p>
        
        <form onSubmit={handleSubmit}>
          <textarea
            className="idea-textarea"
            value={ideaText}
            onChange={(e) => setIdeaText(e.target.value)}
            placeholder="Example: A mobile app that connects local farmers directly with consumers, eliminating middlemen and ensuring fresh produce delivery within 24 hours. The app will include features like real-time inventory, subscription boxes, and farm-to-table tracking..."
            rows="8"
            disabled={loading}
            required
          />
          
          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="evaluate-button"
            disabled={loading || !ideaText.trim()}
          >
            {loading ? 'Evaluating...' : 'Evaluate Startup'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default IdeaInput;

