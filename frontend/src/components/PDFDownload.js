import React, { useState } from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './PDFDownload.css';

function PDFDownload({ evaluation, apiBaseUrl }) {
  const [generating, setGenerating] = useState(false);

  const generatePDF = async () => {
    setGenerating(true);
    
    try {
      // Create a temporary div with all the content
      const content = document.createElement('div');
      content.style.width = '800px';
      content.style.padding = '40px';
      content.style.backgroundColor = 'white';
      content.style.position = 'absolute';
      content.style.left = '-9999px';
      document.body.appendChild(content);

      // Build PDF content
      content.innerHTML = `
        <div style="text-align: center; margin-bottom: 30px;">
          <h1 style="color: #2c3e50; font-size: 32px; margin-bottom: 10px;">Startup Evaluation Report</h1>
          <p style="color: #7f8c8d;">Generated on ${new Date().toLocaleDateString()}</p>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
          <div style="font-size: 48px; font-weight: bold; color: ${getScoreColor(evaluation.feasibility_score)};">
            ${evaluation.feasibility_score}/100
          </div>
          <p style="color: #7f8c8d; font-size: 18px;">Feasibility Score</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Executive Summary</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.executive_summary}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Problem Statement</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.problem_statement}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Target Users</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.target_users}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Market Potential</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.market_potential}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Technical Feasibility</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.technical_feasibility}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Innovation & Uniqueness</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.innovation_uniqueness}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Risks & Challenges</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.risks_challenges}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Strengths</h2>
          <ul style="line-height: 2; color: #34495e;">
            ${evaluation.strengths.map(s => `<li>${s}</li>`).join('')}
          </ul>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Weaknesses</h2>
          <ul style="line-height: 2; color: #34495e;">
            ${evaluation.weaknesses.map(w => `<li>${w}</li>`).join('')}
          </ul>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Improvement Suggestions</h2>
          <ul style="line-height: 2; color: #34495e;">
            ${evaluation.improvement_suggestions.map(i => `<li>${i}</li>`).join('')}
          </ul>
        </div>
        
        <div style="margin-bottom: 30px;">
          <h2 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Final Recommendation</h2>
          <p style="line-height: 1.8; color: #34495e;">${evaluation.final_recommendation}</p>
        </div>
      `;

      // Convert to canvas and then to PDF
      const canvas = await html2canvas(content, {
        scale: 2,
        useCORS: true,
        logging: false
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgWidth = 210;
      const pageHeight = 297;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      // Clean up
      document.body.removeChild(content);

      // Save PDF
      pdf.save(`startup_evaluation_${Date.now()}.pdf`);
      
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return '#27ae60';
    if (score >= 50) return '#f39c12';
    return '#e74c3c';
  };

  return (
    <div className="pdf-download-container">
      <button 
        onClick={generatePDF} 
        className="pdf-button"
        disabled={generating}
      >
        {generating ? 'Generating PDF...' : '📄 Download PDF Report'}
      </button>
    </div>
  );
}

export default PDFDownload;

