import React, { useState } from 'react';
import './EvaluationSections.css';

function EvaluationSections({ evaluation }) {
  const [expandedSection, setExpandedSection] = useState(null);

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const sections = [
    {
      key: 'executive_summary',
      title: 'Executive Summary',
      content: evaluation.executive_summary,
      type: 'text'
    },
    {
      key: 'problem_statement',
      title: 'Problem Statement',
      content: evaluation.problem_statement,
      type: 'text'
    },
    {
      key: 'target_users',
      title: 'Target Users',
      content: evaluation.target_users,
      type: 'text'
    },
    {
      key: 'market_potential',
      title: 'Market Potential',
      content: evaluation.market_potential,
      type: 'text'
    },
    {
      key: 'technical_feasibility',
      title: 'Technical Feasibility',
      content: evaluation.technical_feasibility,
      type: 'text'
    },
    {
      key: 'innovation_uniqueness',
      title: 'Innovation & Uniqueness',
      content: evaluation.innovation_uniqueness,
      type: 'text'
    },
    {
      key: 'risks_challenges',
      title: 'Risks & Challenges',
      content: evaluation.risks_challenges,
      type: 'text'
    },
    {
      key: 'strengths',
      title: 'Strengths',
      content: evaluation.strengths,
      type: 'list'
    },
    {
      key: 'weaknesses',
      title: 'Weaknesses',
      content: evaluation.weaknesses,
      type: 'list'
    },
    {
      key: 'improvement_suggestions',
      title: 'Improvement Suggestions',
      content: evaluation.improvement_suggestions,
      type: 'list'
    },
    {
      key: 'final_recommendation',
      title: 'Final Recommendation',
      content: evaluation.final_recommendation,
      type: 'text'
    }
  ];

  return (
    <div className="evaluation-sections">
      {sections.map((section) => (
        <div key={section.key} className="section-card">
          <div 
            className="section-header"
            onClick={() => toggleSection(section.key)}
          >
            <h3>{section.title}</h3>
            <span className="toggle-icon">
              {expandedSection === section.key ? '−' : '+'}
            </span>
          </div>
          
          {expandedSection === section.key && (
            <div className="section-content">
              {section.type === 'list' ? (
                <ul>
                  {Array.isArray(section.content) 
                    ? section.content.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))
                    : <li>{section.content}</li>
                  }
                </ul>
              ) : (
                <p>{section.content}</p>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default EvaluationSections;

