#!/usr/bin/env python3
"""Bootstrap milestones for the UX migration"""

from app import app, db

def create_milestones():
    """Create initial milestone data"""
    # Import here to avoid circular imports
    from models import Milestone
    
    with app.app_context():
        # Clear existing milestones
        Milestone.query.delete()
        
        # Create starter milestones
        milestones = [
            Milestone(
                code='define_identity',
                title='Define Identity',
                description='Establish your archetype, mood, and professional identity',
                active=True,
                completed=False,
                order_index=1
            ),
            Milestone(
                code='build_mission',
                title='Build Mission',
                description='Create your mission statement and highest goal',
                active=False,
                completed=False,
                order_index=2
            ),
            Milestone(
                code='design_first_offer',
                title='Design First Offer',
                description='Create your first service or product offering',
                active=False,
                completed=False,
                order_index=3
            ),
            Milestone(
                code='secure_first_clients',
                title='Secure First Clients',
                description='Land your initial customers and validate your offer',
                active=False,
                completed=False,
                order_index=4
            ),
            Milestone(
                code='automate_system',
                title='Automate AI System',
                description='Build systems to scale your solopreneur business',
                active=False,
                completed=False,
                order_index=5
            )
        ]
        
        for milestone in milestones:
            db.session.add(milestone)
        
        db.session.commit()
        print(f"✓ Created {len(milestones)} milestones")

if __name__ == '__main__':
    create_milestones()
