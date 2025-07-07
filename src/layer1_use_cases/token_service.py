"""Token Service Use Case - Manage token consumption and monetization"""

from typing import Dict, Any, Optional
from datetime import datetime
from src.layer0_entities.token import Token
from src.layer0_entities.user import User

class TokenService:
    """Handles token tracking, consumption, and monetization flows"""
    
    def __init__(self):
        # In production, this would use a database gateway
        self.token_data = {}  # user_id -> Token
        
    def get_or_create_token_balance(self, user_id: int) -> Token:
        """Get existing token balance or create new one for user"""
        if user_id not in self.token_data:
            self.token_data[user_id] = Token(user_id=user_id)
        return self.token_data[user_id]
    
    def consume_tokens(self, user_id: int, action: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Consume tokens for a specific action
        Returns success status and current balance
        """
        token = self.get_or_create_token_balance(user_id)
        
        # Check if user can use requested model
        if model and not token.can_use_model(model):
            return {
                'success': False,
                'error': 'model_not_available',
                'message': f'Model {model} requires {self._get_required_tier(model)} tier',
                'balance': token.balance,
                'should_upgrade': True
            }
        
        # Attempt to consume tokens
        success = token.consume_tokens(action)
        
        result = {
            'success': success,
            'balance': token.balance,
            'consumed': token.COSTS.get(action, 1) if success else 0,
            'should_upgrade': token.should_prompt_upgrade()
        }
        
        if not success:
            result['error'] = 'insufficient_tokens'
            result['message'] = 'Not enough tokens for this action'
            result['required'] = token.COSTS.get(action, 1)
        
        return result
    
    def add_tokens(self, user_id: int, amount: int, tier: Optional[str] = None) -> Dict[str, Any]:
        """Add tokens from purchase and optionally upgrade tier"""
        token = self.get_or_create_token_balance(user_id)
        token.add_tokens(amount)
        
        if tier and tier in token.TIERS:
            token.tier = tier
        
        return {
            'success': True,
            'balance': token.balance,
            'tier': token.tier,
            'features_unlocked': token.TIERS.get(token.tier, {}).get('features', [])
        }
    
    def get_token_status(self, user_id: int) -> Dict[str, Any]:
        """Get current token status and recommendations"""
        token = self.get_or_create_token_balance(user_id)
        
        return {
            'balance': token.balance,
            'tier': token.tier,
            'usage_percentage': token.get_usage_percentage(),
            'available_features': token.TIERS.get(token.tier, {}).get('features', []),
            'available_models': token.TIERS.get(token.tier, {}).get('models', []),
            'should_upgrade': token.should_prompt_upgrade(),
            'upgrade_benefits': self._get_upgrade_benefits(token.tier)
        }
    
    def process_payment(self, user_id: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment and add tokens"""
        # In production, this would integrate with payment gateway
        package = payment_data.get('package', 'basic')
        
        packages = {
            'basic': {'tokens': 500, 'price': 5, 'tier': 'basic'},
            'premium': {'tokens': 2000, 'price': 15, 'tier': 'premium'},
            'enterprise': {'tokens': 10000, 'price': 50, 'tier': 'premium'}
        }
        
        if package not in packages:
            return {'success': False, 'error': 'invalid_package'}
        
        pkg = packages[package]
        
        # Simulate payment processing
        # In production: verify payment with Stripe/crypto
        payment_verified = True  
        
        if payment_verified:
            result = self.add_tokens(user_id, pkg['tokens'], pkg['tier'])
            result['package'] = package
            result['price'] = pkg['price']
            return result
        
        return {'success': False, 'error': 'payment_failed'}
    
    def _get_required_tier(self, model: str) -> str:
        """Get minimum tier required for a model"""
        for tier, config in Token.TIERS.items():
            if model in config.get('models', []):
                return tier
        return 'premium'
    
    def _get_upgrade_benefits(self, current_tier: str) -> list:
        """Get benefits of upgrading from current tier"""
        benefits = []
        
        if current_tier == 'free':
            benefits.extend([
                'Access to GPT-4 for advanced responses',
                'Generate detailed roadmaps',
                'Basic AR interactions',
                '500 tokens included'
            ])
        
        if current_tier in ['free', 'basic']:
            benefits.extend([
                'GPT-4 Vision for image analysis',
                'Advanced AR features',
                'Priority support',
                'Unlimited feature access'
            ])
        
        return benefits
    
    def track_instant_win(self, user_id: int) -> Dict[str, Any]:
        """Track instant win achievement (< 5 min task completion)"""
        token = self.get_or_create_token_balance(user_id)
        
        # Reward user with bonus tokens for quick achievement
        bonus = 10
        token.add_tokens(bonus)
        
        return {
            'success': True,
            'bonus_tokens': bonus,
            'message': 'Instant win! Bonus tokens added.',
            'balance': token.balance
        }