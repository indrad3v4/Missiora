from flask import session
from app import app, db
from replit_auth import require_login, make_replit_blueprint
from flask_login import current_user

app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    """Main application entry point"""
    return render_template('app.html')

@app.route('/app')
def app_interface():
    """Main app interface - handles both auth states"""
    guest_mode = request.args.get('guest') == 'true'
    if current_user.is_authenticated or guest_mode:
        return render_template('index.html')
    else:
        return redirect(url_for('replit_auth.login'))

# Add remaining routes from the original file with fixed syntax
