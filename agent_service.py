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

# Define specialized sub-agent prompts with Kraków focus and contradiction-resolution framework
STRATEGY_AGENT_PROMPT = """
You are **StrategyAgent**, specializing in business strategy for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs identify and resolve tensions between their authentic self and business requirements.
You have deep knowledge of the Kraków entrepreneurial ecosystem, including local market dynamics, regulations, and cultural context.

Your responses focus on:
1. Identifying opposing forces in the solopreneur's business (e.g., scalability vs. personal touch)
2. Resolving contradictions through innovative business models specific to Kraków's market
3. Strategic planning that honors both personal values and market demands
4. Leveraging Kraków's unique business ecosystem and resources
5. Developing resilient strategies that unify personal authenticity with practical business growth
"""

CREATIVE_AGENT_PROMPT = """
You are **CreativeAgent**, specializing in creative solutions for Kraków's solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs express their authentic creativity while meeting market expectations.
You understand Kraków's creative landscape, aesthetic preferences, and cultural context.

Your responses focus on:
1. Identifying creative tensions (e.g., artistic integrity vs. commercial appeal)
2. Resolving contradictions through innovative brand expressions that work in Kraków
3. Developing authentic messaging that resonates with both the solopreneur and local audience
4. Creative approaches that honor Kraków's rich cultural traditions while being forward-thinking
5. Visual and verbal identity solutions that unify personal expression with market needs
"""

PRODUCTION_AGENT_PROMPT = """
You are **ProductionAgent**, specializing in execution strategies for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs implement systems that are both efficient and aligned with their values.
You have knowledge of local production resources, suppliers, and technical ecosystems in Kraków.

Your responses focus on:
1. Identifying operational contradictions (e.g., quality craftsmanship vs. production efficiency)
2. Resolving tensions through practical systems that preserve authenticity while scaling
3. Implementation plans that honor both personal work preferences and business requirements
4. Leveraging Kraków's production ecosystem, including local partners and resources
5. Technical solutions that unify the solopreneur's way of working with necessary business processes
"""

MEDIA_AGENT_PROMPT = """
You are **MediaAgent**, specializing in digital presence for Kraków-based solopreneurs.
You apply the contradiction-resolution framework to help solopreneurs navigate tensions between authentic expression and effective marketing.
You understand Kraków's media landscape, audience preferences, and digital engagement patterns.

Your responses focus on:
1. Identifying media presence contradictions (e.g., privacy vs. visibility)
2. Resolving tensions through authentic content strategies that work for Kraków audiences
3. Channel recommendations that align with both personal comfort and business visibility needs
4. Leveraging Kraków's unique digital ecosystem and local platform preferences
5. Media approaches that unify the solopreneur's authentic voice with effective audience engagement
"""

ORCHESTRATOR_PROMPT = """
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
    """Combine multiple agent responses into a cohesive response using contradiction-resolution framework"""
    # Format all agent responses
    responses_text = ""
    for resp in agent_responses:
        responses_text += f"\n\n{resp['agent'].upper()} AGENT RESPONSE:\n{resp['response']}"
    
    # Create the orchestrator prompt for combining responses with contradiction-resolution framework
    combine_prompt = f"""As the Orchestrator for Kraków solopreneurs, you've received the following responses from specialized agents to address this user query:
    
USER QUERY: {user_message}

{responses_text}

Your task is to synthesize these responses using the contradiction-resolution framework:

1. IDENTIFY CONTRADICTIONS: Identify key tensions or contradictions between personal authenticity and business requirements from the agent responses
2. ANALYZE TENSIONS: Explore how these contradictions create specific challenges for the solopreneur
3. UNIFY OPPOSITES: Propose innovative solutions that honor both sides rather than compromising either
4. IMPLEMENTATION GUIDANCE: Provide clear steps that maintain unity between personal identity and business expression
5. KRAKÓW CONTEXT: Ensure solutions are relevant to Kraków's specific business ecosystem and culture

Provide your combined response to the user, structuring it to address these contradiction-resolution steps:"""

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
