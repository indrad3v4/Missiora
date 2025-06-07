"""
Enhanced backend for context-aware orchestrator with persistent memory
"""

from flask import request, jsonify, session
from datetime import datetime
import json
from models import User, Conversation, Message
from app import app, db
from agents_sdk import get_agent_response

@app.route('/api/context-aware-chat', methods=['POST'])
def context_aware_chat():
    """Enhanced chat endpoint with full context awareness"""
    data = request.get_json()
    user_message = data.get('user_message', '')
    section = data.get('section', 'general')  # identity, mission, roadmap
    
    # Get or create user session
    user_id = session.get('user_id', 'anonymous')
    
    # Build comprehensive context from all user data
    context = build_user_context(user_id, section)
    
    # Get conversation history for this section
    history = get_section_conversation_history(user_id, section)
    
    # Call enhanced agent with full context
    try:
        response = get_agent_response(
            user_message=user_message,
            conversation_history=history,
            user_context=context,
            section=section
        )
        
        # Store conversation with context
        store_conversation_with_context(user_id, section, user_message, response, context)
        
        return jsonify({
            'reply': response.get('reply', ''),
            'agent_name': response.get('agent_name', 'Orchestrator'),
            'suggestions': response.get('suggestions', []),
            'form_updates': response.get('form_updates', {})
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Context processing failed',
            'fallback_reply': get_contextual_fallback(section, user_message)
        }), 500

def build_user_context(user_id, current_section):
    """Build comprehensive user context from all sections"""
    context = {
        'current_section': current_section,
        'timestamp': datetime.now().isoformat(),
        'identity': {},
        'mission': {},
        'milestones': [],
        'previous_interactions': []
    }
    
    try:
        # Get identity data
        identity_response = requests.get(f'/api/identity')
        if identity_response.status_code == 200:
            context['identity'] = identity_response.json()
            
        # Get mission data  
        mission_response = requests.get(f'/api/mission')
        if mission_response.status_code == 200:
            context['mission'] = mission_response.json()
            
        # Get milestone progress
        milestones_response = requests.get(f'/api/milestones')
        if milestones_response.status_code == 200:
            context['milestones'] = milestones_response.json()
            
        # Get recent conversations across all sections
        context['previous_interactions'] = get_recent_cross_section_interactions(user_id)
        
    except Exception as e:
        print(f"Context building error: {e}")
    
    return context

def get_section_conversation_history(user_id, section, limit=10):
    """Get conversation history for specific section"""
    try:
        conversations = Conversation.query.filter_by(
            user_id=user_id,
            section=section
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        history = []
        for conv in conversations:
            for msg in conv.messages:
                history.append({
                    'role': 'user' if msg.is_user else 'assistant',
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                })
        
        return history
    except Exception as e:
        print(f"History retrieval error: {e}")
        return []

def store_conversation_with_context(user_id, section, user_message, response, context):
    """Store conversation with full context for future reference"""
    try:
        # Create or get conversation for this section
        conversation = Conversation.query.filter_by(
            user_id=user_id,
            section=section,
            title=f"{section.title()} Discussion"
        ).first()
        
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                section=section,
                title=f"{section.title()} Discussion",
                context_data=json.dumps(context)
            )
            db.session.add(conversation)
            db.session.flush()
        
        # Add user message
        user_msg = Message(
            conversation_id=conversation.id,
            content=user_message,
            is_user=True,
            context_snapshot=json.dumps(context)
        )
        db.session.add(user_msg)
        
        # Add AI response
        ai_msg = Message(
            conversation_id=conversation.id,
            content=response.get('reply', ''),
            is_user=False,
            agent_name=response.get('agent_name', 'Orchestrator')
        )
        db.session.add(ai_msg)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Conversation storage error: {e}")
        db.session.rollback()

def get_contextual_fallback(section, user_message):
    """Provide contextual fallback responses"""
    fallbacks = {
        'identity': "I understand you're exploring your identity. Let me help you discover what makes you unique as an entrepreneur. What aspects of yourself do you want to express through your business?",
        'mission': "Crafting your mission is crucial. Think about the impact you want to make and how your personal values align with your business goals. What change do you want to create in the world?",
        'roadmap': "Let's focus on your next steps. Based on your identity and mission, what milestone feels most important to tackle first? I can help you break it down into actionable steps."
    }
    
    return fallbacks.get(section, "I'm here to help you on your entrepreneurial journey. What would you like to explore?")
