"""Simple API endpoints for Vue frontend testing"""

from flask import Blueprint, jsonify, request, session

simple_api_bp = Blueprint('simple_api', __name__, url_prefix='/api')

@simple_api_bp.route('/auth/status', methods=['GET'])
def auth_status():
    """Get current authentication status"""
    message_count = session.get('agent_interactions', 0)
    return jsonify({
        'authenticated': False,
        'user_id': None,
        'agent_interactions': message_count
    })

@simple_api_bp.route('/agent/interact', methods=['POST'])
def agent_interact():
    """Handle agent interactions with simple responses"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message required'}), 400
        
        user_message = data['message']
        
        # Track interactions
        interaction_count = session.get('agent_interactions', 0)
        session['agent_interactions'] = interaction_count + 1
        
        # Simple response logic
        responses = [
            "I understand you're interested in entrepreneurship. What specific area would you like to explore?",
            "That's a great question! Let me help you think through the steps to achieve that goal.",
            "Building a successful business requires clarity on your identity, mission, and roadmap. Which would you like to focus on first?",
            "I can see your passion coming through. How can we turn that energy into actionable next steps?",
            "Your entrepreneurial journey is unique. Let's work together to define what success looks like for you."
        ]
        
        import random
        response = random.choice(responses)
        
        return jsonify({
            'response': response,
            'interaction_count': session['agent_interactions'],
            'requires_auth': session['agent_interactions'] >= 10
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@simple_api_bp.route('/identity', methods=['GET'])
def get_identity():
    """Get identity data"""
    return jsonify({
        'name': 'Indradeva',
        'location': 'Kraków',
        'archetype': 'Visionary',
        'completion': 75
    })

@simple_api_bp.route('/mission', methods=['GET'])
def get_mission():
    """Get mission data"""
    return jsonify({
        'goal': 'Reach €1K',
        'deadline': 'Q3 2025',
        'purpose': 'Help solopreneurs build sustainable businesses',
        'completion': 60
    })

@simple_api_bp.route('/roadmap', methods=['GET'])
def get_roadmap():
    """Get roadmap data"""
    return jsonify({
        'completion': 25,
        'current_milestone': 'Market Research',
        'next_milestone': 'Product Development'
    })

@simple_api_bp.route('/roadmap/next', methods=['GET'])
def get_next_milestone():
    """Get next milestone data"""
    return jsonify({
        'milestone': 'Market Research',
        'target_value': '€1K',
        'progress': 25
    })

@simple_api_bp.route('/milestones', methods=['GET'])
def get_milestones():
    """Get milestones data"""
    return jsonify([
        {
            'id': 1,
            'title': 'Foundation Setup',
            'description': 'Complete identity discovery and define core values',
            'completed': True,
            'active': False
        },
        {
            'id': 2,
            'title': 'Mission Development', 
            'description': 'Craft purpose and vision statements',
            'completed': True,
            'active': False
        },
        {
            'id': 3,
            'title': 'Market Research',
            'description': 'Validate your idea and understand your target market',
            'completed': False,
            'active': True
        }
    ])