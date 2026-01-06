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
            'mind reading', 'read mind', 'read thoughts', 'read human thoughts', 'read minds',
            'reading thoughts', 'thought reading', 'decode thoughts', 'interpret thoughts',
            'telepathy', 'telepathic', 'brain reading', 'neural reading',
            'time travel', 'time machine', 'go back in time',
            'teleport', 'teleportation', 'instant travel',
            'invisible', 'invisibility', 'become invisible',
            'superpower', 'super powers', 'magic', 'magical',
            'flying human', 'fly like bird', 'levitate',
            'immortal', 'immortality', 'live forever',
            'predict future', 'see future', 'future prediction', 'predict career', 'predict financial',
            'predict life', 'predict happiness', 'predict success', 'predict outcomes',
            'future career success', 'future financial growth', 'future life happiness',
            'life predictions', 'predict life outcomes', 'know their future',
            'accurately predict', 'guaranteed predictions', 'guaranteed prediction',
            'near-perfect accuracy', 'perfect accuracy', 'predict natural disasters',
            'predict political events', 'predict stock market', 'predict crashes',
            'predict years in advance', 'years in advance', 'predict individual life',
            'predict life outcomes', 'guaranteed predictions with',
            'predict exact questions', 'predict exam questions', 'predict questions before',
            'exact question forecasts', 'guaranteed success', 'guaranteed exam success',
            'predict questions that will appear', 'predict exact exam questions',
            'forecast exam questions', 'predict questions before conducted',
            'exact question prediction', 'guaranteed question prediction',
            'guaranteed profits', 'guaranteed profit', 'guaranteed returns',
            'guaranteed income', 'guaranteed money', 'guaranteed earnings',
            'mind control', 'control minds', 'brain control',
            'memory transfer', 'transfer memories', 'upload consciousness',
            'ghost', 'spirit', 'afterlife', 'communicate with dead',
            'parallel universe', 'alternate dimension', 'multiverse travel',
            'astrology', 'astrological', 'birth chart', 'horoscope', 'zodiac',
            'fortune telling', 'fortune teller', 'crystal ball', 'palm reading',
            'quantum computing for predictions', 'blockchain for predictions',
            'predict by facial expressions', 'predict by voice tone', 'predict by social media',
            'analyze brain signals', 'brain signals', 'decode brain', 'interpret brain',
            'subconscious intent', 'read subconscious', 'access subconscious',
            'real-time thoughts', 'instant thoughts', 'live thoughts'
        ]
        
        # Mind reading specific keywords (scientifically impossible)
        self.mind_reading_keywords = [
            'read thoughts', 'read human thoughts', 'read minds', 'reading thoughts',
            'thought reading', 'decode thoughts', 'interpret thoughts', 'brain reading',
            'neural reading', 'analyze brain signals', 'brain signals', 'decode brain',
            'interpret brain', 'subconscious intent', 'read subconscious', 'access subconscious',
            'real-time thoughts', 'instant thoughts', 'live thoughts', 'mind reading device',
            'thought reading device', 'brain reading device'
        ]
        
        # Pseudoscience and impossible prediction methods
        self.pseudoscience_keywords = [
            'astrology', 'astrological', 'birth chart', 'horoscope', 'zodiac sign',
            'fortune telling', 'palm reading', 'tarot', 'crystal ball',
            'predict future', 'predict life', 'predict career', 'predict financial',
            'predict happiness', 'predict success', 'life predictions',
            'know their future', 'future outcomes', 'future prediction'
        ]
        
        # Unethical behavior indicators (cheating, manipulation, etc.)
        self.unethical_keywords = [
            'cheating', 'cheat', 'manipulate', 'manipulation', 'bypass',
            'circumvent', 'exploit', 'hack exam', 'exam cheating',
            'academic dishonesty', 'fraud', 'scam', 'deceive',
            'guaranteed profits', 'guaranteed profit', 'guaranteed returns',
            'guaranteed income', 'guaranteed money', 'guaranteed earnings'
        ]
        
        # Technology misuse indicators (using advanced tech for impossible tasks)
        self.tech_misuse_keywords = [
            'quantum computing for predictions', 'quantum computing to predict',
            'blockchain for predictions', 'blockchain to predict',
            'deep learning to predict future', 'ai to predict life outcomes',
            'predict future using', 'predict life using', 'predict career using',
            'ai to read thoughts', 'ai to read minds', 'deep learning to read thoughts',
            'neural network to read thoughts', 'machine learning to read thoughts'
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
            'innovative', 'unique', 'scalable', 'feasible', 'low risk',
            'proven', 'established', 'standard', 'straightforward', 'achievable'
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
            'dream reading', 'mind reading', 'read thoughts', 'read minds', 'brain reading',
            'brain interface', 'telepathy', 'decode thoughts', 'interpret thoughts',
            'analyze brain signals', 'brain signals', 'subconscious intent',
            'time travel', 'teleportation', 'magic', 'supernatural',
            'predict future', 'predict life', 'predict career', 'predict financial',
            'predict happiness', 'predict success', 'life predictions',
            'future prediction', 'predict outcomes', 'know their future',
            'astrology', 'astrological', 'horoscope', 'fortune telling',
            'quantum computing for predictions', 'blockchain for predictions',
            'predict by facial expressions', 'predict by voice tone',
            'predict exact questions', 'predict exam questions', 'predict questions before',
            'exact question forecasts', 'guaranteed success', 'guaranteed exam success',
            'predict questions that will appear', 'predict exact exam questions',
            'forecast exam questions', 'guaranteed question prediction'
        ]
        
        if any(keyword in tech_lower for keyword in impossible_keywords):
            tech_score = max(0, min(15, tech_score - 60))  # Cap at 15 for impossible ideas
        
        # HIGHLY FEASIBLE: Standard tech stack indicators (mobile/web apps, APIs, databases)
        elif any(word in tech_lower for word in [
            'mobile app', 'web app', 'web application', 'mobile application',
            'standard technology', 'proven technology', 'existing technology',
            'well-established', 'common', 'readily available', 'straightforward',
            'standard stack', 'mature technology', 'widely used', 'off-the-shelf',
            'rest api', 'database', 'cloud services', 'saas', 'crud',
            'cloud-based', 'subscription service', 'management system', 'platform',
            'attendance system', 'leave management', 'hr system', 'payroll integration'
        ]):
            tech_score = min(100, tech_score + 30)  # Increased boost for standard tech (was 25)
        
        # Positive indicators
        elif any(word in tech_lower for word in ['feasible', 'proven', 'existing', 'standard', 'available', 'current technology']):
            tech_score = min(100, tech_score + 15)  # Increased from 10
        # Moderate difficulty
        elif any(word in tech_lower for word in ['complex', 'experimental', 'unproven', 'cutting-edge', 'challenging']):
            tech_score = max(0, tech_score - 15)
        # Very difficult
        elif any(word in tech_lower for word in ['very difficult', 'breakthrough', 'research needed', 'not yet available']):
            tech_score = max(0, tech_score - 30)
        
        return tech_score
    
    def _score_innovation_level(self, evaluation: Dict) -> int:
        """Score based on innovation and uniqueness
        NOTE: Competition does NOT reduce feasibility - only affects differentiation
        """
        innovation_text = evaluation.get('innovation_uniqueness', '')
        if not innovation_text:
            return 50  # Neutral - competition doesn't reduce feasibility
        
        innovation_score = self._extract_score_from_text(innovation_text)
        
        # Check for uniqueness indicators (bonus, but not required)
        innovation_lower = innovation_text.lower()
        if any(word in innovation_lower for word in ['unique', 'novel', 'innovative', 'differentiated', 'first-mover']):
            innovation_score = min(100, innovation_score + 10)  # Reduced from 15
        # DO NOT penalize for competition - it doesn't reduce feasibility
        # elif any(word in innovation_lower for word in ['saturated', 'competitive', 'similar', 'existing']):
        #     innovation_score = max(0, innovation_score - 15)  # REMOVED - competition doesn't reduce feasibility
        
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
        market_text = evaluation.get('market_potential', '').lower()
        
        # Check for impossible keywords in the idea itself
        if any(keyword in idea_lower for keyword in self.impossible_keywords):
            return True
        
        # Check for mind reading keywords (scientifically impossible)
        if any(keyword in idea_lower for keyword in self.mind_reading_keywords):
            return True
        
        # Check for pseudoscience keywords (astrology, fortune telling, future prediction)
        if any(keyword in idea_lower for keyword in self.pseudoscience_keywords):
            return True
        
        # Check for technology misuse (using quantum/blockchain for predictions)
        if any(keyword in idea_lower for keyword in self.tech_misuse_keywords):
            return True
        
        # Check for future prediction concepts (impossible)
        prediction_phrases = [
            'predict future', 'predict life', 'predict career success',
            'predict financial growth', 'predict life happiness', 'predict outcomes',
            'know their future', 'future predictions', 'life predictions',
            'accurately predict', 'guaranteed predictions', 'guaranteed prediction',
            'near-perfect accuracy', 'perfect accuracy', 'predict natural disasters',
            'predict political events', 'predict stock market', 'predict crashes',
            'predict years in advance', 'years in advance', 'predict individual life',
            'predict individual life outcomes', 'guaranteed predictions with',
            'predict exact questions', 'predict exam questions', 'predict questions before',
            'exact question forecasts', 'guaranteed success', 'guaranteed exam success',
            'predict questions that will appear', 'predict exact exam questions',
            'forecast exam questions', 'predict questions before conducted',
            'exact question prediction', 'guaranteed question prediction',
            'guaranteed success', 'guaranteed forecasts', 'exact forecasts'
        ]
        if any(phrase in idea_lower for phrase in prediction_phrases):
            return True
        
        # Check evaluation text for impossibility indicators
        impossible_indicators = [
            'impossible', 'does not exist', 'not possible', 'cannot be done',
            'science fiction', 'not feasible', 'unrealistic', 'no technology exists',
            'requires technology that does not exist', 'beyond current science',
            'not yet invented', 'not available', 'does not exist yet',
            'theoretical only', 'not proven', 'no scientific basis',
            'cannot predict future', 'future cannot be predicted', 'pseudoscience',
            'not scientifically valid', 'no evidence', 'unproven claims',
            'cannot read thoughts', 'cannot read minds', 'thought reading impossible',
            'mind reading impossible', 'brain reading not possible', 'scientifically impossible',
            'not feasible with current technology', 'requires breakthrough'
        ]
        
        combined_text = tech_text + ' ' + risks_text + ' ' + market_text
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
        # FIRST: Check if idea is impossible or unethical - if so, return very low score
        idea_lower = idea_text.lower() if idea_text else ''
        
        # Check for unethical behavior (cheating, manipulation, etc.)
        is_unethical = any(keyword in idea_lower for keyword in self.unethical_keywords)
        if is_unethical:
            return 15  # Unethical ideas score 10-35 range
        
        if idea_text and self._check_impossible_idea(idea_text, evaluation):
            # Force impossible ideas to score 10-35 (very low)
            # Check specific types of impossibility
            prediction_keywords_extended = [
                'predict future', 'predict life', 'predict career', 'predict financial',
                'accurately predict', 'guaranteed predictions', 'guaranteed prediction',
                'near-perfect accuracy', 'perfect accuracy', 'predict natural disasters',
                'predict political events', 'predict stock market', 'predict crashes',
                'predict years in advance', 'years in advance', 'predict individual life',
                'predict exact questions', 'predict exam questions', 'predict questions before',
                'exact question forecasts', 'guaranteed success', 'guaranteed exam success',
                'predict questions that will appear', 'predict exact exam questions',
                'forecast exam questions', 'predict questions before conducted',
                'exact question prediction', 'guaranteed question prediction',
                'guaranteed forecasts', 'exact forecasts', 'guaranteed profits',
                'guaranteed profit', 'guaranteed returns'
            ]
            if any(keyword in idea_lower for keyword in self.mind_reading_keywords):
                return 15  # Mind reading = 15-20 range (scientifically impossible)
            elif any(keyword in idea_lower for keyword in self.pseudoscience_keywords + prediction_keywords_extended):
                return 10  # Pseudoscience/prediction = very low score (10)
            return 10  # Other impossible ideas
        
        # Calculate individual component scores
        scores = {
            'problem_clarity': self._score_problem_clarity(evaluation),
            'market_demand': self._score_market_demand(evaluation),
            'technical_feasibility': self._score_technical_feasibility(evaluation),
            'innovation_level': self._score_innovation_level(evaluation),
            'scalability': self._score_scalability(evaluation),
            'risk_level': self._score_risk_level(evaluation)
        }
        
        # Check for proven/standard business models in idea text
        idea_lower = idea_text.lower() if idea_text else ''
        proven_models = [
            'budget', 'expense', 'tracking', 'finance', 'payment', 'wallet',
            'e-commerce', 'marketplace', 'booking', 'reservation', 'delivery',
            'social media', 'messaging', 'chat', 'blog', 'content', 'learning',
            'education', 'fitness', 'health', 'food', 'restaurant', 'shopping',
            'attendance', 'leave management', 'hr system', 'human resources',
            'employee management', 'payroll', 'time tracking', 'scheduling',
            'crm', 'project management', 'task management', 'inventory',
            'pos system', 'accounting software', 'billing', 'invoicing',
            'saas', 'subscription service', 'cloud-based', 'web application',
            'mobile app', 'management system', 'platform'
        ]
        
        # Boost for proven business models using standard tech
        is_proven_model = any(model in idea_lower for model in proven_models)
        tech_score = scores['technical_feasibility']
        
        # Check for violations (scientific, ethical, legal)
        prediction_keywords = [
            'predict future', 'predict life', 'predict career', 'predict financial', 
            'predict happiness', 'predict success', 'predict outcomes',
            'accurately predict', 'guaranteed predictions', 'guaranteed prediction',
            'near-perfect accuracy', 'perfect accuracy', 'predict natural disasters',
            'predict political events', 'predict stock market', 'predict crashes',
            'predict years in advance', 'years in advance', 'predict individual life',
            'predict life outcomes', 'guaranteed predictions with',
            'predict exact questions', 'predict exam questions', 'predict questions before',
            'exact question forecasts', 'guaranteed success', 'guaranteed exam success',
            'predict questions that will appear', 'predict exact exam questions',
            'forecast exam questions', 'predict questions before conducted',
            'exact question prediction', 'guaranteed question prediction',
            'guaranteed forecasts', 'exact forecasts', 'guaranteed profits',
            'guaranteed profit', 'guaranteed returns'
        ]
        is_pseudoscience = any(keyword in idea_lower for keyword in self.pseudoscience_keywords + prediction_keywords)
        is_tech_misuse = any(keyword in idea_lower for keyword in self.tech_misuse_keywords)
        is_mind_reading = any(keyword in idea_lower for keyword in self.mind_reading_keywords)
        is_unethical = any(keyword in idea_lower for keyword in self.unethical_keywords)
        
        # Check evaluation text for violation indicators
        risks_text = evaluation.get('risks_challenges', '').lower()
        tech_text = evaluation.get('technical_feasibility', '').lower()
        has_ethical_risk = any(word in (risks_text + tech_text) for word in [
            'ethical', 'legal risk', 'regulatory', 'unethical', 'cheating',
            'manipulation', 'fraud', 'illegal', 'violates', 'prohibited'
        ])
        
        # CRITICAL: If violates scientific, ethical, or legal constraints, cap at 40
        has_violation = is_pseudoscience or is_tech_misuse or is_mind_reading or is_unethical or has_ethical_risk
        
        if has_violation:
            # Cap score below 40 for violations
            max_possible = 35  # Hard cap for violations (below 40)
            weighted_score = sum(
                scores[factor] * self.weights[factor]
                for factor in self.weights
            )
            final_score = min(weighted_score, max_possible)
        elif tech_score < 25:
            # Very low technical feasibility
            max_possible = 10 + (tech_score * 0.2)  # Max 10-15 for impossible ideas
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
            
            # BONUS: If it's a proven model with high tech feasibility, boost score
            # But only if it meets HIGH FEASIBILITY criteria (real problem, clear target, proven tech, 6-12 month MVP)
            if is_proven_model and tech_score >= 70:
                # Proven business model + high tech feasibility = strong idea (SaaS, cloud-based, etc.)
                # Check if it has clear target and real problem
                problem_text = evaluation.get('problem_statement', '').lower()
                target_text = evaluation.get('target_users', '').lower()
                has_clear_target = len(target_text) > 20 and any(word in target_text for word in ['target', 'customer', 'user', 'business', 'company', 'student', 'employee'])
                has_real_problem = len(problem_text) > 30 and any(word in problem_text for word in ['problem', 'issue', 'pain', 'need', 'challenge', 'difficulty'])
                
                if has_clear_target and has_real_problem:
                    final_score = min(95, final_score + 20)  # Cap at 95 for high feasibility
                else:
                    final_score = min(100, final_score + 15)
            elif is_proven_model and tech_score >= 50:
                # Proven model with moderate tech = still good
                final_score = min(100, final_score + 15)
            elif is_proven_model:
                # Even if tech score is lower, proven models get a boost
                final_score = min(100, final_score + 10)
        
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

