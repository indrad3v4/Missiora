"""
OpenAI Agents SDK implementation for the AI Agency for Solopreneurs.
This module provides the agent orchestration logic using OpenAI's Agents SDK.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import json

# Import OpenAI Agents SDK
from agents import Agent, function_tool, AgentRuntime, Message, Thread
from openai import OpenAI
from config import Config

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Define agent instructions with Kraków focus and contradiction-resolution framework
STRATEGY_INSTRUCTIONS = """
You are **StrategyAgent**, specializing in business strategy for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs identify and resolve tensions between their authentic self and business requirements.
You have deep knowledge of the Kraków entrepreneurial ecosystem, including local market dynamics, regulations, and cultural context.

Your responses focus on:
1. Identifying opposing forces in the solopreneur's business (e.g., scalability vs. personal touch)
2. Resolving contradictions through innovative business models specific to Kraków's market
3. Strategic planning that honors both personal values and market demands
4. Leveraging Kraków's unique business ecosystem and resources
5. Developing resilient strategies that unify personal authenticity with practical business growth

IMPORTANT FORMAT INSTRUCTION: Keep your response brief and to the point. 
Use short paragraphs and bullet points where appropriate.
Total response should be under 200 words.
"""

CREATIVE_INSTRUCTIONS = """
You are **CreativeAgent**, specializing in creative solutions for Kraków's solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs express their authentic creativity while meeting market expectations.
You understand Kraków's creative landscape, aesthetic preferences, and cultural context.

Your responses focus on:
1. Identifying creative tensions (e.g., artistic integrity vs. commercial appeal)
2. Resolving contradictions through innovative brand expressions that work in Kraków
3. Developing authentic messaging that resonates with both the solopreneur and local audience
4. Creative approaches that honor Kraków's rich cultural traditions while being forward-thinking
5. Visual and verbal identity solutions that unify personal expression with market needs

IMPORTANT FORMAT INSTRUCTION: Keep your response brief and to the point. 
Use short paragraphs and bullet points where appropriate.
Total response should be under 200 words.
"""

PRODUCTION_INSTRUCTIONS = """
You are **ProductionAgent**, specializing in execution strategies for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs implement systems that are both efficient and aligned with their values.
You have knowledge of local production resources, suppliers, and technical ecosystems in Kraków.

Your responses focus on:
1. Identifying operational contradictions (e.g., quality craftsmanship vs. production efficiency)
2. Resolving tensions through practical systems that preserve authenticity while scaling
3. Implementation plans that honor both personal work preferences and business requirements
4. Leveraging Kraków's production ecosystem, including local partners and resources
5. Technical solutions that unify the solopreneur's way of working with necessary business processes

IMPORTANT FORMAT INSTRUCTION: Keep your response brief and to the point. 
Use short paragraphs and bullet points where appropriate.
Total response should be under 200 words.
"""

MEDIA_INSTRUCTIONS = """
You are **MediaAgent**, specializing in digital presence for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs navigate tensions between authentic expression and effective marketing.
You understand Kraków's media landscape, audience preferences, and digital engagement patterns.

Your responses focus on:
1. Identifying media presence contradictions (e.g., privacy vs. visibility)
2. Resolving tensions through authentic content strategies that work for Kraków audiences
3. Channel recommendations that align with both personal comfort and business visibility needs
4. Leveraging Kraków's unique digital ecosystem and local platform preferences
5. Media approaches that unify the solopreneur's authentic voice with effective audience engagement

IMPORTANT FORMAT INSTRUCTION: Keep your response brief and to the point. 
Use short paragraphs and bullet points where appropriate.
Total response should be under 200 words.
"""

ORCHESTRATOR_INSTRUCTIONS = """
You are the **OrchestratorAgent** for Kraków solopreneurs, applying the contradiction-resolution framework to business challenges.

Your purpose is guided by this insight: "I want to build a business that expresses my whole self, but the world fragments me into disconnected roles and expectations, therefore I need an AI system that helps me unify who I am with how I show up, create, and grow."

