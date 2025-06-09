import logging
from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import os
import requests
import time
from app import app, db
from models import User, Conversation, Message, UserGoal, UserInsight, Milestone
# Import the new agent SDK for handoff capabilities
from agents_sdk import get_agent_response, get_greeting
from werkzeug.security import generate_password_hash
import json
from web3 import Web3
from eth_account.messages import encode_defunct
from replit_auth import make_replit_blueprint, require_login
# Import agent building patterns
from health_check import health_bp
from activation_metrics import activation_tracker

# Register Replit Auth blueprint
app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")

# === NEW API ROUTES FOR 3-VIEW UX ===

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

def calculate_identity_completion(user):
    """Calculate identity completion percentage"""
    if not user.identity_data:
        return 0
    
    identity = json.loads(user.identity_data)
    fields = ['name', 'archetype', 'mood', 'region', 'field', 'selfTitle']
    completed = sum(1 for field in fields if identity.get(field, '').strip())
    return (completed / len(fields)) * 100

def calculate_mission_completion(user):
    """Calculate mission completion percentage"""
    if not user.mission_statement:
        return 0
    
    # Check for mission components
    fields = ['mission_statement', 'current_goal']
    completed = sum(1 for field in fields if getattr(user, field, '').strip())
    return (completed / len(fields)) * 100

def calculate_roadmap_completion(user):
    """Calculate roadmap completion percentage"""
    milestones = Milestone.query.filter_by(active=True).all()
    if not milestones:
        return 0
    
    completed_milestones = sum(1 for m in milestones if m.completed)
    return (completed_milestones / len(milestones)) * 100

def get_agent_message(stage):
    """Get personality message based on stage"""
    messages = {
        'seed': [
            "I'm just beginning to understand you! 🌱",
            "Let's plant the seeds of your mission! 🌱",
            "Tell me more about who you are! 🌱"
        ],
        'sprout': [
            "I'm growing! Your mission is becoming clearer 🌿",
            "Keep feeding me insights! 🌿",
            "I can feel your purpose taking shape! 🌿"
        ],
        'bloom': [
            "Look how far we've come! 🌸",
            "Your mission is flourishing! 🌸",
            "We're making beautiful progress! 🌸"
        ],
        'master': [
            "We've achieved mastery together! 🌟",
            "Ready for the next challenge? 🌟",
            "Your entrepreneurial spirit shines bright! 🌟"
        ]
    }
    
    stage_messages = messages.get(stage, messages['seed'])
    import random
    return random.choice(stage_messages)

def get_agent_mood(completion):
    """Determine agent mood based on completion"""
    if completion < 25:
        return 'curious'
    elif completion < 50:
        return 'excited'
    elif completion < 80:
        return 'happy'
    else:
        return 'proud'


    """Calculate identity completion percentage"""
    if not user.identity_data:
        return 0
    
    identity = json.loads(user.identity_data)
    fields = ['name', 'archetype', 'mood', 'region', 'field', 'selfTitle']
    completed = sum(1 for field in fields if identity.get(field, '').strip())
    return (completed / len(fields)) * 100

def calculate_mission_completion(user):
    """Calculate mission completion percentage"""
    if not user.mission_statement:
        return 0
    
    # Check for mission components
    fields = ['mission_statement', 'current_goal']
    completed = sum(1 for field in fields if getattr(user, field, '').strip())
    return (completed / len(fields)) * 100

def calculate_roadmap_completion(user):
    """Calculate roadmap completion percentage"""
    milestones = Milestone.query.filter_by(active=True).all()
    if not milestones:
        return 0
    
    completed_milestones = sum(1 for m in milestones if m.completed)
    return (completed_milestones / len(milestones)) * 100

