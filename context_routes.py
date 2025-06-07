"""
Context-aware orchestrator routes for persistent memory across all sections
"""

from datetime import datetime
from flask import request, jsonify, session
from models import Conversation, Message, ContextSession
from app import app, db
from agent_service import get_agent_response
import json

@app.route('/api/context-aware-chat', methods=['POST'])
def context_aware_chat():
    """Enhanced chat endpoint with full context awareness across all sections"""
    try:
        data = request.get_json()
        user_message = data.get('user_message', '')
        section = data.get('section', 'general')  # identity, mission, roadmap
        current_data = data.get('current_data', {})
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create user session ID
        user_id = session.get('user_id', f'anonymous_{hash(request.remote_addr) % 10000}')
        session['user_id'] = user_id
        
        # Build comprehensive context from all user data
        context = build_user_context(user_id, section, current_data)
        
        # Get conversation history for this section
        history = get_section_conversation_history(user_id, section)
        
        # Call enhanced agent with full context
        response = get_agent_response_with_context(
            user_message=user_message,
            conversation_history=history,
            user_context=context,
            section=section
        )
        
        # Store conversation with context
        store_conversation_with_context(user_id, section, user_message, response, context)
        
        return jsonify({
            'reply': response.get('reply', ''),
            'agent_name': response.get('agent_name', f'{section.title()} Orchestrator'),
            'suggestions': response.get('suggestions', []),
            'form_updates': response.get('form_updates', {})
        })
        
    except Exception as e:
        print(f"Context-aware chat error: {e}")
        return jsonify({
            'reply': get_contextual_fallback(section, user_message)
        }), 200

def build_user_context(user_id, current_section, current_data=None):
    """Build comprehensive user context from all sections"""
    context = {
        'current_section': current_section,
        'timestamp': datetime.now().isoformat(),
        'identity': {},
        'mission': {},
        'milestones': [],
        'previous_interactions': [],
        'current_form_data': current_data or {}
    }
    
    try:
        # Get or create context session
        context_session = ContextSession.query.filter_by(user_id=user_id).first()
        if context_session:
            context.update(context_session.get_full_context())
        
        # Update with current form data
        if current_data:
            if current_section == 'identity':
                context['identity'].update(current_data)
            elif current_section == 'mission':
                context['mission'].update(current_data)
    
    except Exception as e:
        print(f"Context building error: {e}")
    
    return context

