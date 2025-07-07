"""Token Controller - API endpoints for token management"""

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from src.layer1_use_cases.token_service import TokenService

token_bp = Blueprint('token', __name__, url_prefix='/api/token')
token_service = TokenService()

@token_bp.route('/status', methods=['GET'])
@login_required
def get_token_status():
    """Get current token balance and status"""
    try:
        status = token_service.get_token_status(current_user.id)
        return jsonify(status), 200
    except Exception as e:
        current_app.logger.error(f"Error getting token status: {str(e)}")
        return jsonify({'error': 'Failed to get token status'}), 500

@token_bp.route('/consume', methods=['POST'])
@login_required
def consume_tokens():
    """Consume tokens for an action"""
    try:
        data = request.get_json()
        action = data.get('action', 'agent_query')
        model = data.get('model')
        
        result = token_service.consume_tokens(current_user.id, action, model)
        
        if not result['success']:
            return jsonify(result), 402  # Payment Required
            
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Error consuming tokens: {str(e)}")
        return jsonify({'error': 'Failed to consume tokens'}), 500

@token_bp.route('/purchase', methods=['POST'])
@login_required
def purchase_tokens():
    """Process token purchase"""
    try:
        payment_data = request.get_json()
        
        # Validate payment data
        if not payment_data or 'package' not in payment_data:
            return jsonify({'error': 'Invalid payment data'}), 400
        
        result = token_service.process_payment(current_user.id, payment_data)
        
        if not result['success']:
            return jsonify(result), 400
            
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Error processing payment: {str(e)}")
        return jsonify({'error': 'Payment processing failed'}), 500

@token_bp.route('/packages', methods=['GET'])
def get_token_packages():
    """Get available token packages"""
    packages = [
        {
            'id': 'basic',
            'name': 'Basic Package',
            'tokens': 500,
            'price': 5,
            'currency': 'EUR',
            'tier': 'basic',
            'features': [
                'Access to GPT-4',
                'Generate roadmaps',
                'Basic AR features'
            ]
        },
        {
            'id': 'premium',
            'name': 'Premium Package',
            'tokens': 2000,
            'price': 15,
            'currency': 'EUR',
            'tier': 'premium',
            'features': [
                'All Basic features',
                'GPT-4 Vision access',
                'Advanced AR interactions',
                'Priority support'
            ]
        },
        {
            'id': 'enterprise',
            'name': 'Enterprise Package',
            'tokens': 10000,
            'price': 50,
            'currency': 'EUR',
            'tier': 'premium',
            'features': [
                'All Premium features',
                'Bulk token discount',
                'Custom integrations',
                'Dedicated support'
            ]
        }
    ]
    
    return jsonify({'packages': packages}), 200

@token_bp.route('/instant-win', methods=['POST'])
@login_required
def track_instant_win():
    """Track instant win achievement"""
    try:
        result = token_service.track_instant_win(current_user.id)
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Error tracking instant win: {str(e)}")
        return jsonify({'error': 'Failed to track achievement'}), 500