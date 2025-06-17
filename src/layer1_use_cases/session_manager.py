"""Session Manager Use Case - Handle session and user state management"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class SessionManager:
    """Manages user sessions and state persistence"""
    
    def __init__(self):
        self.sessions = {}  # In-memory session storage
        self.session_timeout = timedelta(hours=24)
    
    def create_session(self, user_id: str, initial_data: Dict[str, Any] = None) -> str:
        """Create a new session for a user"""
        session_id = f"session_{user_id}_{datetime.utcnow().timestamp()}"
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_accessed': datetime.utcnow(),
            'data': initial_data or {}
        }
        
        self.sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        
        # Check if session is expired
        if self._is_session_expired(session):
            self.delete_session(session_id)
            return None
            
        # Update last accessed time
        session['last_accessed'] = datetime.utcnow()
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data"""
        session = self.get_session(session_id)
        if not session:
            return False
            
        session['data'].update(data)
        session['last_accessed'] = datetime.utcnow()
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
    
    def get_user_sessions(self, user_id: str) -> list:
        """Get all active sessions for a user"""
        user_sessions = []
        
        for session_id, session in self.sessions.items():
            if session['user_id'] == user_id and not self._is_session_expired(session):
                user_sessions.append({
                    'session_id': session_id,
                    'created_at': session['created_at'],
                    'last_accessed': session['last_accessed']
                })
        
        return user_sessions
    
    def store_conversation_context(self, session_id: str, context: Dict[str, Any]) -> bool:
        """Store conversation context in session"""
        return self.update_session(session_id, {'conversation_context': context})
    
    def get_conversation_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve conversation context from session"""
        session = self.get_session(session_id)
        if session and 'conversation_context' in session['data']:
            return session['data']['conversation_context']
        return None
    
    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """Check if a session is expired"""
        last_accessed = session['last_accessed']
        return datetime.utcnow() - last_accessed > self.session_timeout