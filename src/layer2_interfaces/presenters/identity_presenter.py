"""Identity Presenter - Formats identity data for UI consumption"""

from typing import Dict, Any
from layer0_entities.identity import Identity

class IdentityPresenter:
    """Formats identity-related data for frontend consumption"""
    
    def present_identity(self, identity: Identity) -> Dict[str, Any]:
        """Present identity entity for UI"""
        return {
            'name': identity.name or '',
            'archetype': identity.archetype or '',
            'mood': identity.mood or '',
            'region': identity.region or '',
            'field': identity.field or '',
            'selfTitle': identity.self_title or '',
            'bio': identity.bio or '',
            'completion_percentage': identity.completion_percentage(),
            'is_complete': identity.is_complete()
        }
    
    def present_identity_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Present raw identity data for UI"""
        return {
            'name': raw_data.get('name', ''),
            'archetype': raw_data.get('archetype', ''),
            'mood': raw_data.get('mood', ''),
            'region': raw_data.get('region', ''),
            'field': raw_data.get('field', ''),
            'selfTitle': raw_data.get('selfTitle', ''),
            'bio': raw_data.get('bio', '')
        }
    
    def present_identity_validation(self, validation: Dict[str, Any]) -> Dict[str, Any]:
        """Present identity validation results"""
        return {
            'isValid': validation.get('is_valid', False),
            'completionPercentage': validation.get('completion_percentage', 0),
            'missingFields': validation.get('missing_fields', []),
            'suggestions': validation.get('suggestions', [])
        }