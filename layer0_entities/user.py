"""User Entity - User account and profile"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .identity import Identity
from .mission import Mission

@dataclass
class User:
    """User account and profile information"""
    id: Optional[int] = None
    username: str = ""
    email: Optional[str] = None
    ethereum_address: Optional[str] = None
    created_at: Optional[datetime] = None
    auth_type: str = 'traditional'
    replit_user_id: Optional[str] = None
    
    # Profile information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    business_name: Optional[str] = None
    business_description: Optional[str] = None
    
    # Domain data
    identity: Optional[Identity] = None
    mission: Optional[Mission] = None
    
    def get_display_name(self) -> str:
        """Get display name for the user"""
        if self.identity and self.identity.name:
            return self.identity.name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_profile_complete(self) -> bool:
        """Check if user profile is sufficiently complete"""
        return bool(self.identity and self.identity.is_complete() and 
                   self.mission and self.mission.is_complete())