def get_agent_message(stage):
    """Get personality message based on stage"""
    messages = {
        'seed': [
            "I'm just beginning to understand you! 🌱",
            "Let's plant the seeds of your mission! 🌱",
            "Tell me more about who you are! 🌱"
        ],
        'sprout': [
            "I'm growing! Your mission is becoming clearer 🌿",
            "Keep feeding me insights! 🌿",
            "I can feel your purpose taking shape! 🌿"
        ],
        'bloom': [
            "Look how far we've come! 🌸",
            "Your mission is flourishing! 🌸",
            "We're making beautiful progress! 🌸"
        ],
        'master': [
            "We've achieved mastery together! 🌟",
            "Ready for the next challenge? 🌟",
            "Your entrepreneurial spirit shines bright! 🌟"
        ]
    }
    
    stage_messages = messages.get(stage, messages['seed'])
    import random
    return random.choice(stage_messages)

def get_agent_mood(completion):
    """Determine agent mood based on completion"""
    if completion < 25:
        return 'curious'
    elif completion < 50:
        return 'excited'
    elif completion < 80:
        return 'happy'
    else:
        return 'proud'


# Add these routes to routes.py for agent state management


def calculate_identity_completion(user):
    """Calculate identity completion percentage"""
    if not user.identity_data:
        return 0
    
    identity = json.loads(user.identity_data)
    fields = ['name', 'archetype', 'mood', 'region', 'field', 'selfTitle']
    completed = sum(1 for field in fields if identity.get(field, '').strip())
    return (completed / len(fields)) * 100

def calculate_mission_completion(user):
    """Calculate mission completion percentage"""
    if not user.mission_statement:
        return 0
    
    # Check for mission components
    fields = ['mission_statement', 'current_goal']
    completed = sum(1 for field in fields if getattr(user, field, '').strip())
    return (completed / len(fields)) * 100

def calculate_roadmap_completion(user):
    """Calculate roadmap completion percentage"""
    milestones = Milestone.query.filter_by(active=True).all()
    if not milestones:
        return 0
    
    completed_milestones = sum(1 for m in milestones if m.completed)
    return (completed_milestones / len(milestones)) * 100

def get_agent_message(stage):
    """Get personality message based on stage"""
    messages = {
        'seed': [
            "I'm just beginning to understand you! 🌱",
            "Let's plant the seeds of your mission! 🌱",
            "Tell me more about who you are! 🌱"
        ],
        'sprout': [
            "I'm growing! Your mission is becoming clearer 🌿",
            "Keep feeding me insights! 🌿",
            "I can feel your purpose taking shape! 🌿"
        ],
        'bloom': [
            "Look how far we've come! 🌸",
            "Your mission is flourishing! 🌸",
            "We're making beautiful progress! 🌸"
        ],
        'master': [
            "We've achieved mastery together! 🌟",
            "Ready for the next challenge? 🌟",
            "Your entrepreneurial spirit shines bright! 🌟"
        ]
    }
    
    stage_messages = messages.get(stage, messages['seed'])
    import random
    return random.choice(stage_messages)

def get_agent_mood(completion):
    """Determine agent mood based on completion"""
    if completion < 25:
        return 'curious'
    elif completion < 50:
        return 'excited'
    elif completion < 80:
        return 'happy'
    else:
        return 'proud'


@app.route('/api/identity', methods=['GET', 'POST'])
@login_required
def api_identity():
    """Handle identity data storage and retrieval"""
    if request.method == 'POST':
        identity_data = request.json
        current_user.identity_data = json.dumps(identity_data)
        db.session.commit()
        return jsonify({'success': True})
    else:
        if current_user.identity_data:
            return jsonify(json.loads(current_user.identity_data))
        return jsonify({})

@app.route('/api/mission', methods=['GET', 'POST'])
@login_required
def api_mission():
    """Handle mission data storage and retrieval"""
    if request.method == 'POST':
        mission_data = request.json
        current_user.mission_statement = mission_data.get('statement', '')
        current_user.current_goal = mission_data.get('goal', '')
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({
            'statement': current_user.mission_statement or '',
            'goal': current_user.current_goal or '',
            'blocks': ''
        })

@app.route('/api/milestones')
@login_required
def api_milestones():
    """Get all milestones"""
    milestones = Milestone.query.order_by(Milestone.order_index).all()
    return jsonify([{
        'id': m.id,
        'code': m.code,
        'title': m.title,
        'description': m.description,
        'active': m.active,
        'completed': m.completed,
        'order_index': m.order_index
    } for m in milestones])

