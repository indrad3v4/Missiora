"""Feedback Controller - Handles NPS feedback collection"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ...layer1_use_cases.feedback_service import FeedbackService
from ..presenters.feedback_presenter import FeedbackPresenter

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')

# Initialize services
feedback_service = FeedbackService()
feedback_presenter = FeedbackPresenter()

@feedback_bp.route('/nps', methods=['POST'])
def submit_nps():
    """Submit NPS feedback"""
    try:
        data = request.get_json()
        score = data.get('score')
        verbatim = data.get('verbatim', '')
        
        if score is None:
            return jsonify({'error': 'Score is required'}), 400
        
        user_id = current_user.id if current_user.is_authenticated else 'anonymous'
        
        # Collect feedback
        feedback_entry = feedback_service.collect_nps_feedback(user_id, score, verbatim)
        
        # Present response
        response = feedback_presenter.present_nps_submission(feedback_entry)
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to submit feedback'}), 500

@feedback_bp.route('/nps/metrics', methods=['GET'])
@login_required
def get_nps_metrics():
    """Get NPS metrics (admin only)"""
    try:
        metrics = feedback_service.get_nps_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({'error': 'Failed to get metrics'}), 500

@feedback_bp.route('/nps/recent', methods=['GET'])
@login_required
def get_recent_feedback():
    """Get recent feedback entries"""
    try:
        limit = request.args.get('limit', 10, type=int)
        recent_feedback = feedback_service.get_recent_feedback(limit)
        
        return jsonify({
            'success': True,
            'feedback': recent_feedback
        })
    except Exception as e:
        return jsonify({'error': 'Failed to get feedback'}), 500

@feedback_bp.route('/nps/should-show', methods=['GET'])
def should_show_nps():
    """Check if NPS prompt should be shown"""
    try:
        interaction_count = request.args.get('interaction_count', 0, type=int)
        user_id = current_user.id if current_user.is_authenticated else 'anonymous'
        
        should_show = feedback_service.should_show_nps_prompt(user_id, interaction_count)
        
        return jsonify({
            'should_show': should_show,
            'interaction_count': interaction_count
        })
    except Exception as e:
        return jsonify({'error': 'Failed to check NPS status'}), 500