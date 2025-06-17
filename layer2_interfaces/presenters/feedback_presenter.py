"""Feedback Presenter - Formats NPS feedback responses"""

from typing import Dict, Any

class FeedbackPresenter:
    """Presents feedback data in the required format"""
    
    def present_nps_submission(self, feedback_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Present NPS submission response"""
        return {
            'success': True,
            'score': feedback_entry['score'],
            'verbatim': feedback_entry['verbatim'],
            'category': feedback_entry['category'],
            'message': self._get_thank_you_message(feedback_entry['category'])
        }
    
    def present_nps_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Present NPS metrics in formatted way"""
        return {
            'nps_score': metrics['nps_score'],
            'total_responses': metrics['total_responses'],
            'breakdown': {
                'promoters': metrics['promoters'],
                'passives': metrics['passives'],
                'detractors': metrics['detractors']
            },
            'interpretation': self._interpret_nps_score(metrics['nps_score'])
        }
    
    def _get_thank_you_message(self, category: str) -> str:
        """Get appropriate thank you message based on NPS category"""
        messages = {
            'promoter': "Thank you for your positive feedback! We're thrilled you're enjoying Missiora.",
            'passive': "Thank you for your feedback. We're always working to improve your experience.",
            'detractor': "Thank you for your honest feedback. We take your concerns seriously and will work to improve."
        }
        return messages.get(category, "Thank you for your feedback!")
    
    def _interpret_nps_score(self, score: float) -> str:
        """Interpret NPS score"""
        if score >= 70:
            return "Excellent"
        elif score >= 50:
            return "Good"
        elif score >= 30:
            return "Acceptable"
        elif score >= 0:
            return "Needs Improvement"
        else:
            return "Critical"