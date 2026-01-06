"""
PDF Generator Service - Creates downloadable PDF reports
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict


class PDFGenerator:
    """Service for generating PDF evaluation reports"""
    
    def __init__(self):
        self.output_dir = "reports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_report(self, evaluation: Dict) -> str:
        """
        Generate PDF report from evaluation data
        
        Args:
            evaluation: Dictionary containing evaluation results
            
        Returns:
            str: Path to generated PDF file
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"startup_evaluation_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#34495e'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leftIndent=0
        )
        
        # Bullet list style for consistent formatting
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#34495e'),
            alignment=TA_LEFT,
            spaceAfter=10,
            leftIndent=25,
            firstLineIndent=-15
        )
        
        # Title
        story.append(Paragraph("Startup Evaluation Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"<i>Generated on: {date_str}</i>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Feasibility Score (Highlighted) - Clean formatting
        score = evaluation.get('feasibility_score', 0)
        score_color = self._get_score_color(score)
        
        # Label style
        label_style = ParagraphStyle(
            'ScoreLabelStyle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        # Score value style
        score_style = ParagraphStyle(
            'ScoreStyle',
            parent=styles['Heading1'],
            fontSize=48,
            textColor=score_color,
            alignment=TA_CENTER,
            spaceAfter=20,
            spaceBefore=10
        )
        
        # Add label and score separately to avoid overlap
        story.append(Paragraph("Feasibility Score", label_style))
        story.append(Paragraph(f"{score}/100", score_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(evaluation.get('executive_summary', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Problem Statement
        story.append(Paragraph("Problem Statement", heading_style))
        story.append(Paragraph(evaluation.get('problem_statement', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Target Users
        story.append(Paragraph("Target Users", heading_style))
        story.append(Paragraph(evaluation.get('target_users', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Market Potential
        story.append(Paragraph("Market Potential", heading_style))
        story.append(Paragraph(evaluation.get('market_potential', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Technical Feasibility
        story.append(Paragraph("Technical Feasibility", heading_style))
        story.append(Paragraph(evaluation.get('technical_feasibility', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Innovation & Uniqueness
        story.append(Paragraph("Innovation & Uniqueness", heading_style))
        story.append(Paragraph(evaluation.get('innovation_uniqueness', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Risks & Challenges
        story.append(Paragraph("Risks & Challenges", heading_style))
        story.append(Paragraph(evaluation.get('risks_challenges', 'N/A'), body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Strengths
        story.append(Paragraph("Strengths", heading_style))
        strengths = evaluation.get('strengths', [])
        if strengths and len(strengths) > 0:
            for strength in strengths:
                # Clean bullet formatting with proper spacing
                clean_strength = str(strength).strip()
                if clean_strength:
                    story.append(Paragraph(f"• {clean_strength}", bullet_style))
        else:
            story.append(Paragraph("No strengths identified.", body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Weaknesses
        story.append(Paragraph("Weaknesses", heading_style))
        weaknesses = evaluation.get('weaknesses', [])
        if weaknesses and len(weaknesses) > 0:
            for weakness in weaknesses:
                clean_weakness = str(weakness).strip()
                if clean_weakness:
                    story.append(Paragraph(f"• {clean_weakness}", bullet_style))
        else:
            story.append(Paragraph("No weaknesses identified.", body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Improvement Suggestions
        story.append(Paragraph("Improvement Suggestions", heading_style))
        suggestions = evaluation.get('improvement_suggestions', [])
        if suggestions and len(suggestions) > 0:
            for suggestion in suggestions:
                clean_suggestion = str(suggestion).strip()
                if clean_suggestion:
                    story.append(Paragraph(f"• {clean_suggestion}", bullet_style))
        else:
            story.append(Paragraph("No suggestions provided.", body_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Final Recommendation
        story.append(Paragraph("Final Recommendation", heading_style))
        story.append(Paragraph(evaluation.get('final_recommendation', 'N/A'), body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _get_score_color(self, score: int) -> colors.HexColor:
        """Get color based on score"""
        if score >= 70:
            return colors.HexColor('#27ae60')  # Green
        elif score >= 50:
            return colors.HexColor('#f39c12')  # Orange
        else:
            return colors.HexColor('#e74c3c')  # Red





