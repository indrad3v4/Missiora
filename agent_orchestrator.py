"""
Agent Orchestration System - Implements the three core components:
1. Model: GPT-4o for complex reasoning, smaller models for classification
2. Tools: Data retrieval, Action execution, Agent orchestration
3. Instructions: Clear guidelines with edge case handling
"""

import os
from openai import OpenAI
from datetime import datetime
import json

class AgentOrchestrator:
    """Main agent orchestrator following the practical guide design patterns"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.tools = self._initialize_tools()
        self.activation_metrics = ActivationMetrics()
        
    def _initialize_tools(self):
        """Initialize the three types of tools: Data, Action, Orchestration"""
        return {
            # Data Tools - retrieve context and information
            'data': {
                'query_user_profile': self._query_user_profile,
                'get_milestone_progress': self._get_milestone_progress,
                'search_knowledge_base': self._search_knowledge_base
            },
            # Action Tools - interact with systems to take actions
            'action': {
                'update_milestone': self._update_milestone,
                'send_notification': self._send_notification,
                'create_roadmap': self._create_roadmap
            },
            # Orchestration Tools - other agents as tools
            'orchestration': {
                'roadmap_agent': RoadmapAgent(),
                'mission_agent': MissionAgent(),
                'identity_agent': IdentityAgent()
            }
        }
    
    def process_user_request(self, user_message, user_context=None):
        """Process user request with proper tool selection and execution"""
        
        # Use gpt-4o for complex decision-making
        response = self.client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            messages=[
                {
                    "role": "system",
                    "content": self._get_agent_instructions()
                },
                {
                    "role": "user", 
                    "content": f"Context: {user_context}\n\nRequest: {user_message}"
                }
            ],
            tools=self._get_tool_definitions(),
            tool_choice="auto"
        )
        
        return self._execute_tool_calls(response)
    
    def _get_agent_instructions(self):
        """Clear instructions with edge case handling as per the guide"""
        return """You are MISSIORA, an AI agent for solopreneurs in Kraków.

Core Workflow:
1. Listen to understand both personal values and professional goals
2. Identify authentic strengths for business expression
3. Provide specific, actionable strategies aligning identity with growth
4. Bridge disconnection between personal and professional self
5. Ensure business decisions reflect personal values

Tools Available:
- Data tools: Query profiles, get progress, search knowledge
- Action tools: Update milestones, send notifications, create roadmaps  
- Orchestration tools: Specialized agents for roadmap, mission, identity

Edge Cases:
- If user provides incomplete information: Ask specific clarifying questions
- If user seems disconnected: Focus on identity-business alignment
- If technical issues occur: Gracefully fallback and explain limitations
- If milestone completion stalls: Suggest breaking into smaller steps

Always complete the full workflow before ending your turn."""

    def _execute_tool_calls(self, response):
        """Execute tool calls and track activation metrics"""
        if hasattr(response.choices[0].message, 'tool_calls'):
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                # Track activation metrics
                self.activation_metrics.track_tool_usage(tool_name)
                
                # Execute appropriate tool
                if tool_name in self.tools['data']:
                    return self.tools['data'][tool_name](**args)
                elif tool_name in self.tools['action']:
                    return self.tools['action'][tool_name](**args)
                elif tool_name in self.tools['orchestration']:
                    return self.tools['orchestration'][tool_name].process(**args)
        
        return response.choices[0].message.content

class ActivationMetrics:
    """Track activation rate: users who reach Milestone 1 / total sign-ups"""
    
    def __init__(self):
        self.metrics = {
            'total_signups': 0,
            'milestone_1_completions': 0,
            'tool_usage': {},
            'session_starts': 0,
            'instant_wins': 0  # <5 min wins for 25% higher activation
        }
    
    def track_signup(self):
        """Track new user signup"""
        self.metrics['total_signups'] += 1
    
    def track_milestone_completion(self, milestone_id):
        """Track milestone completion for activation rate"""
        if milestone_id == 1:
            self.metrics['milestone_1_completions'] += 1
    
    def track_tool_usage(self, tool_name):
        """Track which tools are being used"""
        if tool_name not in self.metrics['tool_usage']:
            self.metrics['tool_usage'][tool_name] = 0
        self.metrics['tool_usage'][tool_name] += 1
    
    def track_instant_win(self):
        """Track instant wins (<5 min tasks)"""
        self.metrics['instant_wins'] += 1
    
    def get_activation_rate(self):
        """Calculate activation rate as per industry standards"""
        if self.metrics['total_signups'] == 0:
            return 0
        return (self.metrics['milestone_1_completions'] / self.metrics['total_signups']) * 100

class RoadmapAgent:
    """Specialized agent for roadmap generation - always returns 5 milestones"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def generate_roadmap(self, mission_text):
        """Generate deterministic 5-step roadmap from mission"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a roadmap generation specialist. Create exactly 5 milestones that:
                    1. Build progressively toward the mission goal
                    2. Include specific ROI expectations
                    3. Have clear completion criteria
                    4. Take 1-4 weeks each to complete
                    5. Connect personal identity with business growth
                    
                    Return JSON format:
                    {
                        "milestones": [
                            {
                                "id": 1,
                                "title": "Milestone Title",
                                "description": "Clear description",
                                "expected_roi": "Specific ROI hint",
                                "cost_hint": "Resource requirements",
                                "duration_weeks": 2
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Mission: {mission_text}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def process(self, **kwargs):
        """Process roadmap requests"""
        if 'mission' in kwargs:
            return self.generate_roadmap(kwargs['mission'])
        return {"error": "No mission provided"}

class MissionAgent:
    """Specialized agent for mission statement creation and refinement"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def process(self, **kwargs):
        """Process mission-related requests"""
        if 'identity_data' in kwargs:
            return self._create_mission_from_identity(kwargs['identity_data'])
        elif 'refine_mission' in kwargs:
            return self._refine_mission(kwargs['current_mission'], kwargs.get('feedback', ''))
        return {"error": "Invalid mission request"}
    
    def _create_mission_from_identity(self, identity_data):
        """Create mission statement from identity data"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "Create a compelling mission statement that unifies personal identity with business goals. Focus on authentic self-expression through entrepreneurship."
                },
                {
                    "role": "user",
                    "content": f"Identity: {json.dumps(identity_data)}"
                }
            ]
        )
        return {"mission": response.choices[0].message.content}

class IdentityAgent:
    """Specialized agent for identity exploration and business alignment"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def process(self, **kwargs):
        """Process identity-related requests"""
        if 'analyze_alignment' in kwargs:
            return self._analyze_identity_business_alignment(
                kwargs['identity_data'], 
                kwargs['business_data']
            )
        return {"error": "Invalid identity request"}
    
    def _analyze_identity_business_alignment(self, identity_data, business_data):
        """Analyze how well identity aligns with business direction"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze identity-business alignment. Identify gaps, strengths, and specific recommendations for unified growth."
                },
                {
                    "role": "user", 
                    "content": f"Identity: {json.dumps(identity_data)}\nBusiness: {json.dumps(business_data)}"
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)