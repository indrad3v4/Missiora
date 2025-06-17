"""Session store persistence tests"""

import os
import tempfile
from layer3_frameworks.db.session_store import SessionStore

def test_session_store_persistence():
    """Test that session data persists correctly"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        store = SessionStore(tmp.name)
        
        # Store conversation history
        store.update_conversation_history('user123', {
            'user': 'Hello, I need help with my business',
            'agent': 'I'd be happy to help you with your business needs.'
        })
        
        # Store user data
        store.store_user_data('user123', 'preferences', {'theme': 'dark', 'notifications': True})
        
        # Create new store instance (simulates app restart)
        store2 = SessionStore(tmp.name)
        
        # Verify data persists
        history = store2.get_conversation_history('user123')
        assert len(history) == 1
        assert history[0]['user'] == 'Hello, I need help with my business'
        
        preferences = store2.get_user_data('user123', 'preferences')
        assert preferences['theme'] == 'dark'
        assert preferences['notifications'] == True
        
        # Cleanup
        os.unlink(tmp.name)

def test_conversation_history_limits():
    """Test that conversation history respects size limits"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        store = SessionStore(tmp.name)
        
        # Add more than 50 message pairs
        for i in range(60):
            store.update_conversation_history('user123', {
                'user': f'Message {i}',
                'agent': f'Response {i}'
            })
        
        # Should keep only last 50
        history = store.get_conversation_history('user123')
        assert len(history) == 50
        assert history[0]['user'] == 'Message 10'  # First kept message
        assert history[-1]['user'] == 'Message 59'  # Last message
        
        # Cleanup
        os.unlink(tmp.name)