import logging
from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import os
from app import app, db
from models import User, Conversation, Message, UserGoal, UserInsight
# Import the new agent SDK for handoff capabilities
from agents_sdk import get_agent_response, get_greeting
from werkzeug.security import generate_password_hash
import json
from web3 import Web3
from eth_account.messages import encode_defunct

@app.route('/')
def index():
    # Redirect to the new narrative chat experience
    return redirect(url_for('narrative_chat'))

@app.route('/narrative-chat')
def narrative_chat():
    # Show the narrative-focused AI interface with MetaMask connection prompt
    return render_template('narrative_chat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to metamask login page for registration
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Redirect all registration attempts to MetaMask login
    flash('Please use MetaMask to create an account', 'info')
    return redirect(url_for('metamask_login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to metamask login page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Redirect all login attempts to MetaMask login
    return redirect(url_for('metamask_login_page'))

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
