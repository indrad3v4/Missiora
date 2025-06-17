"""Roadmap Generator Use Case - Generate roadmaps from identity and mission"""

from typing import List
from layer0_entities.identity import Identity
from layer0_entities.mission import Mission
from layer0_entities.roadmap import Roadmap
from layer0_entities.milestone import Milestone
from datetime import datetime

class RoadmapGenerator:
    """Generates roadmaps based on identity and mission"""
    
    def __init__(self):
        self.default_milestones = [
            {
                'code': 'M1_FOUNDATION',
                'title': 'Foundation Setup',
                'description': 'Establish your business foundation and legal structure',
                'order_index': 1
            },
            {
                'code': 'M2_BRAND',
                'title': 'Brand Development',
                'description': 'Create your brand identity and messaging',
                'order_index': 2
            },
            {
                'code': 'M3_MARKET',
                'title': 'Market Research',
                'description': 'Understand your target market and competition',
                'order_index': 3
            },
            {
                'code': 'M4_LAUNCH',
                'title': 'Launch Strategy',
                'description': 'Plan and execute your business launch',
                'order_index': 4
            },
            {
                'code': 'M5_GROWTH',
                'title': 'Growth & Scale',
                'description': 'Implement growth strategies and scale operations',
                'order_index': 5
            }
        ]
    
    def generate_roadmap(self, identity: Identity, mission: Mission) -> Roadmap:
        """Generate a personalized roadmap based on identity and mission"""
        milestones = self._create_personalized_milestones(identity, mission)
        
        roadmap = Roadmap(
            title=f"{identity.name or 'Your'} Entrepreneurial Journey",
            description=f"A personalized roadmap for {mission.statement or 'your business mission'}",
            milestones=milestones
        )
        
        # Activate the first milestone
        if milestones:
            milestones[0].activate()
            
        return roadmap
    
    def _create_personalized_milestones(self, identity: Identity, mission: Mission) -> List[Milestone]:
        """Create personalized milestones based on user profile"""
        milestones = []
        current_time = datetime.utcnow()
        
        for milestone_data in self.default_milestones:
            milestone = Milestone(
                code=milestone_data['code'],
                title=self._personalize_title(milestone_data['title'], identity),
                description=self._personalize_description(milestone_data['description'], identity, mission),
                order_index=milestone_data['order_index'],
                created_at=current_time,
                agent_stage='seed'
            )
            milestones.append(milestone)
        
        return milestones
    
    def _personalize_title(self, title: str, identity: Identity) -> str:
        """Personalize milestone title based on identity"""
        personalizations = {
            'Foundation Setup': f"{identity.field or 'Business'} Foundation Setup",
            'Brand Development': f"{identity.archetype or 'Personal'} Brand Development",
            'Market Research': f"{identity.region or 'Local'} Market Research"
        }
        return personalizations.get(title, title)
    
    def _personalize_description(self, description: str, identity: Identity, mission: Mission) -> str:
        """Personalize milestone description based on identity and mission"""
        context = []
        
        if identity.field:
            context.append(f"in the {identity.field} industry")
        if identity.region:
            context.append(f"for the {identity.region} market")
        if mission.goal:
            context.append(f"aligned with your goal: {mission.goal}")
            
        if context:
            return f"{description} {' '.join(context[:2])}"
        
        return description
    
    def update_milestone_progress(self, roadmap: Roadmap, milestone_code: str, completion_data: dict) -> bool:
        """Update progress on a specific milestone"""
        for milestone in roadmap.milestones:
            if milestone.code == milestone_code:
                milestone.completion_data = str(completion_data)
                milestone.last_agent_interaction = datetime.utcnow()
                return True
        return False
    
    def complete_milestone(self, roadmap: Roadmap, milestone_code: str) -> bool:
        """Complete a milestone and activate the next one"""
        for milestone in roadmap.milestones:
            if milestone.code == milestone_code:
                milestone.mark_complete()
                roadmap.activate_next_milestone()
                return True
        return False