from datetime import datetime
from layer3_frameworks.flask_app import db
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Conversation {self.id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)  # True if from user, False if from AI
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
        return f'<Milestone {self.code}>'

# Add these fields to User model for agent state tracking
    agent_stage = db.Column(db.String(20), default='seed')
    completion_data = db.Column(db.Text, nullable=True)  # JSON stored completion data
    last_agent_interaction = db.Column(db.DateTime, default=datetime.utcnow)

# Add these fields to User model for agent state tracking
    agent_stage = db.Column(db.String(20), default='seed')
    completion_data = db.Column(db.Text, nullable=True)  # JSON stored completion data
    last_agent_interaction = db.Column(db.DateTime, default=datetime.utcnow)

# Add these fields to User model for agent state tracking
    agent_stage = db.Column(db.String(20), default='seed')
    completion_data = db.Column(db.Text, nullable=True)  # JSON stored completion data
    last_agent_interaction = db.Column(db.DateTime, default=datetime.utcnow)
