"""Milestone Entity - Individual roadmap items"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Milestone:
    """Individual milestone in a roadmap"""
    id: Optional[int] = None
    code: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    active: bool = False
    completed: bool = False
    order_index: int = 0
    created_at: Optional[datetime] = None
    agent_stage: str = 'seed'
    completion_data: Optional[str] = None
    last_agent_interaction: Optional[datetime] = None
    
    def mark_complete(self):
        """Mark milestone as completed"""
        self.completed = True
        self.active = False
    
    def activate(self):
        """Activate this milestone"""
        self.active = True
        self.completed = False