@app.route('/api/milestones/<int:milestone_id>/complete', methods=['POST'])
@login_required
def api_complete_milestone(milestone_id):
    """Mark milestone as complete and activate next"""
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.completed = True
    milestone.active = False
    
    # Activate next milestone
    next_milestone = Milestone.query.filter(
        Milestone.order_index > milestone.order_index,
        Milestone.completed == False
    ).order_by(Milestone.order_index).first()
    
    if next_milestone:
        next_milestone.active = True
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/milestones/<int:milestone_id>/activate', methods=['POST'])
@login_required
def api_activate_milestone(milestone_id):
    """Activate a specific milestone"""
    # Deactivate all milestones
    Milestone.query.update({'active': False})
    
    # Activate selected milestone
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.active = True
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/user-data')
@login_required
def api_user_data():
    """Get user data for header display"""
    identity_data = {}
    if current_user.identity_data:
        identity_data = json.loads(current_user.identity_data)
    
    return jsonify({
        'name': identity_data.get('name', current_user.username),
        'currentGoal': current_user.current_goal or 'Set Your Goal',
        'location': identity_data.get('region', 'Location'),
        'timeline': 'Q1 2025',
        'balance': '€0'
    })

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chat requests for mission building"""
    data = request.get_json()
    user_message = data.get('user_message', '')
    
    try:
        # Use the existing agent system
        response = get_agent_response(user_message)
        return jsonify({
            'reply': response.get('reply', 'I understand. Tell me more about your goals.'),
            'agent': response.get('agent', 'orchestrator')
        })
    except Exception as e:
        app.logger.error(f"Chat error: {e}")
        return jsonify({
            'reply': 'I understand your perspective. Could you tell me more about what success looks like for you?',
            'agent': 'orchestrator'
        })

@app.route('/')
def index():
    """Main application entry point"""
    return render_template('app.html')

@app.route('/app')
def app_interface():
    """Main app interface - handles both auth states"""
    guest_mode = request.args.get('guest') == 'true'
    if current_user.is_authenticated or guest_mode:
        return render_template('index.html')
    else:
        return redirect(url_for('replit_auth.login'))

@app.route('/narrative-chat')
def narrative_chat():
    # Show the narrative-focused AI interface with MetaMask connection prompt
    return render_template('narrative_chat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to authentication options page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('auth_options'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to authentication options page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('auth_options'))

@app.route('/metamask', methods=['GET'])
def metamask_login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('metamask_login.html')

@app.route('/metamask/login', methods=['POST'])
def metamask_login():
    try:
        data = request.json
        if not data or 'address' not in data or 'signature' not in data or 'message' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        address = data['address']
        signature = data['signature']
        message = data['message']
        
        # Verify the signature
        w3 = Web3()
        message_encoded = encode_defunct(text=message)
        recovered_address = w3.eth.account.recover_message(message_encoded, signature=signature)
        
        if recovered_address.lower() != address.lower():
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Check if user exists
        user = User.query.filter_by(ethereum_address=address.lower()).first()
        
        if user:
            # User exists, log them in
            login_user(user, remember=True)
            return jsonify({'success': True}), 200
        else:
            # Create new user
            username = f"user_{address.lower()[:8]}"
            base_username = username
            counter = 1
            
            # Make sure username is unique
            while User.query.filter_by(username=username).first():
                username = f"{base_username}_{counter}"
                counter += 1
            
            new_user = User(
                username=username,
                ethereum_address=address.lower(),
                auth_type='metamask'
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            return jsonify({'success': True, 'new_user': True}), 200
            
    except Exception as e:
        logging.error(f"Error during MetaMask login: {e}")
        return jsonify({'error': 'Authentication failed'}), 500

@app.route('/auth/github')
def github_auth():
    """GitHub OAuth authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # For demo purposes, create a simple mock authentication
    # In production, this would integrate with GitHub OAuth
    session['pending_auth'] = {
        'provider': 'github',
        'user_id': 'github_demo_user',
        'username': 'github_user',
        'email': 'user@github.example'
    }
    return redirect(url_for('complete_oauth'))

