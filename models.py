from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # Email made optional for MetaMask users
    password_hash = db.Column(db.String(256), nullable=True)  # Password made optional for MetaMask users
    ethereum_address = db.Column(db.String(42), unique=True, nullable=True)  # Add Ethereum address field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    auth_type = db.Column(db.String(20), default='traditional')  # 'traditional', 'metamask', or 'replit'
    replit_user_id = db.Column(db.String(100), unique=True, nullable=True)  # Replit user ID
    
    # Profile information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    business_name = db.Column(db.String(200))
    business_description = db.Column(db.Text)
    
    # Identity and Mission data
    identity_data = db.Column(db.Text, nullable=True)  # JSON stored identity
    mission_statement = db.Column(db.Text, nullable=True)
    current_goal = db.Column(db.String(500), nullable=True)
    

# Add these fields after the existing User model fields, before # Relationships
    # Identity and Mission data  
    identity_data = db.Column(db.Text, nullable=True)  # JSON stored identity
    mission_statement = db.Column(db.Text, nullable=True)
    current_goal = db.Column(db.String(500), nullable=True)
    
        # Relationships
    conversations = db.relationship('Conversation', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), default="New Conversation")
    section = db.Column(db.String(50), nullable=True)  # identity, mission, roadmap
    context_snapshot = db.Column(db.Text, nullable=True)  # Context at conversation start
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.title}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)  # True if from user, False if from AI
    agent_name = db.Column(db.String(100), nullable=True)  # Which agent responded
    context_used = db.Column(db.Text, nullable=True)  # Context available to agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}>'

class UserGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('goals', lazy=True))
    
    def __repr__(self):
        return f'<UserGoal {self.title}>'

class UserInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source_conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('insights', lazy=True))
    source_conversation = db.relationship('Conversation')
    
    def __repr__(self):
        return f'<UserInsight {self.id}>'

class Milestone(db.Model):
    __tablename__ = 'milestones'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Milestone {self.code}: {self.title}>'

class ContextSession(db.Model):
    """Store user context across all sections for orchestrator memory"""
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
            import json
            return json.loads(self.identity_data)
        return {}
    
    def set_identity(self, data):
        import json
        self.identity_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_mission(self):
        if self.mission_data:
            import json
            return json.loads(self.mission_data)
        return {}
    
    def set_mission(self, data):
        import json
        self.mission_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_full_context(self):
        """Get comprehensive context for AI"""
        import json
        return {
            'identity': self.get_identity(),
            'mission': self.get_mission(),
            'milestone_progress': json.loads(self.milestone_progress) if self.milestone_progress else [],
            'session_data': json.loads(self.session_data) if self.session_data else {},
            'last_updated': self.updated_at.isoformat() if self.updated_at else None
        }
