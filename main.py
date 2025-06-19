#!/usr/bin/env python3

"""
Main application entry point for Missiora Agency.
Supports both Flask and FastAPI/Uvicorn based on environment.
"""

import os
from src.layer3_frameworks.flask_app import create_app

# Check environment to determine server type
MISSIORA_ENV = os.environ.get('MISSIORA_ENV', 'production')

def create_application():
    """Create Flask application"""
    return create_app()

app = create_application()

if __name__ == "__main__":
    if MISSIORA_ENV == 'dev':
        # Development mode with Uvicorn (FastAPI integration)
        try:
            import uvicorn
            from fastapi import FastAPI
            from fastapi.middleware.wsgi import WSGIMiddleware
            
            # Create FastAPI wrapper
            fastapi_app = FastAPI(title="Missiora Agency API")
            fastapi_app.mount("/", WSGIMiddleware(app))
            
            uvicorn.run(
                "main:fastapi_app",
                host="0.0.0.0",
                port=5000,
                reload=True,
                log_level="info"
            )
        except ImportError:
            # Fallback to Flask dev server
            app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        # Production mode with Flask
        app.run(host="0.0.0.0", port=5000, debug=False)
