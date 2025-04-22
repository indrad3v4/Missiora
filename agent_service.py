import os
import logging
from openai import OpenAI
from config import Config

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def get_agent_response(user_message, message_history=None, user_info=None):
    """
    Get a response from the OpenAI API based on the user's message and conversation history.
    
    Args:
        user_message (str): The user's message
        message_history (list, optional): Previous messages in the conversation
        user_info (dict, optional): User profile information for context
    
    Returns:
        str: The agent's response
    """
    try:
        # Create system prompt with user information if available
        system_prompt = Config.SYSTEM_PROMPT
        if user_info:
            user_context = f"""
            User information:
            Name: {user_info.get('first_name', '')} {user_info.get('last_name', '')}
            Business: {user_info.get('business_name', '')}
            Business description: {user_info.get('business_description', '')}
            Bio: {user_info.get('bio', '')}
            """
            system_prompt = f"{system_prompt}\n\nContext about this solopreneur:{user_context}"
        
        # Create message list for OpenAI API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add message history if available
        if message_history:
            for msg in message_history:
                if isinstance(msg, dict) and 'content' in msg:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    messages.append({"role": role, "content": content})
                else:
                    # Handle legacy message format if needed
                    is_user = getattr(msg, 'is_user', True)
                    content = getattr(msg, 'content', str(msg))
                    role = "user" if is_user else "assistant"
                    messages.append({"role": role, "content": content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=Config.DEFAULT_AGENT_MODEL,  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return response content
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error in get_agent_response: {e}")
        return f"I apologize, but I encountered an error while processing your request. Please try again later. (Error: {str(e)})"
