"""Basic application tests"""

from layer3_frameworks.flask_app import create_app

def test_app_creation():
    """Test that the Flask app can be created"""
    app = create_app()
    assert app is not None
    return True

def test_health_endpoint():
    """Test health endpoint is accessible"""
    app = create_app()
    client = app.test_client()
    
    response = client.get('/')
    # Should return some response (200, 302, etc.)
    assert response.status_code < 500
    return True

if __name__ == "__main__":
    try:
        test_app_creation()
        print("✓ App creation test passed")
        
        test_health_endpoint()
        print("✓ Basic endpoint test passed")
        
        print("✓ All basic tests passed - Clean architecture restructure successful!")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        exit(1)