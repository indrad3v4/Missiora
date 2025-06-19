"""Onboarding Controller - Handles Identity → Mission → Roadmap flow"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import json
from ...layer3_frameworks.db.models import db
from ...layer1_use_cases.identity_analysis import IdentityAnalysis
from ...layer1_use_cases.mission_service import MissionService
from ...layer1_use_cases.roadmap_generator import RoadmapGenerator
from ..presenters.identity_presenter import IdentityPresenter
from ..presenters.roadmap_presenter import RoadmapPresenter

onboarding_bp = Blueprint('onboarding', __name__)

# Initialize use cases
identity_analysis = IdentityAnalysis()
mission_service = MissionService()
roadmap_generator = RoadmapGenerator()

# Initialize presenters
identity_presenter = IdentityPresenter()
roadmap_presenter = RoadmapPresenter()

@onboarding_bp.route('/api/identity', methods=['GET', 'POST'])
@login_required
def api_identity():
    """Handle identity data storage and retrieval"""
    if request.method == 'POST':
        identity_data = request.json
        
        # Process through use case
        identity = identity_analysis.process_identity_data(identity_data)
        validation = identity_analysis.validate_identity(identity)
        
        # Store in database
        current_user.identity_data = json.dumps(identity_data)
        db.session.commit()
        
        # Present response
        return jsonify({
            'success': True,
            'validation': validation,
            'presentation': identity_presenter.present_identity(identity)
        })
    else:
        if current_user.identity_data:
            raw_data = json.loads(current_user.identity_data)
            identity = identity_analysis.process_identity_data(raw_data)
            return jsonify(identity_presenter.present_identity_data(raw_data))
        return jsonify({})

@onboarding_bp.route('/api/mission', methods=['GET', 'POST'])
@login_required
def api_mission():
    """Handle mission data storage and retrieval"""
    if request.method == 'POST':
        mission_data = request.json
        
        # Process through use case
        mission = mission_service.process_mission_data(mission_data)
        validation = mission_service.validate_mission(mission)
        
        # Store in database
        current_user.mission_statement = mission_data.get('statement', '')
        current_user.current_goal = mission_data.get('goal', '')
        db.session.commit()
        
        return jsonify({
            'success': True,
            'validation': validation
        })
    else:
        return jsonify({
            'statement': current_user.mission_statement or '',
            'goal': current_user.current_goal or '',
            'blocks': ''
        })

@onboarding_bp.route('/api/user-data')
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