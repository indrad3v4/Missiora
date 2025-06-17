"""
Health Check System - Regression Testing
Implements the /healthz endpoint and basic app boot verification
"""

from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/healthz', methods=['GET'])
def health_check():
    """Health check endpoint for regression testing"""
    try:
        # Verify database connection
        from models import User
        User.query.first()
        
        # Verify agent system is responsive
        from agents_sdk import get_greeting
        greeting = get_greeting()
        
        return jsonify({
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "agent_system": "responsive",
            "version": "1.0.0"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@health_bp.route('/healthz/activation', methods=['GET'])
def activation_health():
    """Health check for activation metrics"""
    try:
        from activation_metrics import activation_tracker
        
        activation_rate = activation_tracker.get_activation_rate()
        is_meeting_target = activation_tracker.is_meeting_target()
        
        return jsonify({
            "activation_rate": round(activation_rate, 2),
            "meeting_70_percent_target": is_meeting_target,
            "total_signups": activation_tracker.data['total_signups'],
            "milestone_1_completions": activation_tracker.data['milestone_1_completions'],
            "instant_wins": activation_tracker.data['instant_wins']
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500