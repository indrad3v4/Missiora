"""Legacy routes for backward compatibility"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import os
import requests
import time
from . import db
from ..db.models import User, Conversation, Message, UserGoal, UserInsight, Milestone
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
        return redirect(url_for('legacy.app_interface'))
    try:
        return render_template('landing.html')
    except:
        # Fallback if template is missing
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Missiora Agency</title></head>
        <body>
            <h1>Welcome to Missiora Agency</h1>
            <p>AI-powered entrepreneurial platform for solopreneurs</p>
            <a href="/login">Login</a> | <a href="/register">Register</a>
        </body>
        </html>
        '''

@legacy_bp.route('/app')
@login_required 
def app_interface():
    """Main app interface - handles both auth states"""
    try:
        return render_template('app.html')
    except:
        # Fallback if template is missing
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Missiora App</title></head>
        <body>
            <h1>Missiora App Interface</h1>
            <p>Welcome to your entrepreneurial journey dashboard</p>
            <div>
                <a href="/api/identity">Identity</a> | 
                <a href="/api/mission">Mission</a> | 
                <a href="/api/milestones">Roadmap</a> |
                <a href="/logout">Logout</a>
            </div>
        </body>
        </html>
        '''

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
        user = User()
        user.username = username
        user.email = email
        user.password_hash = generate_password_hash(password)
        
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
            return redirect(url_for('legacy.dashboard'))
        else:
            flash('Invalid username or password')
    
    try:
        return render_template('login.html')
    except:
        # Fallback login form
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Login - Missiora</title></head>
        <body>
            <h1>Login</h1>
            <form method="POST">
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <p><a href="/register">Register</a> | <a href="/">Home</a></p>
        </body>
        </html>
        '''

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