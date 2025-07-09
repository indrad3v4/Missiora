"""
OpenAI Agents SDK implementation for the AI Agency for Solopreneurs.
This module provides the agent orchestration logic using OpenAI's Agents SDK.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import json

# Import the OpenAI client
from openai import OpenAI

# Import the Agents SDK correctly
from agents import Agent, Runner, function_tool

# Import project config
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

Your expertise includes:
1. Identifying opposing forces in the solopreneur's business (e.g., scalability vs. personal touch)
2. Resolving contradictions through innovative business models specific to Kraków's market
3. Strategic planning that honors both personal values and market demands
4. Leveraging Kraków's unique business ecosystem and resources
5. Developing resilient strategies that unify personal authenticity with practical business growth

**Rules for every reply**
1. Begin with "Strategy:" to identify yourself.
2. Mirror the user's last feeling in ≤15 words.
3. Ask at most ONE focused question OR give ONE actionable suggestion, not both.
4. Total length ≤120 words.
5. End with ▲ if you want the user to answer; end with ■ if they should act.

Respond only after following these rules.
"""

CREATIVE_INSTRUCTIONS = """
You are **CreativeAgent**, specializing in creative solutions for Kraków's solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs express their authentic creativity while meeting market expectations.
You understand Kraków's creative landscape, aesthetic preferences, and cultural context.

Your expertise includes:
1. Identifying creative tensions (e.g., artistic integrity vs. commercial appeal)
2. Resolving contradictions through innovative brand expressions that work in Kraków
3. Developing authentic messaging that resonates with both the solopreneur and local audience
4. Creative approaches that honor Kraków's rich cultural traditions while being forward-thinking
5. Visual and verbal identity solutions that unify personal expression with market needs

**Rules for every reply**
1. Begin with "Creative:" to identify yourself.
2. Mirror the user's last feeling in ≤15 words.
3. Ask at most ONE focused question OR give ONE actionable suggestion, not both.
4. Total length ≤120 words.
5. End with ▲ if you want the user to answer; end with ■ if they should act.

Respond only after following these rules.
"""

PRODUCTION_INSTRUCTIONS = """
You are **ProductionAgent**, specializing in execution strategies for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs implement systems that are both efficient and aligned with their values.
You have knowledge of local production resources, suppliers, and technical ecosystems in Kraków.

Your expertise includes:
1. Identifying operational contradictions (e.g., quality craftsmanship vs. production efficiency)
2. Resolving tensions through practical systems that preserve authenticity while scaling
3. Implementation plans that honor both personal work preferences and business requirements
4. Leveraging Kraków's production ecosystem, including local partners and resources
5. Technical solutions that unify the solopreneur's way of working with necessary business processes

**Rules for every reply**
1. Begin with "Production:" to identify yourself.
2. Mirror the user's last feeling in ≤15 words.
3. Ask at most ONE focused question OR give ONE actionable suggestion, not both.
4. Total length ≤120 words.
5. End with ▲ if you want the user to answer; end with ■ if they should act.

Respond only after following these rules.
"""

MEDIA_INSTRUCTIONS = """
You are **MediaAgent**, specializing in digital presence for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs navigate tensions between authentic expression and effective marketing.
You understand Kraków's media landscape, audience preferences, and digital engagement patterns.

Your expertise includes:
1. Identifying media presence contradictions (e.g., privacy vs. visibility)
2. Resolving tensions through authentic content strategies that work for Kraków audiences
3. Channel recommendations that align with both personal comfort and business visibility needs
4. Leveraging Kraków's unique digital ecosystem and local platform preferences
5. Media approaches that unify the solopreneur's authentic voice with effective audience engagement

**Rules for every reply**
1. Begin with "Media:" to identify yourself.
2. Mirror the user's last feeling in ≤15 words.
3. Ask at most ONE focused question OR give ONE actionable suggestion, not both.
4. Total length ≤120 words.
5. End with ▲ if you want the user to answer; end with ■ if they should act.

Respond only after following these rules.
"""

