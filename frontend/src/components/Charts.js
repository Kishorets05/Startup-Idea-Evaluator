import React from 'react';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';
import './Charts.css';

// Register Chart.js components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function Charts({ evaluation }) {
  // Get component scores from backend evaluation
  const componentScores = evaluation.component_scores || {
    problem_clarity: evaluation.feasibility_score || 50,
    market_demand: evaluation.feasibility_score || 50,
    technical_feasibility: evaluation.feasibility_score || 50,
    innovation_level: evaluation.feasibility_score || 50,
    scalability: evaluation.feasibility_score || 50,
    risk_level: evaluation.feasibility_score || 50
  };

  const radarData = {
    labels: [
      'Problem Clarity',
      'Market Demand',
      'Technical Feasibility',
      'Innovation',
      'Scalability',
      'Risk Management'
    ],
    datasets: [
      {
        label: 'Score',
        data: [
          componentScores.problem_clarity || componentScores.problemClarity || 50,
          componentScores.market_demand || componentScores.marketDemand || 50,
          componentScores.technical_feasibility || componentScores.technicalFeasibility || 50,
          componentScores.innovation_level || componentScores.innovation || 50,
          componentScores.scalability || 50,
          componentScores.risk_level || componentScores.riskLevel || 50
        ],
        backgroundColor: 'rgba(102, 126, 234, 0.2)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(102, 126, 234, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
      }
    ]
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 20
        },
        pointLabels: {
          font: {
            size: 12
          }
        }
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return context.label + ': ' + context.parsed.r + '/100';
          }
        }
      }
    }
  };

  return (
    <div className="charts-container">
      <div className="chart-card">
        <h3>Component Analysis</h3>
        <div className="radar-chart">
          <Radar data={radarData} options={radarOptions} />
        </div>
      </div>
    </div>
  );
}

export default Charts;

