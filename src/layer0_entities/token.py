"""Token Entity - Token-based monetization tracking"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Token:
    """Token balance and usage tracking for monetization"""
    user_id: int
    balance: int = 100  # Starting free tokens
    total_consumed: int = 0
    total_purchased: int = 0
    tier: str = 'free'  # free, basic, premium
    last_purchase: Optional[datetime] = None
    last_usage: Optional[datetime] = None
    
    # Token costs
    COSTS = {
        'agent_query': 1,
        'agent_query_premium': 3,
        'vision_analysis': 5,
        'roadmap_generation': 10,
        'mission_generation': 5,
        'ar_interaction': 2
    }
    
    # Tier benefits
    TIERS = {
        'free': {
            'models': ['gpt-3.5-turbo'],
            'features': ['basic_agent', 'identity', 'mission']
        },
        'basic': {
            'models': ['gpt-3.5-turbo', 'gpt-4'],
            'features': ['basic_agent', 'identity', 'mission', 'roadmap', 'ar_basic']
        },
        'premium': {
            'models': ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-vision-preview'],
            'features': ['all']
        }
    }
    
    def consume_tokens(self, action: str, amount: Optional[int] = None) -> bool:
        """Consume tokens for an action. Returns True if successful."""
        cost = amount or self.COSTS.get(action, 1)
        
        if self.balance >= cost:
            self.balance -= cost
            self.total_consumed += cost
            self.last_usage = datetime.utcnow()
            return True
        return False
    
    def add_tokens(self, amount: int):
        """Add tokens to balance (from purchase)"""
        self.balance += amount
        self.total_purchased += amount
        self.last_purchase = datetime.utcnow()
    
    def can_use_feature(self, feature: str) -> bool:
        """Check if user's tier allows feature access"""
        tier_features = self.TIERS.get(self.tier, {}).get('features', [])
        return feature in tier_features or 'all' in tier_features
    
    def can_use_model(self, model: str) -> bool:
        """Check if user's tier allows model access"""
        tier_models = self.TIERS.get(self.tier, {}).get('models', [])
        return model in tier_models
    
    def should_prompt_upgrade(self) -> bool:
        """Determine if user should see upgrade prompt"""
        # Prompt when balance is low or user tries premium features
        return self.balance < 20 and self.tier == 'free'
    
    def get_usage_percentage(self) -> float:
        """Get percentage of tokens used vs. total acquired"""
        total_acquired = 100 + self.total_purchased  # Initial + purchased
        if total_acquired == 0:
            return 0
        return (self.total_consumed / total_acquired) * 100