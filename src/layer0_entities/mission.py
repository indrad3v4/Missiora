"""Mission Entity - User's mission and goals"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Mission:
    """User mission statement and goals"""
    statement: Optional[str] = None
    goal: Optional[str] = None
    blocks: Optional[str] = None
    
    def completion_percentage(self) -> float:
        """Calculate completion percentage of mission fields"""
        fields = [self.statement, self.goal]
        completed = sum(1 for field in fields if field and field.strip())
        return (completed / len(fields)) * 100
    
    def is_complete(self) -> bool:
        """Check if mission is sufficiently complete"""
        return self.completion_percentage() >= 75