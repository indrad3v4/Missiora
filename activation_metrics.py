"""
Activation Metrics System
Tracks the key metric: users who reach Milestone 1 / total sign-ups
Includes instant win tracking for 25% higher activation rates
"""

from datetime import datetime
import json
import os

class ActivationTracker:
    """Centralized activation metrics tracking following industry standards"""
    
    def __init__(self):
        self.metrics_file = 'activation_metrics.json'
        self.load_metrics()
    
    def load_metrics(self):
        """Load existing metrics or initialize"""
        try:
            with open(self.metrics_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                'total_signups': 0,
                'milestone_1_completions': 0,
                'instant_wins': 0,
                'daily_metrics': {},
                'tool_usage': {},
                'session_data': []
            }
    
    def save_metrics(self):
        """Persist metrics to file"""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_signup(self, user_id):
        """Track new user signup for activation rate calculation"""
        self.data['total_signups'] += 1
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.data['daily_metrics']:
            self.data['daily_metrics'][today] = {'signups': 0, 'activations': 0}
        
        self.data['daily_metrics'][today]['signups'] += 1
        self.save_metrics()
    
    def track_milestone_1_completion(self, user_id):
        """Track Milestone 1 completion - key activation metric"""
        self.data['milestone_1_completions'] += 1
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.data['daily_metrics']:
            self.data['daily_metrics'][today] = {'signups': 0, 'activations': 0}
        
        self.data['daily_metrics'][today]['activations'] += 1
        self.save_metrics()
    
    def track_instant_win(self, user_id, task_type):
        """Track instant wins (<5 min tasks) for 25% higher activation"""
        self.data['instant_wins'] += 1
        
        if task_type not in self.data['tool_usage']:
            self.data['tool_usage'][task_type] = 0
        self.data['tool_usage'][task_type] += 1
        
        self.save_metrics()
    
    def get_activation_rate(self):
        """Calculate activation rate: Milestone 1 completions / total signups"""
        if self.data['total_signups'] == 0:
            return 0.0
        
        return (self.data['milestone_1_completions'] / self.data['total_signups']) * 100
    
    def get_daily_activation_rate(self, date=None):
        """Get activation rate for specific day"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date not in self.data['daily_metrics']:
            return 0.0
        
        day_data = self.data['daily_metrics'][date]
        if day_data['signups'] == 0:
            return 0.0
        
        return (day_data['activations'] / day_data['signups']) * 100
    
    def is_meeting_target(self):
        """Check if meeting the 70% activation target"""
        return self.get_activation_rate() >= 70.0

# Global activation tracker instance
activation_tracker = ActivationTracker()