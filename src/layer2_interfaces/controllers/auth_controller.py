"""Auth Controller - Handles authentication status and user management"""

from flask import Blueprint, jsonify, session
from flask_login import current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Get current authentication status"""
    try:
        # Get message count from session
        message_count = session.get('agent_interactions', 0)
        
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'user_id': current_user.id,
                'username': current_user.username,
                'agent_interactions': message_count
            })
        else:
            return jsonify({
                'authenticated': False,
                'user_id': None,
                'agent_interactions': message_count
            })
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'user_id': None,
            'agent_interactions': 0,
            'error': str(e)
        }), 500