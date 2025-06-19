"""Test API contract endpoints for schema validation"""

import pytest
import requests
import json
from typing import Dict, Any

class TestAPIContracts:
    """Test suite for API endpoint contracts"""
    
    base_url = "http://localhost:5000"
    
    def test_identity_endpoint(self):
        """Test /api/identity endpoint returns correct schema"""
        response = requests.get(f"{self.base_url}/api/identity")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate identity schema
        required_fields = ['name', 'archetype', 'completion']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(data.get('name'), (str, type(None)))
        assert isinstance(data.get('archetype'), (str, type(None)))
        assert isinstance(data.get('completion'), (int, float))
    
    def test_mission_endpoint(self):
        """Test /api/mission endpoint returns correct schema"""
        response = requests.get(f"{self.base_url}/api/mission")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate mission schema
        required_fields = ['goal', 'deadline', 'completion']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(data.get('goal'), (str, type(None)))
        assert isinstance(data.get('deadline'), (str, type(None)))
        assert isinstance(data.get('completion'), (int, float))
    
    def test_roadmap_endpoint(self):
        """Test /api/roadmap endpoint returns correct schema"""
        response = requests.get(f"{self.base_url}/api/roadmap")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate roadmap schema
        required_fields = ['completion', 'current_milestone']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(data.get('completion'), (int, float))
        assert isinstance(data.get('current_milestone'), (str, type(None)))
    
    def test_agent_interact_endpoint(self):
        """Test /api/agent/interact endpoint accepts POST and returns response"""
        payload = {"message": "Hello, this is a test message"}
        response = requests.post(
            f"{self.base_url}/api/agent/interact",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response schema
        required_fields = ['response']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(data.get('response'), str)
        assert len(data.get('response', '')) > 0
    
    def test_roadmap_generate_endpoint(self):
        """Test /api/roadmap/generate endpoint generates proper roadmap"""
        response = requests.post(f"{self.base_url}/api/roadmap/generate")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate generated roadmap schema
        required_fields = ['title', 'description', 'milestones']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate milestones structure
        milestones = data.get('milestones', [])
        assert isinstance(milestones, list)
        assert len(milestones) == 5  # Should always return 5 milestones
        
        for milestone in milestones:
            required_milestone_fields = ['id', 'title', 'description', 'completed', 'active']
            for field in required_milestone_fields:
                assert field in milestone, f"Missing milestone field: {field}"

if __name__ == "__main__":
    # Can be run standalone for basic testing
    test_contracts = TestAPIContracts()
    
    try:
        test_contracts.test_identity_endpoint()
        print("✓ Identity endpoint test passed")
        
        test_contracts.test_mission_endpoint()
        print("✓ Mission endpoint test passed")
        
        test_contracts.test_roadmap_endpoint()
        print("✓ Roadmap endpoint test passed")
        
        test_contracts.test_agent_interact_endpoint()
        print("✓ Agent interact endpoint test passed")
        
        test_contracts.test_roadmap_generate_endpoint()
        print("✓ Roadmap generate endpoint test passed")
        
        print("\n🎉 All API contract tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()