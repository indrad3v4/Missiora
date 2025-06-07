
# Enhanced models for context-aware orchestrator

from app import db
from datetime import datetime
import json

class ContextSession(db.Model):
    """Store user context across all sections"""
    __tablename__ = 'context_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    session_data = db.Column(db.Text, nullable=True)  # JSON stored context
    identity_data = db.Column(db.Text, nullable=True)  # JSON identity info
    mission_data = db.Column(db.Text, nullable=True)   # JSON mission info
    milestone_progress = db.Column(db.Text, nullable=True)  # JSON milestone status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_identity(self):
        if self.identity_data:
            return json.loads(self.identity_data)
        return {}
    
    def set_identity(self, data):
        self.identity_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_mission(self):
        if self.mission_data:
            return json.loads(self.mission_data)
        return {}
    
    def set_mission(self, data):
        self.mission_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_full_context(self):
        """Get comprehensive context for AI"""
        return {
            'identity': self.get_identity(),
            'mission': self.get_mission(),
            'milestone_progress': json.loads(self.milestone_progress) if self.milestone_progress else [],
            'session_data': json.loads(self.session_data) if self.session_data else {},
            'last_updated': self.updated_at.isoformat() if self.updated_at else None
        }

# Add section field to existing Conversation model
class EnhancedConversation(db.Model):
    """Enhanced conversation with section context"""
    __tablename__ = 'enhanced_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(50), nullable=False)  # identity, mission, roadmap
    title = db.Column(db.String(200), default="Section Discussion")
    context_snapshot = db.Column(db.Text, nullable=True)  # Context at conversation start
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('EnhancedMessage', backref='conversation', lazy=True, cascade="all, delete-orphan")

class EnhancedMessage(db.Model):
    """Enhanced message with agent context"""
    __tablename__ = 'enhanced_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('enhanced_conversations.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    agent_name = db.Column(db.String(100), nullable=True)  # Which agent responded
    context_used = db.Column(db.Text, nullable=True)  # Context available to agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
