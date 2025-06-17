"""Agent Controller - Handles AI agent interactions"""

from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from layer1_use_cases.agents_sdk import get_agent_response
from layer1_use_cases.session_manager import SessionManager
from layer2_interfaces.presenters.agent_output_presenter import AgentOutputPresenter
from layer3_frameworks.db.session_store import SessionStore
from datetime import datetime

agent_bp = Blueprint('agent', __name__)

# Initialize services
session_manager = SessionManager()
agent_presenter = AgentOutputPresenter()
session_store = SessionStore()

def login_required_after_limit(f):
    """Custom decorator allowing 10 free interactions before requiring auth"""
    def decorated_function(*args, **kwargs):
        interaction_count = session.get('agent_interactions', 0)
        
        if interaction_count < 10:
            session['agent_interactions'] = interaction_count + 1
            return f(*args, **kwargs)
        else:
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required after 10 free interactions'}), 401
            return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@agent_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chat requests for mission building"""
    data = request.get_json()
    user_message = data.get('user_message', '')
    
    try:
        # Get or create session
        session_id = f"user_{current_user.id}"
        conversation_context = session_manager.get_conversation_context(session_id)
        
        # Get agent response
        response = get_agent_response(user_message, conversation_context)
        
        # Update session with conversation context
        if 'conversation_history' in response:
            session_manager.store_conversation_context(session_id, {
                'history': response['conversation_history']
            })
        
        # Present response
        presented_response = agent_presenter.present_agent_response(response)
        
        return jsonify(presented_response)
        
    except Exception as e:
        # Fallback response
        fallback_response = {
            'reply': 'I understand your perspective. Could you tell me more about what success looks like for you?',
            'agent': 'orchestrator'
        }
        return jsonify(agent_presenter.present_agent_response(fallback_response))

@agent_bp.route('/public/chat', methods=['POST'])
def public_chat():
    """API endpoint for public chat without authentication"""
    data = request.get_json()
    user_message = data.get('user_message', '')
    message_history = data.get('message_history', [])
    
    try:
        # Get agent response
        response = get_agent_response(user_message, message_history)
        
        # Present response
        presented_response = agent_presenter.present_agent_response(response)
        
        return jsonify(presented_response)
        
    except Exception as e:
        # Fallback response
        fallback_response = {
            'reply': 'I understand. Tell me more about your entrepreneurial journey.',
            'agent': 'orchestrator'
        }
        return jsonify(agent_presenter.present_agent_response(fallback_response))