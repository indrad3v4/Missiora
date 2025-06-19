"""Run all tests for Missiora project"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_tests():
    """Run all available tests"""
    print("Running Missiora test suite...")
    
    # Test 1: Disk usage guard
    from test_disk_usage import test_disk_usage
    disk_ok = test_disk_usage()
    
    # Test 2: Import smoke tests
    try:
        print("\nTesting imports...")
        from layer0_entities.user import User
        from layer1_use_cases.agent_orchestrator import AgentOrchestrator
        from layer2_interfaces.gateways.cv_gateway import CVGateway
        from layer3_frameworks.flask_app import create_app
        print("✓ All critical imports successful")
        import_ok = True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import_ok = False
    
    # Test 3: Flask app creation
    try:
        print("\nTesting Flask app creation...")
        app = create_app()
        print("✓ Flask app created successfully")
        app_ok = True
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        app_ok = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST RESULTS:")
    print(f"Disk usage: {'PASS' if disk_ok else 'FAIL'}")
    print(f"Imports: {'PASS' if import_ok else 'FAIL'}")
    print(f"Flask app: {'PASS' if app_ok else 'FAIL'}")
    
    all_passed = disk_ok and import_ok and app_ok
    print(f"Overall: {'PASS' if all_passed else 'FAIL'}")
    
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)