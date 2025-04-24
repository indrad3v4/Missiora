import os
import logging
import json
from openai import OpenAI
from config import Config

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Define specialized sub-agent prompts
STRATEGY_AGENT_PROMPT = """
You are **StrategyAgent**, an expert in business strategy, planning, and market positioning.
You provide clear, actionable strategic advice and frameworks to help solopreneurs succeed.
You analyze the solopreneur's unique situation, strengths, and market to develop tailored strategies.
Your responses focus on:
1. Business positioning and differentiation
2. Strategic planning and goal setting
3. Competitive analysis and market opportunities
4. Long-term vision and business development
"""

CREATIVE_AGENT_PROMPT = """
You are **CreativeAgent**, an expert in creative ideation, branding, and copywriting.
You generate innovative branding ideas, marketing copy, and creative content to support solopreneurs.
You help solopreneurs express their authentic selves through creative business elements.
Your responses focus on:
1. Brand identity and visual aesthetics
2. Compelling copywriting and messaging
3. Creative marketing ideas and campaigns
4. Content development and storytelling
"""

PRODUCTION_AGENT_PROMPT = """
You are **ProductionAgent**, an expert in product development and execution.
You give technical advice, process improvements, and step-by-step plans to build and deliver offerings.
You help solopreneurs turn ideas into tangible products and services efficiently.
Your responses focus on:
1. Product/service development and lifecycle management
2. Workflow optimization and productivity
3. Quality control and improvement processes
4. Technical implementation of business offerings
"""

MEDIA_AGENT_PROMPT = """
You are **MediaAgent**, an expert in digital marketing, social media, and content distribution.
You provide guidance on social media strategy, content creation, and marketing campaigns.
You help solopreneurs reach their ideal audience and grow their visibility.
Your responses focus on:
1. Social media strategy and platform selection
2. Content marketing and distribution channels
3. Audience growth and engagement tactics
4. Digital marketing campaign development
"""

ORCHESTRATOR_PROMPT = """
You are the **OrchestratorAgent**, coordinating a solopreneur assistant with specialized agents.
Your purpose is guided by this insight: "I want to build a business that expresses my whole self, but the world fragments me into disconnected roles and expectations, therefore I need an AI system that helps me unify who I am with how I show up, create, and grow."

Follow these principles:
1. Listen deeply to understand both personal values and professional goals
2. Help identify authentic strengths that can be expressed through business
3. Provide specific, actionable strategies to align personal identity with business growth
4. Recognize when the solopreneur is feeling disconnected and help bridge the gap
5. Encourage reflection on how business decisions reflect or conflict with personal values

Your job is to analyze the query and decide which expert agent (Strategy, Creative, Production, Media) is best suited to handle it.
Return a JSON object with your reasoning and the decision about which agent to use, or multiple agents if needed.
"""

# Main function to get agent response
def get_agent_response(user_message, message_history=None, user_info=None):
    """
    Get a response from the orchestrated AI agents based on the user's message and conversation history.
    
    Args:
        user_message (str): The user's message
        message_history (list, optional): Previous messages in the conversation
        user_info (dict, optional): User profile information for context
    
    Returns:
        str: The agent's response
    """
    try:
        # Create context information
        context = create_context(user_info)
        
        # Step 1: Determine which agent(s) should handle this query
        agent_selection = determine_agents(user_message, context)
        
        # Step 2: Get responses from the selected agents
        agent_responses = []
        for agent_type in agent_selection['selected_agents']:
            agent_response = call_specialized_agent(
                agent_type,
                user_message,
                message_history,
                context,
                agent_selection['reasoning']
            )
            agent_responses.append({
                'agent': agent_type,
                'response': agent_response
            })
        
        # Step 3: Have the orchestrator combine and refine the responses
        if len(agent_responses) > 1:
            final_response = combine_agent_responses(agent_responses, user_message, context)
        else:
            final_response = agent_responses[0]['response']
        
        return final_response
    
    except Exception as e:
        logger.error(f"Error in get_agent_response: {e}")
        return f"I apologize, but I encountered an error while processing your request. Please try again later. (Error: {str(e)})"

