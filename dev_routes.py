"""
Development routes for mobile interface without authentication
"""

from flask import request, jsonify, session, render_template
from app import app
from agent_service import get_agent_response
import json

@app.route('/dev')
def dev_index():
    """Development version without authentication"""
    return render_template('index_mobile.html')

@app.route('/api/dev/identity', methods=['GET', 'POST'])
def dev_api_identity():
    """Handle identity data storage and retrieval - development version"""
    if request.method == 'POST':
        identity_data = request.json
        session['identity_data'] = identity_data
        return jsonify({'status': 'success'})
    else:
        return jsonify(session.get('identity_data', {}))

@app.route('/api/dev/mission', methods=['GET', 'POST'])
def dev_api_mission():
    """Handle mission data storage and retrieval - development version"""
    if request.method == 'POST':
        mission_data = request.json
        session['mission_data'] = mission_data
        return jsonify({'status': 'success'})
    else:
        return jsonify(session.get('mission_data', {}))

@app.route('/api/dev/milestones', methods=['GET'])
def dev_api_milestones():
    """Get all milestones - development version"""
    default_milestones = [
        {
            'id': 1,
            'code': 'define_identity',
            'title': 'Define Identity',
            'description': 'Discover your entrepreneurial archetype and core values',
            'active': True,
            'completed': False,
            'order_index': 1
        },
        {
            'id': 2,
            'code': 'build_mission',
            'title': 'Build Mission',
            'description': 'Craft your mission statement and define your impact',
            'active': False,
            'completed': False,
            'order_index': 2
        },
        {
            'id': 3,
            'code': 'first_offer',
            'title': 'First AI Offer',
            'description': 'Create your initial service offering with AI assistance',
            'active': False,
            'completed': False,
            'order_index': 3
        },
        {
            'id': 4,
            'code': 'secure_clients',
            'title': 'Secure First Clients',
            'description': 'Find and convert your first paying customers',
            'active': False,
            'completed': False,
            'order_index': 4
        },
        {
            'id': 5,
            'code': 'earn_1k',
            'title': 'Earn €1K from AiMe',
            'description': 'Reach your first €1000 in revenue through AI-powered services',
            'active': False,
            'completed': False,
            'order_index': 5
        }
    ]
    
    milestones = session.get('milestones', default_milestones)
    return jsonify(milestones)

@app.route('/api/dev/milestones/<int:milestone_id>/complete', methods=['POST'])
def dev_complete_milestone(milestone_id):
    """Mark milestone as complete and activate next - development version"""
    milestones = session.get('milestones', [])
    
    for i, milestone in enumerate(milestones):
        if milestone['id'] == milestone_id:
            milestone['completed'] = True
            milestone['active'] = False
            
            # Activate next milestone
            if i + 1 < len(milestones):
                milestones[i + 1]['active'] = True
            break
    
    session['milestones'] = milestones
    return jsonify({'status': 'success'})

@app.route('/api/dev/milestones/<int:milestone_id>/activate', methods=['POST'])
def dev_activate_milestone(milestone_id):
    """Activate a specific milestone - development version"""
    milestones = session.get('milestones', [])
    
    for milestone in milestones:
        if milestone['id'] == milestone_id:
            milestone['active'] = True
        else:
            milestone['active'] = False
    
    session['milestones'] = milestones
    return jsonify({'status': 'success'})

@app.route('/api/dev/user-data')
def dev_api_user_data():
    """Get user data for header display - development version"""
    identity_data = session.get('identity_data', {})
    mission_data = session.get('mission_data', {})
    
    return jsonify({
        'name': identity_data.get('name', 'Solopreneur'),
        'currentGoal': mission_data.get('mission_statement', 'Reach €1K')[:30] + '...' if mission_data.get('mission_statement') else 'Reach €1K',
        'location': identity_data.get('region', 'Kraków'),
        'timeline': 'Q3 2025',
        'balance': '0'
    })

@app.route('/api/dev/context-aware-chat', methods=['POST'])
def dev_context_aware_chat():
    """Enhanced chat endpoint with full context awareness - development version"""
    try:
        data = request.get_json()
        user_message = data.get('user_message', '')
        section = data.get('section', 'general')
        current_data = data.get('current_data', {})
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Build context from session data
        identity_data = session.get('identity_data', {})
        mission_data = session.get('mission_data', {})
        
        context_prompt = build_dev_context_prompt(identity_data, mission_data, section)
        
        # Call the agent with context
        try:
            response = get_agent_response(
                user_message=f"{context_prompt}\n\nUser: {user_message}"
            )
            
            return jsonify({
                'reply': response.get('reply', f'I understand you\'re working on your {section}. How can I help you explore this further?'),
                'agent_name': f'{section.title()} Orchestrator'
            })
            
        except Exception as e:
            fallback_responses = {
                'identity': "I'm here to help you discover your authentic entrepreneurial identity. What aspects of yourself do you want to express through your business?",
                'mission': "Let's craft your mission together. Think about the impact you want to make and how your personal values align with your business goals.",
                'roadmap': "Let's focus on your next steps. What milestone feels most important to tackle first?"
            }
            
            return jsonify({
                'reply': fallback_responses.get(section, "I'm here to help you on your entrepreneurial journey. What would you like to explore?"),
                'agent_name': f'{section.title()} Orchestrator'
            })
        
    except Exception as e:
        return jsonify({
            'reply': 'I understand. Let me help you think through this step by step.',
            'agent_name': 'Orchestrator'
        }), 200

def build_dev_context_prompt(identity_data, mission_data, section):
    """Build context-aware prompt for the AI - development version"""
    context_parts = [
        f"You are the {section.title()} Orchestrator for Missiora, helping solopreneurs discover their authentic entrepreneurial path."
    ]
    
    if identity_data:
        identity_info = []
        if identity_data.get('name'):
            identity_info.append(f"Name: {identity_data['name']}")
        if identity_data.get('archetype'):
            identity_info.append(f"Archetype: {identity_data['archetype']}")
        if identity_data.get('field'):
            identity_info.append(f"Field: {identity_data['field']}")
        if identity_data.get('region'):
            identity_info.append(f"Location: {identity_data['region']}")
        
        if identity_info:
            context_parts.append(f"User Identity Context: {', '.join(identity_info)}")
    
    if mission_data:
        mission_info = []
        if mission_data.get('purpose'):
            mission_info.append(f"Purpose: {mission_data['purpose']}")
        if mission_data.get('impact'):
            mission_info.append(f"Impact: {mission_data['impact']}")
        
        if mission_info:
            context_parts.append(f"User Mission Context: {', '.join(mission_info)}")
    
    if section == 'identity':
        context_parts.append("""
        Your role is to help users discover their authentic entrepreneurial identity. Ask deep questions about:
        - Their unique strengths and values
        - What drives their passion for entrepreneurship
        - How they want to express themselves through business
        - Their natural archetype (builder, guide, rebel, creator, connector)
        
        Be conversational, supportive, and guide them toward understanding their authentic self.
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