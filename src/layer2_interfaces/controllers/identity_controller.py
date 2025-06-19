"""Identity Controller - REST API for identity management"""

from flask import Blueprint, jsonify, request
identity_bp = Blueprint('identity', __name__)

# Optional use case service - graceful fallback if not available
try:
    from ...layer1_use_cases.identity_analysis import IdentityAnalysis
    identity_service = IdentityAnalysis()
except ImportError:
    identity_service = None

@identity_bp.route('/api/identity', methods=['GET'])
def get_identity():
    """Get user identity data"""
    # Mock data for MVP - replace with actual user service
    identity_data = {
        "name": "Indradeva",
        "archetype": "Visionary",
        "completion": 75,
        "location": "Kraków",
        "region": "Kraków",
        "mood": "Optimistic",
        "field": "Technology",
        "self_title": "AI Entrepreneur",
        "bio": "Building the future of solopreneur success"
    }
    return jsonify(identity_data)

@identity_bp.route('/api/identity', methods=['POST'])
def update_identity():
    """Update user identity data"""
    try:
        data = request.get_json()
        
        # Process through use case layer if available
        if identity_service:
            identity = identity_service.process_identity_data(data)
            validation = identity_service.validate_identity(identity)
            
            return jsonify({
                "success": True,
                "identity": {
                    "name": identity.name,
                    "archetype": identity.archetype,
                    "completion": identity.completion_percentage(),
                    "location": identity.region
                },
                "validation": validation
            })
        else:
            # Simple processing fallback
            return jsonify({
                "success": True,
                "identity": {
                    "name": data.get("name", ""),
                    "archetype": data.get("archetype", ""),
                    "completion": 75,
                    "location": data.get("region", "")
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 400