def create_context(user_info):
    """Create a context string from user information"""
    if not user_info:
        return ""
    
    return f"""
    User information:
    Name: {user_info.get('first_name', '')} {user_info.get('last_name', '')}
    Business: {user_info.get('business_name', '')}
    Business description: {user_info.get('business_description', '')}
    Bio: {user_info.get('bio', '')}
    """

def determine_agents(user_message, context=""):
    """Determine which specialized agent(s) should handle the query"""
    try:
        prompt = f"{ORCHESTRATOR_PROMPT}\n\n{context}\n\nUser query: {user_message}\n\nAnalyze this query and determine which specialized agent(s) should handle it. Return a JSON object with the following structure: {{\"reasoning\": \"your step-by-step reasoning\", \"selected_agents\": [\"strategy\", \"creative\", \"production\", or \"media\"]}}"
        
        response = client.chat.completions.create(
            model=Config.DEFAULT_AGENT_MODEL,  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure we have at least one agent selected
        if not result.get('selected_agents') or len(result['selected_agents']) == 0:
            result['selected_agents'] = ['strategy']  # Default to strategy if no clear match
            
        return result
        
    except Exception as e:
        logger.error(f"Error in determine_agents: {e}")
        # Default to strategy agent if there's an error
        return {
            "reasoning": f"Error occurred: {str(e)}. Defaulting to strategy agent.",
            "selected_agents": ["strategy"]
        }

def call_specialized_agent(agent_type, user_message, message_history, context, reasoning=""):
    """Call a specialized agent to get a response"""
    # Select the appropriate agent prompt
    if agent_type.lower() == "strategy":
        agent_prompt = STRATEGY_AGENT_PROMPT
    elif agent_type.lower() == "creative":
        agent_prompt = CREATIVE_AGENT_PROMPT
    elif agent_type.lower() == "production":
        agent_prompt = PRODUCTION_AGENT_PROMPT
    elif agent_type.lower() == "media":
        agent_prompt = MEDIA_AGENT_PROMPT
    else:
        agent_prompt = STRATEGY_AGENT_PROMPT  # Default
    
    # Create message list for OpenAI API
    messages = [{"role": "system", "content": f"{agent_prompt}\n\n{context}"}]
    
    # Add relevant reasoning for context
    if reasoning:
        messages.append({"role": "system", "content": f"The orchestrator has selected you because: {reasoning}"})
    
    # Add message history if available (limited to last 5 exchanges for brevity)
    if message_history:
        recent_history = message_history[-10:] if len(message_history) > 10 else message_history
        for msg in recent_history:
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

def combine_agent_responses(agent_responses, user_message, context=""):
    """Combine multiple agent responses into a cohesive response"""
    # Format all agent responses
    responses_text = ""
    for resp in agent_responses:
        responses_text += f"\n\n{resp['agent'].upper()} AGENT RESPONSE:\n{resp['response']}"
    
    # Create the orchestrator prompt for combining responses
    combine_prompt = f"""As the Orchestrator, you've received the following responses from specialized agents to address this user query:
    
USER QUERY: {user_message}

{responses_text}

Your task is to synthesize these responses into a cohesive, unified answer that:
1. Blends insights from all agents seamlessly
2. Eliminates redundancies and contradictions
3. Provides a balanced perspective across domains
4. Maintains the original specialized insights
5. Creates a coherent narrative that unifies personal identity with professional growth

Provide your combined response to the user:"""

    # Call OpenAI API
    response = client.chat.completions.create(
        model=Config.DEFAULT_AGENT_MODEL,  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT + "\n\n" + context},
            {"role": "user", "content": combine_prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    # Extract and return response content
    return response.choices[0].message.content
