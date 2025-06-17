"""Health check tests"""

import pytest
from layer3_frameworks.flask_app import create_app

def test_app_boots():
    """Test that the application boots successfully"""
    app = create_app()
    assert app is not None
    
    with app.test_client() as client:
        # Test that the app responds to requests
        response = client.get('/')
        assert response.status_code < 500

def test_api_endpoints_exist():
    """Test that core API endpoints are registered"""
    app = create_app()
    
    with app.test_client() as client:
        # Test agent interaction endpoint
        response = client.post('/api/agent/interact', 
                             json={'message': 'Hello'},
                             headers={'Content-Type': 'application/json'})
        # Should not return 404 (endpoint exists)
        assert response.status_code != 404
        
        # Test auth status endpoint
        response = client.get('/api/auth/status')
        assert response.status_code != 404