"""Mission Service Use Case - Process and validate mission data"""

from typing import Dict, Any
from layer0_entities.mission import Mission
from layer0_entities.identity import Identity

class MissionService:
    """Handles mission data processing and analysis"""
    
    def __init__(self):
        pass
    
    def process_mission_data(self, raw_data: Dict[str, Any]) -> Mission:
        """Process raw mission data into Mission entity"""
        return Mission(
            statement=raw_data.get('statement'),
            goal=raw_data.get('goal'),
            blocks=raw_data.get('blocks')
        )
    
    def validate_mission(self, mission: Mission) -> Dict[str, Any]:
        """Validate mission completeness and return analysis"""
        return {
            'is_valid': mission.is_complete(),
            'completion_percentage': mission.completion_percentage(),
            'missing_fields': self._get_missing_fields(mission),
            'suggestions': self._get_completion_suggestions(mission)
        }
    
    def align_with_identity(self, mission: Mission, identity: Identity) -> Dict[str, Any]:
        """Analyze mission alignment with identity"""
        alignment_score = self._calculate_alignment_score(mission, identity)
        return {
            'alignment_score': alignment_score,
            'is_aligned': alignment_score >= 0.7,
            'recommendations': self._get_alignment_recommendations(mission, identity)
        }
    
    def _get_missing_fields(self, mission: Mission) -> list:
        """Identify missing fields in mission"""
        fields = {
            'statement': mission.statement,
            'goal': mission.goal
        }
        return [field for field, value in fields.items() if not value or not value.strip()]
    
    def _get_completion_suggestions(self, mission: Mission) -> list:
        """Provide suggestions for completing mission"""
        missing = self._get_missing_fields(mission)
        suggestions = []
        
        if 'statement' in missing:
            suggestions.append("Define your mission statement - what drives your business purpose?")
        if 'goal' in missing:
            suggestions.append("Set a specific, measurable goal for your business")
            
        return suggestions
    
    def _calculate_alignment_score(self, mission: Mission, identity: Identity) -> float:
        """Calculate alignment score between mission and identity"""
        # Simple alignment calculation based on field consistency
        score = 0.5  # Base score
        
        if identity.field and mission.statement:
            # Check if mission mentions the identity field
            if identity.field.lower() in mission.statement.lower():
                score += 0.3
                
        if identity.region and mission.goal:
            # Check for regional considerations in goals
            if identity.region.lower() in mission.goal.lower():
                score += 0.2
                
        return min(score, 1.0)
    
    def _get_alignment_recommendations(self, mission: Mission, identity: Identity) -> list:
        """Provide recommendations for better alignment"""
        recommendations = []
        
        if identity.field and mission.statement:
            if identity.field.lower() not in mission.statement.lower():
                recommendations.append(f"Consider incorporating your {identity.field} expertise into your mission")
        
        if identity.archetype and mission.statement:
            recommendations.append(f"Ensure your mission reflects your {identity.archetype} entrepreneurial style")
            
        return recommendations