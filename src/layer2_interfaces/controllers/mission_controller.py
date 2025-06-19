"""Mission Controller - REST API for mission management"""

from flask import Blueprint, jsonify, request

mission_bp = Blueprint('mission', __name__)

@mission_bp.route('/api/mission', methods=['GET'])
def get_mission():
    """Get user mission data"""
    mission_data = {
        "goal": "Reach €1K",
        "purpose": "Help solopreneurs build sustainable businesses",
        "completion": 60,
        "deadline": "Q3 2025",
        "statement": "To empower solopreneurs with AI-driven business intelligence and personalized guidance",
        "blocks": "Limited technical knowledge, time constraints"
    }
    return jsonify(mission_data)

@mission_bp.route('/api/mission', methods=['POST'])
def update_mission():
    """Update user mission data"""
    try:
        data = request.get_json()
        
        # Process through use case layer
        updated_mission = {
            "goal": data.get("goal", ""),
            "purpose": data.get("purpose", ""),
            "completion": 70,  # Mock calculation
            "deadline": data.get("deadline", "Q3 2025")
        }
        
        return jsonify({
            "success": True,
            "mission": updated_mission
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400