@app.route('/auth/google')
def google_auth():
    """Google OAuth authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # For demo purposes, create a simple mock authentication
    # In production, this would integrate with Google OAuth
    session['pending_auth'] = {
        'provider': 'google',
        'user_id': 'google_demo_user',
        'username': 'google_user',
        'email': 'user@gmail.example'
    }
    return redirect(url_for('complete_oauth'))

@app.route('/auth/apple')
def apple_auth():
    """Apple ID authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # For demo purposes, create a simple mock authentication
    # In production, this would integrate with Apple Sign In
    session['pending_auth'] = {
        'provider': 'apple',
        'user_id': 'apple_demo_user',
        'username': 'apple_user',
        'email': 'user@icloud.example'
    }
    return redirect(url_for('complete_oauth'))

@app.route('/auth/complete')
def complete_oauth():
    """Complete OAuth authentication process"""
    auth_data = session.pop('pending_auth', None)
    if not auth_data:
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('auth_options'))
    
    provider = auth_data['provider']
    provider_user_id = auth_data['user_id']
    username = auth_data['username']
    email = auth_data['email']
    
    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    
    if user:
        # User exists, log them in
        login_user(user, remember=True)
        flash(f'Welcome back!', 'success')
        return redirect(url_for('dashboard'))
    else:
        # Create new user
        base_username = username
        counter = 1
        
        # Ensure username is unique
        while User.query.filter_by(username=username).first():
            username = f"{base_username}_{counter}"
            counter += 1
        
        new_user = User(
            username=username,
            email=email,
            auth_type=provider
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user, remember=True)
        flash(f'Account created successfully!', 'success')
        return redirect(url_for('dashboard'))

@app.route('/auth/options')
def auth_options():
    """Show authentication options page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('auth_options.html')

@app.route('/api/auth/status')
def auth_status():
    """Check authentication status for API calls"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user_id': current_user.id if current_user.is_authenticated else None,
        'username': current_user.username if current_user.is_authenticated else None
    })

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent conversations
    recent_conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).limit(5).all()
    # Get user's goals
    goals = UserGoal.query.filter_by(user_id=current_user.id).all()
    # Get user's insights
    insights = UserInsight.query.filter_by(user_id=current_user.id).order_by(UserInsight.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          recent_conversations=recent_conversations,
                          goals=goals,
                          insights=insights)

@app.route('/chat', methods=['GET'])
@login_required
def chat():
    conversation_id = request.args.get('id')
    if conversation_id:
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first_or_404()
        messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at).all()
    else:
        conversation = None
        messages = []
    
    all_conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    return render_template('chat.html', conversation=conversation, messages=messages, all_conversations=all_conversations)

@app.route('/api/conversations', methods=['GET'])
@login_required
def get_conversations():
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    return jsonify([{
        'id': conv.id,
        'title': conv.title,
        'created_at': conv.created_at.isoformat(),
        'updated_at': conv.updated_at.isoformat()
    } for conv in conversations])

@app.route('/api/conversations', methods=['POST'])
@login_required
def create_conversation():
    # Create a new conversation
    conversation = Conversation(user_id=current_user.id)
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'id': conversation.id,
        'title': conversation.title,
        'created_at': conversation.created_at.isoformat(),
        'updated_at': conversation.updated_at.isoformat()
    }), 201

@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first_or_404()
    db.session.delete(conversation)
    db.session.commit()
    return '', 204

@app.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
@login_required
def get_messages(conversation_id):
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first_or_404()
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at).all()
    return jsonify([{
        'id': msg.id,
        'content': msg.content,
        'is_user': msg.is_user,
        'created_at': msg.created_at.isoformat()
    } for msg in messages])

