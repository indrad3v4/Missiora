"""Flask Application Factory"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app(config_name='default'):
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///solopreneur_agency.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'legacy.login'
    
    # Set up OpenAI API key
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
    
    # Register blueprints (with error handling for missing dependencies)
    try:
        from ...layer2_interfaces.controllers.onboarding_controller import onboarding_bp
        app.register_blueprint(onboarding_bp)
    except ImportError:
        app.logger.warning("Onboarding controller not available")
    
    try:
        from ...layer2_interfaces.controllers.agent_controller import agent_bp
        app.register_blueprint(agent_bp)
    except ImportError:
        app.logger.warning("Agent controller not available")
        
    try:
        from ...layer2_interfaces.controllers.milestone_controller import milestone_bp
        app.register_blueprint(milestone_bp)
    except ImportError:
        app.logger.warning("Milestone controller not available")
    
    try:
        from ...layer2_interfaces.controllers.feedback_controller import feedback_bp
        app.register_blueprint(feedback_bp)
    except ImportError:
        app.logger.warning("Feedback controller not available")
    
    try:
        from ...layer2_interfaces.controllers.auth_controller import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError:
        app.logger.warning("Auth controller not available")
    
    # Register simple API for Vue frontend
    from .simple_api import simple_api_bp
    app.register_blueprint(simple_api_bp)
    
    # Import legacy routes for compatibility (register with prefix to avoid conflicts)
    from .legacy_routes import legacy_bp
    app.register_blueprint(legacy_bp, url_prefix='/legacy')
    
    # Create database tables
    with app.app_context():
        from ..db.models import User, Conversation, Message, UserGoal, UserInsight, Milestone
        db.create_all()
    
    # Serve Vue SPA for all non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_spa(path=''):
        """Serve Vue.js SPA for all routes except API"""
        from flask import send_from_directory, abort
        import os
        
        # Don't serve SPA for API routes
        if path.startswith('api/'):
            abort(404)
            
        # Path to Vue dist directory
        vue_dist = os.path.join(app.root_path, '../vue_frontend/dist')
        
        # If dist directory exists, serve from it
        if os.path.exists(vue_dist):
            # Try to serve the specific file first
            if path and os.path.exists(os.path.join(vue_dist, path)):
                return send_from_directory(vue_dist, path)
            # Otherwise serve index.html for SPA routing
            return send_from_directory(vue_dist, 'index.html')
        else:
            # Fallback to basic HTML if Vue build not available
            return '''<!DOCTYPE html>
<html><head><title>Missiora Agency</title></head>
<body><h1>Missiora Agency</h1><p>Vue frontend not built yet. Run: npm run build</p></body>
</html>'''
    
    # Import health check and auth blueprints (with error handling)
    try:
        from ..health_check import health_bp
        app.register_blueprint(health_bp, url_prefix="/health")
    except ImportError:
        app.logger.warning("Health check blueprint not available")
        
    try:
        from ..replit_auth import make_replit_blueprint
        app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")
    except ImportError:
        app.logger.warning("Replit auth blueprint not available")
    
    # User loader
    from ..db.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app