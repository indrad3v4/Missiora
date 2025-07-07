"""
Direct OpenAI integration for solopreneurs without TensorFlow dependencies.
This module provides agent orchestration using only the OpenAI Python SDK.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional

# Use OpenAI SDK directly
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def assemble_conversation_history(prev_history, new_user_input):
    """
    Combine previous conversation history with the new user input for the next agent run.
    
    Args:
        prev_history: Previous conversation history (list of message dicts or None)
        new_user_input: The new user message
        
    Returns:
        Either the raw user input (if no history) or a list of messages including the new input
    """
    if not prev_history:
        return new_user_input
    
    # If prev_history is a list, append the new message
    if isinstance(prev_history, list):
        return prev_history + [{"role": "user", "content": new_user_input}]
    
    # Otherwise, just return the new input
    return new_user_input

def get_greeting() -> Dict[str, str]:
    """Get the initial greeting message from the orchestrator agent."""
    return {
        "reply": "Hello! I'm your AI companion designed to help you build a business that expresses your whole self. I'm here to help you unify your personal identity with your professional growth. How can I assist you today?",
        "agent_name": "Solopreneur Coach"
    }

def condense(text: str, limit: int = 120) -> str:
    """
    Condense text to a specified word limit, preserving key information.
    
    Args:
        text: The text to condense
        limit: Maximum word count (default: 120 words)
    
    Returns:
        Condensed text that respects the word limit
    """
    words = text.split()
    if len(words) <= limit:
        return text
    
    # Take the first portion and last portion to preserve context
    first_part = words[:limit//2]
    last_part = words[-(limit//2):]
    
    return " ".join(first_part) + " ... " + " ".join(last_part)

def get_agent_response(user_message: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Process a user message through the direct OpenAI integration system.
    
    Args:
        user_message: The message from the user
        conversation_history: List of previous messages in the conversation
    
    Returns:
        Dict containing the agent's reply, agent name, and the updated conversation history
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        # Assemble conversation for the agent
        conversation = assemble_conversation_history(conversation_history, user_message)
        
        # Create the system message for agent orchestration
        system_message = """You are an AI assistant for solopreneurs, designed to help them unify their personal identity with their professional growth.

Your purpose is guided by this insight: "I want to build a business that expresses my whole self, but the world fragments me into disconnected roles and expectations, therefore I need an AI system that helps me unify who I am with how I show up, create, and grow."

Follow these principles:
1. Listen deeply to understand both personal values and professional goals
2. Help identify authentic strengths that can be expressed through business
3. Provide specific, actionable strategies to align personal identity with business growth
4. Recognize when the solopreneur is feeling disconnected and help bridge the gap
5. Encourage reflection on how business decisions reflect or conflict with personal values

Remember:
1. Continue until the solopreneur's query is completely resolved before ending your turn
2. If uncertain, ask clarifying questions rather than making assumptions
3. Plan thoroughly before suggesting actions and reflect on the outcomes"""

        # Prepare messages for API call
        if isinstance(conversation, str):
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": conversation}
            ]
        else:
            messages = [{"role": "system", "content": system_message}] + conversation
        
        # Call OpenAI API with the latest model
        response = client.chat.completions.create(
            model="gpt-4o",  # Using the latest model directly
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )
        
        # Extract the response
        agent_reply = response.choices[0].message.content
        
        # Update conversation history
        updated_history = conversation_history or []
        updated_history.append({"role": "user", "content": user_message})
        updated_history.append({"role": "assistant", "content": agent_reply})
        
        # Condense if too long (keep last 10 messages)
        if len(updated_history) > 10:
            updated_history = updated_history[-10:]
        
        return {
            "reply": agent_reply,
            "agent_name": "Solopreneur Coach",
            "conversation_history": updated_history
        }
        
    except Exception as e:
        logger.error(f"Error in agent response: {e}")
        return {
            "reply": "I'm experiencing some technical difficulties. Could you please try your question again?",
            "agent_name": "System",
            "conversation_history": conversation_history or []
        }