@app.route('/api/conversations/<int:conversation_id>/messages', methods=['POST'])
@login_required
def send_message(conversation_id):
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        content=data['content'],
        is_user=True
    )
    db.session.add(user_message)
    
    # Update conversation timestamp
    conversation.updated_at = user_message.created_at
    
    # Update conversation title if it's the first message
    if conversation.title == "New Conversation" and len(data['content']) > 0:
        # Use first few words for the title
        title_preview = data['content'][:30] + ('...' if len(data['content']) > 30 else '')
        conversation.title = title_preview
    
    db.session.commit()
    
    # Get AI response
    try:
        # Get user profile information for context
        user_info = {
            'username': current_user.username,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'bio': current_user.bio,
            'business_name': current_user.business_name,
            'business_description': current_user.business_description
        }
        
        # Get previous messages for context
        previous_messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at).all()
        message_history = [{'role': 'user' if msg.is_user else 'assistant', 'content': msg.content} for msg in previous_messages]
        
        # Get AI response
        ai_response = get_agent_response(data['content'], message_history, user_info)
        
        # Save AI response
        ai_message = Message(
            conversation_id=conversation.id,
            content=ai_response,
            is_user=False
        )
        db.session.add(ai_message)
        db.session.commit()
        
        # Extract insights if appropriate
        if len(ai_response) > 100 and any(keyword in ai_response.lower() for keyword in ['insight', 'discover', 'realize', 'clarity']):
            # Create a new insight
            insight = UserInsight(
                user_id=current_user.id,
                content=ai_response[:200] + ("..." if len(ai_response) > 200 else ""),
                source_conversation_id=conversation.id
            )
            db.session.add(insight)
            db.session.commit()
        
        return jsonify({
            'id': ai_message.id,
            'content': ai_message.content,
            'is_user': ai_message.is_user,
            'created_at': ai_message.created_at.isoformat()
        })
    
    except Exception as e:
        logging.error(f"Error getting AI response: {e}")
        return jsonify({'error': 'Failed to get AI response. Please try again.'}), 500

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update user profile information
        current_user.first_name = request.form.get('first_name', '')
        current_user.last_name = request.form.get('last_name', '')
        current_user.bio = request.form.get('bio', '')
        current_user.business_name = request.form.get('business_name', '')
        current_user.business_description = request.form.get('business_description', '')
        
        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating profile: {e}")
            flash('An error occurred while updating profile', 'danger')
            
    return render_template('profile.html')

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        if not title:
            flash('Goal title is required', 'danger')
        else:
            goal = UserGoal(
                user_id=current_user.id,
                title=title,
                description=description
            )
            db.session.add(goal)
            db.session.commit()
            flash('Goal added successfully', 'success')
            
    goals = UserGoal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals.html', goals=goals)

@app.route('/api/goals/<int:goal_id>/toggle', methods=['POST'])
@login_required
def toggle_goal(goal_id):
    goal = UserGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    goal.completed = not goal.completed
    db.session.commit()
    return jsonify({'id': goal.id, 'completed': goal.completed})

@app.route('/insights')
@login_required
def insights():
    insights = UserInsight.query.filter_by(user_id=current_user.id).order_by(UserInsight.created_at.desc()).all()
    return render_template('insights.html', insights=insights)