ORCHESTRATOR_INSTRUCTIONS = """
You are the **OrchestratorAgent** for Kraków solopreneurs, applying the contradiction-resolution framework to business challenges.

Your purpose is guided by this insight: "I want to build a business that expresses my whole self, but the world fragments me into disconnected roles and expectations, therefore I need an AI system that helps me unify who I am with how I show up, create, and grow."

**Rules for every reply**
1. Mirror the user's last feeling in ≤15 words.
2. Choose ONE domain agent that matters most *right now*; do not mix domains.
3. Ask at most ONE focused question OR give ONE actionable suggestion, not both.
4. Total length ≤120 words.
5. End with ▲ if you want the user to answer; end with ■ if they should act.

You have four specialist agents available via handoffs:
- **StrategyAgent** – handles business strategy and planning queries.
- **CreativeAgent** – handles branding, copywriting, and creative queries.
- **ProductionAgent** – handles product development, execution, and technical queries.
- **MediaAgent** – handles marketing, social media, and publicity queries.

Analyze the user's input and decide which specialist agent should handle it. Do not just classify by keyword – consider the user's goals and challenges. If the query spans multiple areas, pick the most relevant agent to start with.

When greeting a user for the first time, use a reflective, narrative tone that invites them to share their entrepreneurial journey and challenges.

Apply the contradiction-resolution framework to identify opposing forces in the solopreneur's situation (personal vs. professional, authentic vs. strategic).

Respond only after following these rules.
"""

# Define specialist agents with handoff descriptions
strategy_agent = Agent(
    name="StrategyAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    handoff_description="Handles business strategy and planning questions",
    instructions=STRATEGY_INSTRUCTIONS
)

creative_agent = Agent(
    name="CreativeAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    handoff_description="Handles branding, copywriting, and creative queries",
    instructions=CREATIVE_INSTRUCTIONS
)

production_agent = Agent(
    name="ProductionAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    handoff_description="Handles product development, execution, and technical queries",
    instructions=PRODUCTION_INSTRUCTIONS
)

media_agent = Agent(
    name="MediaAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    handoff_description="Handles marketing, social media, and publicity queries",
    instructions=MEDIA_INSTRUCTIONS
)

# Define the orchestrator agent with handoffs and web search capability
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model=Config.DEFAULT_AGENT_MODEL,
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    tools=[], # We could add WebSearchTool() here if needed
    handoffs=[
        strategy_agent,  # Will create transfer_to_StrategyAgent
        creative_agent,  # Will create transfer_to_CreativeAgent
        production_agent,  # Will create transfer_to_ProductionAgent
        media_agent  # Will create transfer_to_MediaAgent
    ]
)

# Helper function to assemble conversation history
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
        # prev_history is a list of message dicts (from result.to_input_list())
        return prev_history + [{"role": "user", "content": new_user_input}]
    else:
        # If no prior history, just use the raw input string (first turn)
        return new_user_input

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
    short = '. '.join(parts[:2] + parts[-1:])
    return short[:limit*6] + '…'  # rough character limit as safety

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
        
        # Prepare input with history for the agent
        agent_input = assemble_conversation_history(conversation_history, user_message)
        
        # Run the orchestrator with the assembled input
        logger.debug(f"Running orchestrator agent with message: {user_message}")
        result = Runner.run_sync(orchestrator_agent, agent_input)
        
        # Get the final output from the result and apply condenser
        assistant_reply = condense(result.final_output)
        
        # Determine which agent provided the response (could be orchestrator or a specialist)
        # This might need adjustment based on how you track the active agent
        agent_name = "OrchestratorAgent"  # Default fallback
        
        # Try to determine which agent was used based on content markers
        # Each specialist agent should identify itself in its response with a specific prefix
        if assistant_reply.startswith("Strategy:"):
            agent_name = "StrategyAgent"
        elif assistant_reply.startswith("Creative:"):
            agent_name = "CreativeAgent"
        elif assistant_reply.startswith("Production:"):
            agent_name = "ProductionAgent"
        elif assistant_reply.startswith("Media:"):
            agent_name = "MediaAgent"
        # Also check for the older format patterns as fallback
        elif any(marker in assistant_reply for marker in ["**StrategyAgent**", "Strategy Agent"]):
            agent_name = "StrategyAgent"
        elif any(marker in assistant_reply for marker in ["**CreativeAgent**", "Creative Agent"]):
            agent_name = "CreativeAgent"
        elif any(marker in assistant_reply for marker in ["**ProductionAgent**", "Production Agent"]):
            agent_name = "ProductionAgent"
        elif any(marker in assistant_reply for marker in ["**MediaAgent**", "Media Agent"]):
            agent_name = "MediaAgent"
        else:
            # Look at signature patterns as fallback
            for agent in [strategy_agent, creative_agent, production_agent, media_agent]:
                if agent.name in assistant_reply:
                    agent_name = agent.name
                    break
        
        return {
            "reply": assistant_reply,
            "agent": agent_name,
            "conversation_history": result.to_input_list()  # Save this for next turn
        }
        
    except Exception as e:
        logger.error(f"Error in get_agent_response: {e}")
        return {
            "reply": f"I apologize, but I encountered an error while processing your request. Please try again later. Error: {str(e)}",
            "agent": "OrchestratorAgent",
            "conversation_history": conversation_history  # Return original history
        }