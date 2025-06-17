"""Session storage for persisting conversation history"""

import json
import os
from typing import List, Dict, Any, Optional

class SessionStore:
    """Persistent session storage for conversation history"""
    
    def __init__(self, storage_file: str = "instance/session_store.json"):
        self.storage_file = storage_file
        self._ensure_storage_dir()
        self._load_storage()
    
    def _ensure_storage_dir(self):
        """Ensure storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
    
    def _load_storage(self):
        """Load storage from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    self._storage = json.load(f)
            else:
                self._storage = {}
        except (json.JSONDecodeError, FileNotFoundError):
            self._storage = {}
    
    def _save_storage(self):
        """Save storage to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self._storage, f, indent=2)
        except Exception as e:
            print(f"Failed to save session storage: {e}")
    
    def get_conversation_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        return self._storage.get(f"conversation_{user_id}", [])
    
    def update_conversation_history(self, user_id: str, message_pair: Dict[str, str]):
        """Add a new message pair to conversation history"""
        key = f"conversation_{user_id}"
        if key not in self._storage:
            self._storage[key] = []
        
        self._storage[key].append(message_pair)
        
        # Keep only last 50 message pairs to prevent unbounded growth
        if len(self._storage[key]) > 50:
            self._storage[key] = self._storage[key][-50:]
        
        self._save_storage()
    
    def clear_conversation_history(self, user_id: str):
        """Clear conversation history for a user"""
        key = f"conversation_{user_id}"
        if key in self._storage:
            del self._storage[key]
            self._save_storage()
    
    def store_user_data(self, user_id: str, data_key: str, data_value: Any):
        """Store arbitrary user data"""
        key = f"user_{user_id}_{data_key}"
        self._storage[key] = data_value
        self._save_storage()
    
    def get_user_data(self, user_id: str, data_key: str, default: Any = None) -> Any:
        """Get user data"""
        key = f"user_{user_id}_{data_key}"
        return self._storage.get(key, default)
    
    def get_all_keys(self) -> List[str]:
        """Get all storage keys for debugging"""
        return list(self._storage.keys())