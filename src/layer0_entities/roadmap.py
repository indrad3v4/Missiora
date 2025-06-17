"""Roadmap Entity - Collection of milestones"""

from dataclasses import dataclass, field
from typing import List, Optional
from .milestone import Milestone

@dataclass
class Roadmap:
    """User's roadmap composed of milestones"""
    title: Optional[str] = None
    description: Optional[str] = None
    milestones: List[Milestone] = field(default_factory=list)
    

    
    def completion_percentage(self) -> float:
        """Calculate completion percentage of roadmap"""
        if not self.milestones:
            return 0
        
        completed_milestones = sum(1 for m in self.milestones if m.completed)
        return (completed_milestones / len(self.milestones)) * 100
    
    def add_milestone(self, milestone: Milestone):
        """Add a milestone to the roadmap"""
        self.milestones.append(milestone)
    
    def get_active_milestone(self) -> Optional[Milestone]:
        """Get the currently active milestone"""
        for milestone in self.milestones:
            if milestone.active and not milestone.completed:
                return milestone
        return None
    
    def activate_next_milestone(self):
        """Activate the next milestone in sequence"""
        for milestone in sorted(self.milestones, key=lambda m: m.order_index):
            if not milestone.completed and not milestone.active:
                milestone.activate()
                break