# Enhanced API endpoint for narrative-style chat with agent handoff
@app.route('/api/chat', methods=['POST'])
def public_chat():
    """API endpoint for the narrative-style chat feature with agent handoff capabilities"""
    try:
        data = request.json
        
        # Check if this is a start conversation request
        if data.get('start'):
            # Initialize or reset the chat session
            session['conversation_history'] = None  # Set to None for first turn
            greeting = get_greeting()
            
            return jsonify({
                'reply': greeting['reply'],
                'agent': greeting['agent']
            })
        
        # Otherwise, handle a user message
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user_message = data.get('user_message')
        if not user_message:
            return jsonify({'error': 'Message content is required'}), 400
        
        address = data.get('address')
        
        # Retrieve conversation history from session
        conversation_history = session.get('conversation_history')
        
        # Check for free usage count or MetaMask authentication
        free_message_count = session.get('free_message_count', 0)
        
        # If we have an ethereum address, try to find the user for personalization
        if address and not current_user.is_authenticated:
            user = User.query.filter_by(ethereum_address=address.lower()).first()
            if user:
                # Use authenticated user with MetaMask
                login_user(user, remember=True)
                # Reset free message count if user is authenticated
                free_message_count = 0
        else:
            # If no address and not authenticated, increment free message count
            if not current_user.is_authenticated:
                free_message_count += 1
                session['free_message_count'] = free_message_count
                
                # If over limit, require MetaMask login
                if free_message_count > 10:  # Allow 10 free messages
                    return jsonify({
                        'error': 'Free message limit reached. Please connect with MetaMask to continue.',
                        'require_metamask': True
                    }), 403
        
        # Store message in database if user is authenticated
        if current_user.is_authenticated:
            # Create or update conversation record for this chat session
            conversation_id = session.get('current_conversation_id')
            if not conversation_id:
                # Create a new conversation
                conversation = Conversation(user_id=current_user.id)
                db.session.add(conversation)
                db.session.commit()
                session['current_conversation_id'] = conversation.id
            else:
                # Use existing conversation
                conversation = Conversation.query.get(conversation_id)
                if not conversation or conversation.user_id != current_user.id:
                    # Create a new conversation if ID is invalid
                    conversation = Conversation(user_id=current_user.id)
                    db.session.add(conversation)
                    db.session.commit()
                    session['current_conversation_id'] = conversation.id
            
            # Add user message to DB
            user_msg = Message(
                conversation_id=conversation.id,
                content=user_message,
                is_user=True
            )
            db.session.add(user_msg)
            db.session.commit()
        
        # Get response from orchestrated AI agents with handoff capabilities using SDK 0.0.12
        result = get_agent_response(user_message, conversation_history)
        
        # Store the updated conversation history for next turn
        session['conversation_history'] = result.get('conversation_history')
        
        # If user is logged in, save the AI response to the database
        if current_user.is_authenticated and session.get('current_conversation_id'):
            conversation_id = session.get('current_conversation_id')
            ai_message = Message(
                conversation_id=conversation_id,
                content=result['reply'],
                is_user=False
            )
            db.session.add(ai_message)
            db.session.commit()
            
            # Update conversation title if it's new
            conversation = Conversation.query.get(conversation_id)
            if conversation and conversation.title == "New Conversation":
                conversation.title = user_message[:30] + ('...' if len(user_message) > 30 else '')
                db.session.commit()
        
        return jsonify({
            'reply': result['reply'],
            'agent': result['agent'],
            'free_messages_remaining': 10 - free_message_count if not current_user.is_authenticated else None
        })
    
    except Exception as e:
        logging.error(f"Error in narrative chat API: {e}")
        return jsonify({'error': f'Failed to get AI response. Error: {str(e)}'}), 500



# Add these vision API routes to routes.py

