"""Roadmap Controller - REST API for milestone tracking"""

from flask import Blueprint, jsonify, request

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/api/roadmap', methods=['GET'])
def get_roadmap():
    """Get user roadmap data"""
    roadmap_data = {
        "completion": 25,
        "current_milestone": "Market Research",
        "next_milestone": "Product Development",
        "milestones": [
            {
                "id": 1,
                "title": "Foundation & Identity",
                "description": "Define core identity and value proposition",
                "completed": True,
                "active": False,
                "order_index": 1
            },
            {
                "id": 2,
                "title": "Market Research",
                "description": "Validate idea and understand target market",
                "completed": False,
                "active": True,
                "order_index": 2
            },
            {
                "id": 3,
                "title": "MVP Development",
                "description": "Build minimum viable product",
                "completed": False,
                "active": False,
                "order_index": 3
            }
        ]
    }
    return jsonify(roadmap_data)

@roadmap_bp.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate AI-powered roadmap"""
    try:
        # Generate 5-step roadmap using existing logic
        generated_roadmap = {
            "title": "Solopreneur Success Roadmap",
            "description": "A strategic 5-step plan to reach your business goals",
            "milestones": [
                {
                    "id": 1,
                    "title": "Foundation & Identity",
                    "description": "Define your core identity and value proposition",
                    "completed": False,
                    "active": True,
                    "order_index": 1,
                    "agent_stage": "foundation"
                },
                {
                    "id": 2,
                    "title": "Market Research",
                    "description": "Validate your idea and understand your target market",
                    "completed": False,
                    "active": False,
                    "order_index": 2,
                    "agent_stage": "research"
                },
                {
                    "id": 3,
                    "title": "MVP Development",
                    "description": "Build and test your minimum viable product",
                    "completed": False,
                    "active": False,
                    "order_index": 3,
                    "agent_stage": "development"
                },
                {
                    "id": 4,
                    "title": "Launch & Marketing",
                    "description": "Launch your product and attract first customers",
                    "completed": False,
                    "active": False,
                    "order_index": 4,
                    "agent_stage": "launch"
                },
                {
                    "id": 5,
                    "title": "Scale & Optimize",
                    "description": "Scale your business and optimize operations",
                    "completed": False,
                    "active": False,
                    "order_index": 5,
                    "agent_stage": "scale"
                }
            ]
        }
        
        return jsonify(generated_roadmap)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500