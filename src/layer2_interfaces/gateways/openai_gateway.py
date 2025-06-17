"""OpenAI Gateway - Interface to OpenAI Agents SDK"""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI

class OpenAIGateway:
    """Gateway for OpenAI API interactions"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.default_model = "gpt-4o"
    
    def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
        """Get chat completion from OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                'success': True,
                'reply': response.choices[0].message.content,
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'reply': 'I apologize, but I encountered an issue processing your request.'
            }
    
    def analyze_text(self, text: str, analysis_type: str = "sentiment") -> Dict[str, Any]:
        """Analyze text using OpenAI"""
        prompt = self._get_analysis_prompt(analysis_type, text)
        
        messages = [
            {"role": "system", "content": "You are an expert text analyst."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)
    
    def _get_analysis_prompt(self, analysis_type: str, text: str) -> str:
        """Get analysis prompt based on type"""
        prompts = {
            "sentiment": f"Analyze the sentiment of this text and provide insights: {text}",
            "identity": f"Extract identity characteristics from this text: {text}",
            "mission": f"Analyze the mission clarity and purpose in this text: {text}",
            "strategy": f"Provide strategic insights for this business context: {text}"
        }
        return prompts.get(analysis_type, f"Analyze this text: {text}")