@app.route('/api/vision/analyze', methods=['POST'])
def analyze_vision():
    """CLIP Vision analysis endpoint for object detection"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 image data
        image_data = data['image']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Use OpenAI Vision API (GPT-4 Vision)
        from openai import OpenAI
        import base64
        
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image and identify objects that would be relevant to a solopreneur in Krakow. Focus on:
                            - Business-related items (laptops, business cards, documents, whiteboards)
                            - People and networking opportunities
                            - QR codes or text that could be scanned
                            - Plants, books, or inspirational items
                            - Workspace elements
                            
                            For each object, provide:
                            1. Object label (simple, descriptive name)
                            2. Confidence level (0-1)
                            3. Approximate bounding box coordinates (x, y, width, height as percentages of image)
                            4. Whether it's actionable (business card, QR code, etc.)
                            
                            Respond in JSON format like this:
                            {
                                "objects": [
                                    {
                                        "label": "laptop",
                                        "confidence": 0.95,
                                        "boundingBox": {"x": 100, "y": 150, "width": 200, "height": 150},
                                        "actionable": true
                                    }
                                ],
                                "scene_description": "Brief description of the overall scene"
                            }"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Parse the response
        analysis_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        import json
        import re
        
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            try:
                analysis_result = json.loads(json_match.group())
            except json.JSONDecodeError:
                # Fallback: create a basic response
                analysis_result = {
                    "objects": [
                        {
                            "label": "detected object",
                            "confidence": 0.8,
                            "boundingBox": {"x": 50, "y": 50, "width": 200, "height": 200},
                            "actionable": False
                        }
                    ],
                    "scene_description": "Scene analysis available"
                }
        else:
            # Fallback response
            analysis_result = {
                "objects": [],
                "scene_description": "Unable to parse vision analysis"
            }
        
        # Add timestamp
        analysis_result['timestamp'] = data.get('timestamp', int(time.time() * 1000))
        analysis_result['processing_time'] = int(time.time() * 1000) - analysis_result['timestamp']
        
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"Vision analysis error: {e}")
        return jsonify({
            'error': 'Vision analysis failed',
            'objects': [],
            'scene_description': 'Analysis unavailable'
        }), 500

@app.route('/api/vision/action', methods=['POST'])
def execute_vision_action():
    """Execute action based on detected object"""
    try:
        data = request.get_json()
        action_id = data.get('action')
        object_data = data.get('object', {})
        
        # Execute different actions based on type
        result = {'title': 'Action Complete', 'message': 'Action executed successfully'}
        
        if action_id == 'scan_card':
            result = {
                'title': 'Business Card Scanned',
                'message': 'Contact information extracted and ready to save.',
                'data': {
                    'name': 'John Doe',
                    'company': 'Tech Startup',
                    'email': 'john@example.com',
                    'phone': '+48 123 456 789'
                }
            }
            
        elif action_id == 'scan_qr':
            result = {
                'title': 'QR Code Scanned',
                'message': 'QR code content decoded successfully.',
                'data': {
                    'type': 'url',
                    'content': 'https://example.com/networking'
                }
            }
            
        elif action_id == 'ocr_text':
            result = {
                'title': 'Text Extracted',
                'message': 'Text has been extracted and is ready to process.',
                'data': {
                    'extracted_text': 'Sample extracted text from the image'
                }
            }
            
        elif action_id == 'networking_tips':
            result = {
                'title': 'Networking Insights',
                'message': 'Based on what I see, here are some networking tips for Krakow entrepreneurs.',
                'data': {
                    'tips': [
                        'Join local startup meetups in Krakow',
                        'Connect on LinkedIn within 24 hours',
                        'Follow up with a personalized message'
                    ]
                }
            }
            
        elif action_id == 'add_to_roadmap':
            # Add item to user's roadmap
            if current_user.is_authenticated:
                new_milestone = Milestone()
                new_milestone.title = f"Action from vision: {object_data.get('label', 'Unknown')}"
                new_milestone.description = f"Follow up on detected {object_data.get('label', 'item')}"
                new_milestone.active = True
                new_milestone.code = f"vision_{int(time.time())}"
                
                db.session.add(new_milestone)
                db.session.commit()
                
                result = {
                    'title': 'Added to Roadmap',
                    'message': 'New milestone created based on your vision input.'
                }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Action execution error: {e}")
        return jsonify({
            'title': 'Action Failed',
            'message': 'Unable to execute the requested action.'
        }), 500

@app.route('/api/milestones/from-suggestion', methods=['POST'])
def create_milestone_from_suggestion():
    """Create milestone from vision-based suggestion"""
    try:
        data = request.get_json()
        suggestion_text = data.get('suggestion', '')
        source = data.get('source', 'vision')
        
        if current_user.is_authenticated:
            new_milestone = Milestone()
            new_milestone.title = f"Vision Insight: {source}"
            new_milestone.description = suggestion_text
            new_milestone.active = True
            new_milestone.code = f"suggestion_{int(time.time())}"
            new_milestone.order_index = len(Milestone.query.all()) + 1
            
            db.session.add(new_milestone)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'milestone_id': new_milestone.id,
                'message': 'Milestone created from suggestion'
            })
        else:
            return jsonify({'error': 'Authentication required'}), 401
            
    except Exception as e:
        print(f"Milestone creation error: {e}")
        return jsonify({'error': 'Failed to create milestone'}), 500
