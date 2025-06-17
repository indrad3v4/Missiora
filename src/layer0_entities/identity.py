"""Identity Entity - Core user identity data"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Identity:
    """User identity information"""
    name: Optional[str] = None
    archetype: Optional[str] = None
    mood: Optional[str] = None
    region: Optional[str] = None
    field: Optional[str] = None
    self_title: Optional[str] = None
    bio: Optional[str] = None
    
    def completion_percentage(self) -> float:
        """Calculate completion percentage of identity fields"""
        fields = [self.name, self.archetype, self.mood, self.region, self.field, self.self_title]
        completed = sum(1 for field in fields if field and field.strip())
        return (completed / len(fields)) * 100
    
    def is_complete(self) -> bool:
        """Check if identity is sufficiently complete"""
        return self.completion_percentage() >= 80