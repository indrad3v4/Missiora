"""Feedback Service - NPS Loop Implementation"""

from typing import Dict, Any, Optional
from datetime import datetime

class FeedbackService:
    """Handles NPS feedback collection and analysis"""
    
    def __init__(self):
        self.feedback_store = []  # In production, this would be a database
    
    def collect_nps_feedback(self, user_id: str, score: int, verbatim: str = "") -> Dict[str, Any]:
        """Collect NPS feedback from user"""
        if not (0 <= score <= 10):
            raise ValueError("NPS score must be between 0 and 10")
        
        feedback_entry = {
            'user_id': user_id,
            'score': score,
            'verbatim': verbatim,
            'category': self._categorize_nps_score(score),
            'timestamp': datetime.utcnow().isoformat(),
            'id': len(self.feedback_store) + 1
        }
        
        self.feedback_store.append(feedback_entry)
        return feedback_entry
    
    def get_nps_metrics(self) -> Dict[str, Any]:
        """Calculate NPS metrics"""
        if not self.feedback_store:
            return {
                'nps_score': 0,
                'total_responses': 0,
                'promoters': 0,
                'passives': 0,
                'detractors': 0
            }
        
        promoters = len([f for f in self.feedback_store if f['category'] == 'promoter'])
        passives = len([f for f in self.feedback_store if f['category'] == 'passive'])
        detractors = len([f for f in self.feedback_store if f['category'] == 'detractor'])
        total = len(self.feedback_store)
        
        nps_score = ((promoters - detractors) / total) * 100 if total > 0 else 0
        
        return {
            'nps_score': round(nps_score, 2),
            'total_responses': total,
            'promoters': promoters,
            'passives': passives,
            'detractors': detractors
        }
    
    def get_recent_feedback(self, limit: int = 10) -> list:
        """Get recent feedback entries"""
        return sorted(self.feedback_store, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def _categorize_nps_score(self, score: int) -> str:
        """Categorize NPS score into promoter/passive/detractor"""
        if score >= 9:
            return 'promoter'
        elif score >= 7:
            return 'passive'
        else:
            return 'detractor'
    
    def should_show_nps_prompt(self, user_id: str, interaction_count: int) -> bool:
        """Determine if NPS prompt should be shown"""
        # Show NPS after 5 interactions and then every 20 interactions
        if interaction_count == 5 or interaction_count % 20 == 0:
            # Check if user hasn't given feedback recently
            recent_feedback = [f for f in self.feedback_store 
                             if f['user_id'] == user_id]
            if not recent_feedback:
                return True
            
            # Don't show if they gave feedback in last session
            latest_feedback = max(recent_feedback, key=lambda x: x['timestamp'])
            return datetime.fromisoformat(latest_feedback['timestamp']).date() < datetime.utcnow().date()
        
        return False