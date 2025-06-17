"""Roadmap generation tests"""

from layer1_use_cases.roadmap_generator import RoadmapGenerator
from layer0_entities.mission import Mission

def test_roadmap_generator_creates_milestones():
    """Test that roadmap generator creates proper milestones"""
    generator = RoadmapGenerator()
    
    mission = Mission(
        statement="Build an AI-powered coaching platform for entrepreneurs",
        vision="Democratize access to business mentorship",
        values=["Innovation", "Accessibility", "Growth"]
    )
    
    roadmap = generator.generate_roadmap(mission)
    
    # Should generate 5 milestones as per requirements
    assert len(roadmap.milestones) == 5
    
    # Each milestone should have required properties
    for milestone in roadmap.milestones:
        assert hasattr(milestone, 'title')
        assert hasattr(milestone, 'description')
        assert milestone.title is not None
        assert len(milestone.title) > 0

def test_roadmap_deterministic():
    """Test that roadmap generation is deterministic for same input"""
    generator = RoadmapGenerator()
    
    mission = Mission(
        statement="Launch a sustainable fashion brand",
        vision="Transform the fashion industry",
        values=["Sustainability", "Quality", "Ethics"]
    )
    
    roadmap1 = generator.generate_roadmap(mission)
    roadmap2 = generator.generate_roadmap(mission)
    
    # Should generate same number of milestones
    assert len(roadmap1.milestones) == len(roadmap2.milestones)
    
    # Milestone structure should be consistent
    for i, (m1, m2) in enumerate(zip(roadmap1.milestones, roadmap2.milestones)):
        assert type(m1.title) == type(m2.title)
        assert type(m1.description) == type(m2.description)