"""
OpenAI Agents SDK implementation for the AI Agency for Solopreneurs.
This module provides the agent orchestration logic using OpenAI's API directly.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import json

# Import the OpenAI client
from openai import OpenAI

# Use agent service instead of unavailable agents SDK
from agent_service import get_agent_response as agent_service_response, get_milestone_context

# Import project config
from config import Config

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def assemble_conversation_history(prev_history, new_user_input):
    """
    Combine previous conversation history with the new user input for the next agent run.
    
    Args:
        prev_history: Previous conversation history (list of message dicts or None)
        new_user_input: The new user message
        
    Returns:
        Either the raw user input (if no history) or a list of messages including the new input
    """
    if prev_history:
        # prev_history is a list of message dicts
        return prev_history + [{"role": "user", "content": new_user_input}]
    else:
        # If no prior history, create a new conversation
        return [{"role": "user", "content": new_user_input}]

def get_greeting() -> Dict[str, str]:
    """Get the initial greeting message from the orchestrator agent."""
    opening_line = "Welcome, solopreneur. What are you creating — and what's holding you back?"
    return {
        "reply": opening_line,
        "agent": "OrchestratorAgent"
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
    if len(text.split()) <= limit:  # already short
        return text
    
    # simple heuristic: keep first 2 sentences + final sentence
    parts = text.split('. ')
    if len(parts) > 2:
        short = '. '.join(parts[:2] + parts[-1:])
    else:
        short = text
    return short[:limit*6] + '…' if len(short) > limit*6 else short

def get_agent_response(user_message: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Process a user message through the agent orchestration system.
    
    Args:
        user_message: The message from the user
        conversation_history: List of previous messages in the conversation
    
    Returns:
        Dict containing the agent's reply, agent name, and the updated conversation history
    """
    try:
        # Limit message length to prevent token issues
        if user_message and len(user_message) > 500:
            user_message = user_message[:500] + "..."
        
        # Use the existing agent service function
        response = agent_service_response(user_message, conversation_history)
        
        # If agent_service_response returns a string, wrap it in the expected format
        if isinstance(response, str):
            assistant_reply = condense(response)
            agent_name = "OrchestratorAgent"
            new_history = assemble_conversation_history(conversation_history, user_message)
            new_history.append({"role": "assistant", "content": assistant_reply})
        else:
            # If it returns a dict, use its structure
            assistant_reply = condense(response.get("reply", response.get("content", str(response))))
            agent_name = response.get("agent", "OrchestratorAgent")
            new_history = response.get("conversation_history", 
                                     assemble_conversation_history(conversation_history, user_message))
            if new_history and new_history[-1].get("role") != "assistant":
                new_history.append({"role": "assistant", "content": assistant_reply})
        
        return {
            "reply": assistant_reply,
            "agent": agent_name,
            "conversation_history": new_history
        }
        
    except Exception as e:
        logger.error(f"Error in get_agent_response: {e}")
        
        # Fallback to direct OpenAI call
        try:
            messages = [
                {
                    "role": "system",
                    "content": Config.SYSTEM_PROMPT
                }
            ]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            response = client.chat.completions.create(
                model=Config.DEFAULT_AGENT_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_reply = condense(response.choices[0].message.content)
            new_history = assemble_conversation_history(conversation_history, user_message)
            new_history.append({"role": "assistant", "content": assistant_reply})
            
            return {
                "reply": assistant_reply,
                "agent": "OrchestratorAgent",
                "conversation_history": new_history
            }
            
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
            return {
                "reply": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
                "agent": "OrchestratorAgent",
                "conversation_history": conversation_history or []
            }