def get_section_conversation_history(user_id, section, limit=5):
    """Get recent conversation history for specific section"""
    try:
        conversations = Conversation.query.filter_by(
            user_id=user_id,
            section=section
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        history = []
        for conv in conversations:
            for msg in conv.messages[-10:]:  # Last 10 messages per conversation
                history.append({
                    'role': 'user' if msg.is_user else 'assistant',
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat(),
                    'agent_name': msg.agent_name
                })
        
        return history[-20:]  # Return last 20 messages
    except Exception as e:
        print(f"History retrieval error: {e}")
        return []

def get_agent_response_with_context(user_message, conversation_history, user_context, section):
    """Get AI response with full context awareness"""
    try:
        # Prepare context-aware prompt
        context_prompt = build_context_prompt(user_context, section)
        
        # Call the existing agent with enhanced context
        response = get_agent_response(
            user_message=f"{context_prompt}\n\nUser: {user_message}",
            message_history=conversation_history
        )
        
        return {
            'reply': response.get('reply', ''),
            'agent_name': response.get('agent_name', f'{section.title()} Orchestrator')
        }
        
    except Exception as e:
        print(f"Agent response error: {e}")
        return {
            'reply': get_contextual_fallback(section, user_message),
            'agent_name': f'{section.title()} Orchestrator'
        }

def build_context_prompt(user_context, section):
    """Build context-aware prompt for the AI"""
    identity = user_context.get('identity', {})
    mission = user_context.get('mission', {})
    
    context_parts = [
        f"You are the {section.title()} Orchestrator for Missiora, helping solopreneurs discover their authentic entrepreneurial path."
    ]
    
    if identity:
        identity_info = []
        if identity.get('name'):
            identity_info.append(f"Name: {identity['name']}")
        if identity.get('archetype'):
            identity_info.append(f"Archetype: {identity['archetype']}")
        if identity.get('field'):
            identity_info.append(f"Field: {identity['field']}")
        if identity.get('region'):
            identity_info.append(f"Location: {identity['region']}")
        if identity.get('mood'):
            identity_info.append(f"Current mood: {identity['mood']}")
        
        if identity_info:
            context_parts.append(f"User Identity Context: {', '.join(identity_info)}")
    
    if mission:
        context_parts.append(f"User Mission Context: {mission}")
    
    if section == 'identity':
        context_parts.append("""
        Your role is to help users discover their authentic entrepreneurial identity. Ask deep questions about:
        - Their unique strengths and values
        - What drives their passion for entrepreneurship
        - How they want to express themselves through business
        - Their natural archetype (builder, guide, rebel, creator, connector)
        
        Remember their previous responses and build upon them with follow-up questions that help them go deeper.
        Be conversational, supportive, and guide them toward filling out the identity form fields naturally.
        """)
    elif section == 'mission':
        context_parts.append("""
        Your role is to help users craft a compelling mission statement that connects their identity to their business purpose:
        - How their personal values translate to business impact
        - What change they want to create in the world
        - Who they want to serve and why
        - How their unique identity positions them to make this impact
        
        Reference their identity data to make connections between who they are and what they want to achieve.
        """)
    elif section == 'roadmap':
        context_parts.append("""
        Your role is to help users create actionable milestones based on their identity and mission:
        - Break down their mission into concrete steps
        - Suggest specific milestones that align with their archetype
        - Provide realistic timelines and resource estimates
        - Connect each milestone to their deeper purpose
        """)
    
    return "\n".join(context_parts)

def store_conversation_with_context(user_id, section, user_message, response, context):
    """Store conversation with full context for future reference"""
    try:
        # Update context session
        context_session = ContextSession.query.filter_by(user_id=user_id).first()
        if not context_session:
            context_session = ContextSession(user_id=user_id)
            db.session.add(context_session)
        
        # Update context data based on section
        if section == 'identity' and context.get('current_form_data'):
            context_session.set_identity(context['current_form_data'])
        elif section == 'mission' and context.get('current_form_data'):
            context_session.set_mission(context['current_form_data'])
        
        # Create or get conversation for this section
        conversation = Conversation.query.filter_by(
            user_id=user_id,
            section=section
        ).order_by(Conversation.updated_at.desc()).first()
        
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                section=section,
                title=f"{section.title()} Discussion",
                context_snapshot=json.dumps(context)
            )
            db.session.add(conversation)
            db.session.flush()
        
        # Add user message
        user_msg = Message(
            conversation_id=conversation.id,
            content=user_message,
            is_user=True,
            context_used=json.dumps(context)
        )
        db.session.add(user_msg)
        
        # Add AI response
        ai_msg = Message(
            conversation_id=conversation.id,
            content=response.get('reply', ''),
            is_user=False,
            agent_name=response.get('agent_name', f'{section.title()} Orchestrator')
        )
        db.session.add(ai_msg)
        
        conversation.updated_at = datetime.now()
        db.session.commit()
        
    except Exception as e:
        print(f"Conversation storage error: {e}")
        db.session.rollback()

def get_contextual_fallback(section, user_message):
    """Provide contextual fallback responses"""
    fallbacks = {
        'identity': "I'm here to help you discover your authentic entrepreneurial identity. What aspects of yourself do you want to express through your business? Think about your core values, unique strengths, and what truly drives you.",
        'mission': "Let's craft your mission together. Think about the impact you want to make and how your personal values align with your business goals. What change do you want to create in the world?",
        'roadmap': "Let's focus on your next steps. Based on your identity and mission, what milestone feels most important to tackle first? I can help you break it down into actionable steps."
    }
    
    return fallbacks.get(section, "I'm here to help you on your entrepreneurial journey. What would you like to explore?")