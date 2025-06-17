"""Agent Output Presenter - Formats agent responses for UI"""

from typing import Dict, Any, List, Optional

class AgentOutputPresenter:
    """Formats AI agent outputs for frontend consumption"""
    
    def present_agent_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Present agent response for UI consumption"""
        return {
            'reply': self._sanitize_reply(response.get('reply', '')),
            'agent': response.get('agent', 'orchestrator'),
            'confidence': response.get('confidence', 0.8),
            'suggestions': response.get('suggestions', []),
            'next_actions': response.get('next_actions', []),
            'metadata': self._extract_metadata(response)
        }
    
    def present_conversation_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Present conversation history for UI"""
        formatted_history = []
        
        for entry in history:
            formatted_entry = {
                'timestamp': entry.get('timestamp'),
                'role': entry.get('role', 'user'),
                'content': self._sanitize_reply(entry.get('content', '')),
                'agent': entry.get('agent', 'user')
            }
            formatted_history.append(formatted_entry)
        
        return formatted_history
    
    def present_agent_status(self, agent_name: str, status: Dict[str, Any]) -> Dict[str, Any]:
        """Present agent status information"""
        return {
            'name': agent_name,
            'status': status.get('status', 'ready'),
            'last_active': status.get('last_active'),
            'capabilities': status.get('capabilities', []),
            'current_task': status.get('current_task')
        }
    
    def _sanitize_reply(self, reply: str) -> str:
        """Sanitize agent reply for safe UI display"""
        if not reply:
            return ''
        
        # Remove any potential script tags or dangerous HTML
        import re
        # Basic HTML tag removal - in production, use a proper HTML sanitizer
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', reply, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        
        return sanitized.strip()
    
    def _extract_metadata(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from agent response"""
        metadata = {}
        
        # Extract conversation history if present
        if 'conversation_history' in response:
            metadata['conversation_length'] = len(response['conversation_history'])
        
        # Extract agent performance metrics if present
        if 'processing_time' in response:
            metadata['processing_time'] = response['processing_time']
        
        # Extract any tool usage information
        if 'tools_used' in response:
            metadata['tools_used'] = response['tools_used']
        
        return metadata