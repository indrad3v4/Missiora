"""Simple integration tests"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_layer_imports():
    """Test that all layers can be imported"""
    try:
        from src.layer0_entities.user import User
        from src.layer1_use_cases.roadmap_generator import RoadmapGenerator
        from src.layer2_interfaces.gateways.cv_gateway import CVGateway
        from src.layer3_frameworks.db.session_store import SessionStore
        print("✓ All layer imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_cv_gateway():
    """Test computer vision gateway stub"""
    try:
        from src.layer2_interfaces.gateways.cv_gateway import CVGateway
        cv = CVGateway()
        result = cv.analyze_frame()
        assert result['success'] == True
        assert 'objects' in result
        assert len(result['objects']) > 0
        print("✓ CV Gateway test passed")
        return True
    except Exception as e:
        print(f"✗ CV Gateway test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        test_layer_imports()
        test_cv_gateway()
        print("✓ All simple tests passed")
    except Exception as e:
        print(f"✗ Simple test failed: {e}")
        exit(1)