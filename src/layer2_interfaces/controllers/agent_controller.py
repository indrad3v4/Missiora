"""Agent Controller - Handles AI agent interactions"""

from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from src.layer1_use_cases.agents_sdk import get_agent_response
from src.layer1_use_cases.session_manager import SessionManager
from src.layer2_interfaces.presenters.agent_output_presenter import AgentOutputPresenter
from src.layer3_frameworks.db.session_store import SessionStore
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

@agent_bp.route('/api/agent/interact', methods=['POST'])
@login_required_after_limit
def interact():
    """Handle agent interactions with login delay logic and session persistence"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Get user ID for session management
        user_id = current_user.id if current_user.is_authenticated else 'anonymous'
        
        # Load conversation history from session store
        conversation_history = session_store.get_conversation_history(user_id)
        
        # Get response from agent orchestrator
        response = get_agent_response(user_message, conversation_history)
        
        # Update conversation history in session store
        session_store.update_conversation_history(user_id, {
            'user': user_message,
            'agent': response.get('reply', '') if isinstance(response, dict) else str(response),
            'timestamp': str(datetime.utcnow())
        })
        
        return jsonify({
            'success': True,
            'response': response,
            'user_id': user_id,
            'interaction_count': session.get('agent_interactions', 0)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_bp.route('/api/agent/history', methods=['GET'])
@login_required
def get_history():
    """Get conversation history for authenticated user"""
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
            
        history = session_store.get_conversation_history(user_id)
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500