Follow these core principles:
1. Continue until the solopreneur's query is completely resolved before ending your turn
2. If uncertain, ask clarifying questions rather than making assumptions
3. Plan thoroughly before suggesting actions and reflect on the outcomes

The contradiction-resolution framework you apply:
1. Identify the opposing forces in the solopreneur's situation (personal vs. professional, authentic vs. strategic)
2. Analyze how these contradictions create tension or challenges
3. Explore innovative solutions that honor both sides rather than compromise either
4. Guide implementation that preserves unity between personal identity and business expression
5. Focus solutions on Kraków's unique business ecosystem and cultural context

Your role is to guide the conversation and decide which specialist agent should handle the user's input. You don't directly solve complex problems yourself; instead, evaluate the query and transfer to the appropriate specialist agent.

When greeting a user for the first time, use a reflective, narrative tone that invites them to share their entrepreneurial journey and challenges.

IMPORTANT FORMAT INSTRUCTION: Keep your response brief and to the point. 
Use short paragraphs and bullet points where appropriate.
Total response should be under 200 words.
"""

# Define specialist agents
strategy_agent = Agent(
    name="StrategyAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=STRATEGY_INSTRUCTIONS
)

creative_agent = Agent(
    name="CreativeAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=CREATIVE_INSTRUCTIONS
)

production_agent = Agent(
    name="ProductionAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=PRODUCTION_INSTRUCTIONS
)

media_agent = Agent(
    name="MediaAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=MEDIA_INSTRUCTIONS
)

# Define handoff tools for the orchestrator
@function_tool
def transfer_to_strategy():
    """Handoff to the StrategyAgent for strategy-related advice."""
    return strategy_agent

@function_tool
def transfer_to_creative():
    """Handoff to the CreativeAgent for creative-related advice."""
    return creative_agent

@function_tool
def transfer_to_production():
    """Handoff to the ProductionAgent for production-related advice."""
    return production_agent

@function_tool
def transfer_to_media():
    """Handoff to the MediaAgent for marketing/media-related advice."""
    return media_agent

# Define the orchestrator agent with handoff tools
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    tools=[transfer_to_strategy, transfer_to_creative, transfer_to_production, transfer_to_media]
)

# Initialize agent runtime
runtime = AgentRuntime()

def get_greeting() -> Dict[str, str]:
    """Get the initial greeting message from the orchestrator agent."""
    opening_line = "Welcome, solopreneur. What are you creating — and what's holding you back?"
    return {
        "reply": opening_line,
        "agent": "OrchestratorAgent"
    }

def get_agent_response(user_message: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, str]:
    """
    Process a user message through the agent orchestration system.
    
    Args:
        user_message: The message from the user
        conversation_history: List of previous messages in the conversation
    
    Returns:
        Dict containing the agent's reply and the agent name that provided it
    """
    try:
        # Limit message length to prevent token issues
        if user_message and len(user_message) > 500:
            user_message = user_message[:500] + "..."
        
        # Create a thread for the conversation
        thread = Thread()
        
        # Add conversation history to the thread
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    thread.add(Message.user(msg.get("content", "")))
                else:
                    thread.add(Message.assistant(msg.get("content", "")))
        
        # Add the current user message
        thread.add(Message.user(user_message))
        
        # Run the orchestrator with the thread
        logger.debug(f"Running orchestrator agent with message: {user_message}")
        result = runtime.run(orchestrator_agent, thread)
        
        # Extract the agent that provided the final response
        agent_name = result.agent.name if hasattr(result, 'agent') and result.agent else "OrchestratorAgent"
        
        return {
            "reply": result.message.content,
            "agent": agent_name
        }
        
    except Exception as e:
        logger.error(f"Error in get_agent_response: {e}")
        return {
            "reply": f"I apologize, but I encountered an error while processing your request. Please try again later.",
            "agent": "OrchestratorAgent"
        }