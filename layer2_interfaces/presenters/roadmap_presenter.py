"""Roadmap Presenter - Formats roadmap and milestone data for UI"""

from typing import Dict, Any, List
from layer0_entities.roadmap import Roadmap
from layer0_entities.milestone import Milestone

class RoadmapPresenter:
    """Formats roadmap-related data for frontend consumption"""
    
    def present_roadmap(self, roadmap: Roadmap) -> Dict[str, Any]:
        """Present roadmap entity for UI"""
        return {
            'title': roadmap.title or '',
            'description': roadmap.description or '',
            'milestones': [self.present_milestone(m) for m in roadmap.milestones],
            'completion_percentage': roadmap.completion_percentage(),
            'active_milestone': self.present_milestone(roadmap.get_active_milestone()) if roadmap.get_active_milestone() else None
        }
    
    def present_milestone(self, milestone: Milestone) -> Dict[str, Any]:
        """Present milestone entity for UI"""
        return {
            'id': milestone.id,
            'code': milestone.code,
            'title': milestone.title,
            'description': milestone.description,
            'active': milestone.active,
            'completed': milestone.completed,
            'order_index': milestone.order_index,
            'agent_stage': milestone.agent_stage,
            'created_at': milestone.created_at.isoformat() if milestone.created_at else None,
            'last_interaction': milestone.last_agent_interaction.isoformat() if milestone.last_agent_interaction else None
        }
    
    def present_milestones(self, milestones_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Present list of milestone data for UI"""
        return [{
            'id': m['id'],
            'code': m['code'],
            'title': m['title'],
            'description': m['description'],
            'active': m['active'],
            'completed': m['completed'],
            'order_index': m['order_index']
        } for m in milestones_data]
    
    def present_milestone_progress(self, milestone: Milestone, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Present milestone progress information"""
        return {
            'milestone': self.present_milestone(milestone),
            'progress': progress_data,
            'completion_status': 'completed' if milestone.completed else 'active' if milestone.active else 'pending'
        }