"""Legacy routes for backward compatibility"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import os
import requests
import time
from layer3_frameworks.flask_app import db
from layer3_frameworks.db.models import User, Conversation, Message, UserGoal, UserInsight, Milestone
from werkzeug.security import generate_password_hash
import json
from web3 import Web3
from eth_account.messages import encode_defunct

# Create blueprint for legacy routes
legacy_bp = Blueprint('legacy', __name__)

@legacy_bp.route('/')
def index():
    """Main application entry point"""
    if current_user.is_authenticated:
        return redirect(url_for('app_interface'))
    return render_template('landing.html')

@legacy_bp.route('/app')
@login_required 
def app_interface():
    """Main app interface - handles both auth states"""
    return render_template('app.html')

@legacy_bp.route('/narrative-chat')
def narrative_chat():
    return render_template('narrative_chat.html')

@legacy_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@legacy_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@legacy_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@legacy_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@legacy_bp.route('/auth-options')
def auth_options():
    """Show authentication options page"""
    return render_template('auth_options.html')

@legacy_bp.route('/auth-status')
def auth_status():
    """Check authentication status for API calls"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user_id': current_user.id if current_user.is_authenticated else None
    })