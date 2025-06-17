"""Identity Analysis Use Case - Process and validate identity data"""

from typing import Dict, Any, Optional
from layer0_entities.identity import Identity

class IdentityAnalysis:
    """Handles identity data processing and analysis"""
    
    def __init__(self):
        pass
    
    def process_identity_data(self, raw_data: Dict[str, Any]) -> Identity:
        """Process raw identity data into Identity entity"""
        return Identity(
            name=raw_data.get('name'),
            archetype=raw_data.get('archetype'),
            mood=raw_data.get('mood'),
            region=raw_data.get('region'),
            field=raw_data.get('field'),
            self_title=raw_data.get('selfTitle'),
            bio=raw_data.get('bio')
        )
    
    def validate_identity(self, identity: Identity) -> Dict[str, Any]:
        """Validate identity completeness and return analysis"""
        return {
            'is_valid': identity.is_complete(),
            'completion_percentage': identity.completion_percentage(),
            'missing_fields': self._get_missing_fields(identity),
            'suggestions': self._get_completion_suggestions(identity)
        }
    
    def _get_missing_fields(self, identity: Identity) -> list:
        """Identify missing fields in identity"""
        fields = {
            'name': identity.name,
            'archetype': identity.archetype,
            'mood': identity.mood,
            'region': identity.region,
            'field': identity.field,
            'self_title': identity.self_title
        }
        return [field for field, value in fields.items() if not value or not value.strip()]
    
    def _get_completion_suggestions(self, identity: Identity) -> list:
        """Provide suggestions for completing identity"""
        missing = self._get_missing_fields(identity)
        suggestions = []
        
        if 'name' in missing:
            suggestions.append("Add your name to personalize your experience")
        if 'archetype' in missing:
            suggestions.append("Choose an archetype that represents your entrepreneurial style")
        if 'region' in missing:
            suggestions.append("Specify your location for localized business insights")
        if 'field' in missing:
            suggestions.append("Define your business field or industry")
            
        return suggestions