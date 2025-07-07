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
    
    # Register Clean Architecture controllers
    try:
        from ...layer2_interfaces.controllers.identity_controller import identity_bp
        from ...layer2_interfaces.controllers.mission_controller import mission_bp
        from ...layer2_interfaces.controllers.roadmap_controller import roadmap_bp
        from ...layer2_interfaces.controllers.agent_controller import agent_bp
        from ...layer2_interfaces.controllers.cv_controller import cv_bp
        from ...layer2_interfaces.controllers.token_controller import token_bp
        
        app.register_blueprint(identity_bp)
        app.register_blueprint(mission_bp)
        app.register_blueprint(roadmap_bp)
        app.register_blueprint(agent_bp)
        app.register_blueprint(cv_bp)
        app.register_blueprint(token_bp)
        
        app.logger.info("Clean Architecture controllers registered successfully")
    except Exception as e:
        app.logger.warning(f"Failed to register Clean Architecture controllers: {e}")
    
    # Keep simple API for backward compatibility
    try:
        from .simple_api import simple_api_bp
        app.register_blueprint(simple_api_bp, url_prefix='/api/legacy')
    except ImportError:
        pass
    
    # Mount Gradio CV tools in Flask process
    try:
        import gradio as gr
        from ..gradio_app.interface import create_cv_interface
        
        # Create Gradio interface
        cv_interface = create_cv_interface()
        
        # Mount Gradio app at /tools/vision
        gradio_app = gr.mount_gradio_app(app, cv_interface, path="/tools/vision")
        
        app.logger.info("Gradio CV tools mounted at /tools/vision")
        
    except ImportError as e:
        app.logger.warning(f"Gradio not available: {e}")
        
        # Fallback route when Gradio not installed
        @app.route('/tools/vision')
        def cv_tools_fallback():
            """Fallback when Gradio not available"""
            return """
            <!DOCTYPE html>
            <html><head><title>CV Tools</title></head>
            <body>
            <h1>Computer Vision Tools</h1>
            <p>Gradio CV tools not available. Install with:</p>
            <code>pip install gradio transformers pillow</code>
            </body>
            </html>
            """
    except Exception as e:
        app.logger.error(f"Failed to mount Gradio: {e}")
        
        @app.route('/tools/vision')
        def cv_tools_error():
            return f"CV Tools Error: {str(e)}", 500
    
    # Serve Vue frontend
    vue_dist_path = os.path.join(os.path.dirname(__file__), '..', 'vue_frontend', 'dist')
    
    if os.path.exists(os.path.join(vue_dist_path, 'index.html')):
        # Serve built Vue SPA
        from flask import send_from_directory, send_file
        
        @app.route('/')
        def index():
            """Serve Vue SPA index.html"""
            return send_file(os.path.join(vue_dist_path, 'index.html'))
        
        @app.route('/assets/<path:filename>')
        def vue_assets(filename):
            """Serve Vue SPA assets"""
            return send_from_directory(os.path.join(vue_dist_path, 'assets'), filename)
        
        @app.route('/<path:path>')
        def catch_all(path):
            """Catch-all route for Vue SPA routing"""
            # For SPA routing, return index.html for all non-API routes
            if not path.startswith('api/') and not path.startswith('tools/'):
                return send_file(os.path.join(vue_dist_path, 'index.html'))
            else:
                return "Not found", 404
    else:
        @app.route('/')
        def index():
            """Fallback when Vue build not found"""
            return """
            <!DOCTYPE html>
            <html><head><title>Missiora Agency</title></head>
            <body><h1>Missiora Agency</h1><p>Vue build not found - run npm run build in src/layer3_frameworks/vue_frontend</p></body>
            </html>
            """
    
    # Import legacy routes for compatibility (register with prefix to avoid conflicts)
    try:
        from .legacy_routes import legacy_bp
        app.register_blueprint(legacy_bp, url_prefix='/legacy')
    except ImportError:
        pass
    
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