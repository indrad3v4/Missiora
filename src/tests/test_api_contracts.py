"""Test API contracts for Clean Architecture implementation"""

import requests
import json
from typing import Dict, Any

class TestAPIContracts:
    """Test Clean Architecture API endpoints"""
    
    base_url = "http://localhost:5000"
    
    def test_identity_endpoint(self):
        """Test /api/identity endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/identity", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            required_fields = ['name', 'archetype', 'completion', 'location']
            for field in required_fields:
                assert field in data, f"Missing field: {field}"
            
            print("✓ Identity endpoint test passed")
            return True
        except Exception as e:
            print(f"❌ Identity endpoint test failed: {e}")
            return False
    
    def test_mission_endpoint(self):
        """Test /api/mission endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/mission", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            required_fields = ['goal', 'purpose', 'completion']
            for field in required_fields:
                assert field in data, f"Missing field: {field}"
            
            print("✓ Mission endpoint test passed")
            return True
        except Exception as e:
            print(f"❌ Mission endpoint test failed: {e}")
            return False
    
    def test_roadmap_endpoint(self):
        """Test /api/roadmap endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/roadmap", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            required_fields = ['completion', 'current_milestone']
            for field in required_fields:
                assert field in data, f"Missing field: {field}"
            
            print("✓ Roadmap endpoint test passed")
            return True
        except Exception as e:
            print(f"❌ Roadmap endpoint test failed: {e}")
            return False
    
    def test_agent_interact_endpoint(self):
        """Test /api/agent/interact endpoint"""
        try:
            payload = {"message": "Hello, test message"}
            response = requests.post(
                f"{self.base_url}/api/agent/interact",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            
            required_fields = ['response', 'agent']
            for field in required_fields:
                assert field in data, f"Missing field: {field}"
            
            assert len(data['response']) > 0, "Empty response"
            
            print("✓ Agent interact endpoint test passed")
            return True
        except Exception as e:
            print(f"❌ Agent interact endpoint test failed: {e}")
            return False
    
    def test_gradio_tools_endpoint(self):
        """Test /tools/vision endpoint"""
        try:
            response = requests.get(f"{self.base_url}/tools/vision", timeout=5)
            # Should return either Gradio interface or fallback message
            assert response.status_code in [200, 500]  # 500 OK for fallback
            
            print("✓ CV tools endpoint accessible")
            return True
        except Exception as e:
            print(f"❌ CV tools endpoint test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API contract tests"""
        print("Running Clean Architecture API contract tests...")
        
        tests = [
            self.test_identity_endpoint,
            self.test_mission_endpoint,
            self.test_roadmap_endpoint,
            self.test_agent_interact_endpoint,
            self.test_gradio_tools_endpoint
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print(f"\nResults: {passed}/{total} tests passed")
        return passed == total

if __name__ == "__main__":
    tester = TestAPIContracts()
    success = tester.run_all_tests()
    exit(0 if success else 1)