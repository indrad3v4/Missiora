"""Milestone Controller - Handles roadmap and milestone operations"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ...layer3_frameworks.db.models import Milestone, db
from ...layer1_use_cases.roadmap_generator import RoadmapGenerator
from ..presenters.roadmap_presenter import RoadmapPresenter

milestone_bp = Blueprint('milestone', __name__)

# Initialize services
roadmap_generator = RoadmapGenerator()
roadmap_presenter = RoadmapPresenter()

@milestone_bp.route('/api/milestones')
@login_required
def api_milestones():
    """Get all milestones"""
    milestones = Milestone.query.order_by(Milestone.order_index).all()
    
    # Convert to entities and present
    milestone_data = []
    for m in milestones:
        milestone_data.append({
            'id': m.id,
            'code': m.code,
            'title': m.title,
            'description': m.description,
            'active': m.active,
            'completed': m.completed,
            'order_index': m.order_index
        })
    
    return jsonify(roadmap_presenter.present_milestones(milestone_data))

@milestone_bp.route('/api/milestones/<int:milestone_id>/complete', methods=['POST'])
@login_required
def api_complete_milestone(milestone_id):
    """Mark milestone as complete and activate next"""
    milestone = Milestone.query.get_or_404(milestone_id)
    
    # Track activation metrics
    if milestone.code == 'M1_FOUNDATION':
        activation_tracker.track_milestone_1_completion(current_user.id)
    
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

@milestone_bp.route('/api/milestones/<int:milestone_id>/activate', methods=['POST'])
@login_required
def api_activate_milestone(milestone_id):
    """Activate a specific milestone"""
    # Deactivate all milestones
    Milestone.query.update({'active': False})
    
    # Activate the specified milestone
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.active = True
    
    db.session.commit()
    return jsonify({'success': True})