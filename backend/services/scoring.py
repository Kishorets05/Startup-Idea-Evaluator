"""
Scoring Service - Calculates feasibility score using weighted factors
"""

import re
from typing import Dict


class ScoringService:
    """Service for calculating feasibility scores"""
    
    def __init__(self):
        # Weight configuration
        self.weights = {
            'problem_clarity': 0.20,      # 20%
            'market_demand': 0.25,        # 25%
            'technical_feasibility': 0.20, # 20%
            'innovation_level': 0.15,     # 15%
            'scalability': 0.10,           # 10%
            'risk_level': 0.10            # 10%
        }
        
        # Keywords that indicate impossible/unrealistic ideas
        self.impossible_keywords = [
            'dream', 'dreams', 'dreaming', 'convert dreams', 'dream reading', 'read dreams',
            'mind reading', 'read mind', 'telepathy', 'telepathic',
            'time travel', 'time machine', 'go back in time',
            'teleport', 'teleportation', 'instant travel',
            'invisible', 'invisibility', 'become invisible',
            'superpower', 'super powers', 'magic', 'magical',
            'flying human', 'fly like bird', 'levitate',
            'immortal', 'immortality', 'live forever',
            'predict future', 'see future', 'future prediction',
            'mind control', 'control minds', 'brain control',
            'memory transfer', 'transfer memories', 'upload consciousness',
            'ghost', 'spirit', 'afterlife', 'communicate with dead',
            'parallel universe', 'alternate dimension', 'multiverse travel'
        ]
    
    def _extract_score_from_text(self, text: str) -> int:
        """
        Extracts numeric score from text using keyword analysis
        Returns a score between 0-100
        """
        text_lower = text.lower()
        
        # Positive indicators
        positive_keywords = [
            'strong', 'excellent', 'high', 'significant', 'clear', 'viable',
            'promising', 'substantial', 'robust', 'well-defined', 'large',
            'innovative', 'unique', 'scalable', 'feasible', 'low risk'
        ]
        
        # Negative indicators
        negative_keywords = [
            'weak', 'poor', 'low', 'limited', 'unclear', 'risky',
            'challenging', 'small', 'saturated', 'difficult', 'high risk',
            'uncertain', 'vague', 'unproven', 'niche'
        ]
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
        
        # Base score
        base_score = 50
        
        # Adjust based on keywords
        score = base_score + (positive_count * 10) - (negative_count * 10)
        
        # Clamp between 0-100
        return max(0, min(100, score))
    
    def _score_problem_clarity(self, evaluation: Dict) -> int:
        """Score based on problem statement clarity"""
        problem_text = evaluation.get('problem_statement', '')
        if not problem_text:
            return 30
        
        # Check for clarity indicators
        clarity_score = self._extract_score_from_text(problem_text)
        
        # Bonus for specific problem description
        if len(problem_text) > 50 and any(word in problem_text.lower() for word in ['problem', 'issue', 'pain', 'need']):
            clarity_score = min(100, clarity_score + 10)
        
        return clarity_score
    
    def _score_market_demand(self, evaluation: Dict) -> int:
        """Score based on market potential"""
        market_text = evaluation.get('market_potential', '')
        if not market_text:
            return 30
        
        market_score = self._extract_score_from_text(market_text)
        
        # Check for market size indicators
        market_lower = market_text.lower()
        if any(word in market_lower for word in ['large', 'growing', 'billion', 'million', 'expanding']):
            market_score = min(100, market_score + 15)
        
        return market_score
    
    def _score_technical_feasibility(self, evaluation: Dict) -> int:
        """Score based on technical feasibility - be strict about impossible ideas"""
        tech_text = evaluation.get('technical_feasibility', '')
        if not tech_text:
            return 50  # Neutral if not specified
        
        tech_score = self._extract_score_from_text(tech_text)
        
        # Check for feasibility indicators
        tech_lower = tech_text.lower()
        
        # STRICT: Penalize impossible/unrealistic ideas heavily
        impossible_keywords = [
            'impossible', 'does not exist', 'not possible', 'cannot be done',
            'science fiction', 'not feasible', 'unrealistic', 'no technology',
            'requires technology that', 'beyond current', 'not yet invented',
            'dream reading', 'mind reading', 'brain interface', 'telepathy',
            'time travel', 'teleportation', 'magic', 'supernatural'
        ]
        
        if any(keyword in tech_lower for keyword in impossible_keywords):
            tech_score = max(0, min(20, tech_score - 50))  # Cap at 20 for impossible ideas
        
        # Positive indicators
        elif any(word in tech_lower for word in ['feasible', 'proven', 'existing', 'standard', 'available', 'current technology']):
            tech_score = min(100, tech_score + 10)
        # Moderate difficulty
        elif any(word in tech_lower for word in ['complex', 'experimental', 'unproven', 'cutting-edge', 'challenging']):
            tech_score = max(0, tech_score - 15)
        # Very difficult
        elif any(word in tech_lower for word in ['very difficult', 'breakthrough', 'research needed', 'not yet available']):
            tech_score = max(0, tech_score - 30)
        
        return tech_score
    
    def _score_innovation_level(self, evaluation: Dict) -> int:
        """Score based on innovation and uniqueness"""
        innovation_text = evaluation.get('innovation_uniqueness', '')
        if not innovation_text:
            return 40
        
        innovation_score = self._extract_score_from_text(innovation_text)
        
        # Check for uniqueness indicators
        innovation_lower = innovation_text.lower()
        if any(word in innovation_lower for word in ['unique', 'novel', 'innovative', 'differentiated', 'first-mover']):
            innovation_score = min(100, innovation_score + 15)
        elif any(word in innovation_lower for word in ['saturated', 'competitive', 'similar', 'existing']):
            innovation_score = max(0, innovation_score - 15)
        
        return innovation_score
    
    def _score_scalability(self, evaluation: Dict) -> int:
        """Score based on scalability potential"""
        # Analyze strengths and market potential for scalability
        strengths = evaluation.get('strengths', [])
        market_text = evaluation.get('market_potential', '')
        
        # Ensure strengths is a list
        if not isinstance(strengths, list):
            strengths = [str(strengths)] if strengths else []
        # Ensure market_text is a string
        if not isinstance(market_text, str):
            market_text = str(market_text) if market_text else ''
        
        # Convert list items to strings
        strengths_str = ' '.join(str(s) for s in strengths)
        combined_text = strengths_str + ' ' + market_text
        scalability_score = self._extract_score_from_text(combined_text)
        
        # Check for scalability indicators
        combined_lower = combined_text.lower()
        if any(word in combined_lower for word in ['scalable', 'expandable', 'replicable', 'growth', 'network effect']):
            scalability_score = min(100, scalability_score + 15)
        
        return scalability_score
    
    def _score_risk_level(self, evaluation: Dict) -> int:
        """Score based on risks (inverse - lower risk = higher score)"""
        risks_text = evaluation.get('risks_challenges', '')
        weaknesses = evaluation.get('weaknesses', [])
        
        # Ensure risks_text is a string
        if not isinstance(risks_text, str):
            risks_text = str(risks_text) if risks_text else ''
        # Ensure weaknesses is a list
        if not isinstance(weaknesses, list):
            weaknesses = [str(weaknesses)] if weaknesses else []
        
        # Convert list items to strings
        weaknesses_str = ' '.join(str(w) for w in weaknesses)
        combined_text = risks_text + ' ' + weaknesses_str
        risk_score = 100 - self._extract_score_from_text(combined_text)  # Invert
        
        # Check for high-risk indicators
        combined_lower = combined_text.lower()
        if any(word in combined_lower for word in ['high risk', 'uncertain', 'regulatory', 'legal', 'competition']):
            risk_score = max(0, risk_score - 20)
        
        return max(0, min(100, risk_score))
    
    def _check_impossible_idea(self, idea_text: str, evaluation: Dict) -> bool:
        """
        Check if the idea is technically impossible based on keywords and evaluation
        Returns True if the idea is impossible
        """
        idea_lower = idea_text.lower()
        tech_text = evaluation.get('technical_feasibility', '').lower()
        risks_text = evaluation.get('risks_challenges', '').lower()
        
        # Check for impossible keywords in the idea itself
        if any(keyword in idea_lower for keyword in self.impossible_keywords):
            return True
        
        # Check evaluation text for impossibility indicators
        impossible_indicators = [
            'impossible', 'does not exist', 'not possible', 'cannot be done',
            'science fiction', 'not feasible', 'unrealistic', 'no technology exists',
            'requires technology that does not exist', 'beyond current science',
            'not yet invented', 'not available', 'does not exist yet',
            'theoretical only', 'not proven', 'no scientific basis'
        ]
        
        combined_text = tech_text + ' ' + risks_text
        if any(indicator in combined_text for indicator in impossible_indicators):
            return True
        
        return False
    
    def calculate_score(self, evaluation: Dict, idea_text: str = '') -> int:
        """
        Calculate weighted feasibility score
        
        Args:
            evaluation: Dictionary containing evaluation results
            idea_text: Original idea text (optional, for impossible idea detection)
            
        Returns:
            int: Feasibility score (0-100)
        """
        # FIRST: Check if idea is impossible - if so, return very low score
        if idea_text and self._check_impossible_idea(idea_text, evaluation):
            # Force impossible ideas to score 5-10
            return 5
        
        # Calculate individual component scores
        scores = {
            'problem_clarity': self._score_problem_clarity(evaluation),
            'market_demand': self._score_market_demand(evaluation),
            'technical_feasibility': self._score_technical_feasibility(evaluation),
            'innovation_level': self._score_innovation_level(evaluation),
            'scalability': self._score_scalability(evaluation),
            'risk_level': self._score_risk_level(evaluation)
        }
        
        # CRITICAL: If technical feasibility is very low, cap the overall score
        tech_score = scores['technical_feasibility']
        if tech_score < 25:
            # If technically impossible/very difficult, cap overall score severely
            max_possible = 10 + (tech_score * 0.2)  # Max 10-15 for impossible ideas
            # Still calculate weighted average but cap it
            weighted_score = sum(
                scores[factor] * self.weights[factor]
                for factor in self.weights
            )
            final_score = min(weighted_score, max_possible)
        else:
            # Normal calculation for feasible ideas
            weighted_score = sum(
                scores[factor] * self.weights[factor]
                for factor in self.weights
            )
            final_score = weighted_score
        
        # Round to integer
        final_score = int(round(final_score))
        
        # Ensure score is within bounds
        return max(0, min(100, final_score))
    
    def get_component_scores(self, evaluation: Dict, idea_text: str = '') -> Dict:
        """
        Get individual component scores for visualization
        
        Returns:
            dict: Component scores for charting
        """
        return {
            'problem_clarity': self._score_problem_clarity(evaluation),
            'market_demand': self._score_market_demand(evaluation),
            'technical_feasibility': self._score_technical_feasibility(evaluation),
            'innovation_level': self._score_innovation_level(evaluation),
            'scalability': self._score_scalability(evaluation),
            'risk_level': self._score_risk_level(evaluation)
        }

