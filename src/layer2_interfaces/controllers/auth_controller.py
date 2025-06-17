"""Authentication controller with login delay logic"""

from functools import wraps
from flask import Blueprint, request, session, jsonify
from flask_login import login_required as flask_login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def login_required(f):
    """Custom login decorator that allows 10 free agent interactions before requiring auth"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if this is an agent interaction endpoint
        if request.endpoint == 'agent.interact':
            # Get or initialize interaction count for this session
            interaction_count = session.get('agent_interactions', 0)
            
            if interaction_count < 10:
                # Allow free access for first 10 interactions
                session['agent_interactions'] = interaction_count + 1
                return f(*args, **kwargs)
            else:
                # Require authentication after 10 interactions
                if not current_user.is_authenticated:
                    return jsonify({'error': 'Authentication required after 10 free interactions'}), 401
        
        # For all other endpoints, use standard login requirement
        return flask_login_required(f)(*args, **kwargs)
    
    return decorated_function

@auth_bp.route('/status')
def auth_status():
    """Check authentication status"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user_id': current_user.id if current_user.is_authenticated else None,
        'agent_interactions': session.get('agent_interactions', 0)
    })