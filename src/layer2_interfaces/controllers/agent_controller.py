"""Agent Controller - REST API for AI agent interactions"""

from flask import Blueprint, jsonify, request
from ...layer2_interfaces.gateways.cv_gateway import cv_gateway
from ...layer1_use_cases.agent_service import get_agent_response

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/api/agent/interact', methods=['POST'])
def interact_with_agent():
    """Handle agent interactions with optional CV processing"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        image_data = data.get('image')  # Base64 encoded image if present
        
        # If image is present, use CV gateway for analysis
        if image_data:
            import asyncio
            import base64
            from io import BytesIO
            
            # Decode base64 image
            try:
                # Remove data URL prefix if present
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                
                image_bytes = base64.b64decode(image_data)
                
                # Run CV analysis
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    cv_result = loop.run_until_complete(cv_gateway.caption_image(image_bytes))
                    caption = cv_result.get('caption', 'Unable to analyze image')
                    
                    # Enhance message with CV analysis
                    enhanced_message = f"{message}\n\nImage analysis: {caption}"
                    
                finally:
                    loop.close()
                    
            except Exception as cv_error:
                enhanced_message = f"{message}\n\nNote: Unable to process image - {str(cv_error)}"
        else:
            enhanced_message = message
        
        # Get agent response
        response = get_agent_response(
            user_message=enhanced_message,
            message_history=data.get('history', [])
        )
        
        return jsonify({
            "response": response,
            "timestamp": "2025-06-19T11:45:00Z",
            "agent": "missiora_ai"
        })
        
    except Exception as e:
        return jsonify({
            "response": f"I'm having trouble processing that request. Could you try again? (Error: {str(e)})",
            "timestamp": "2025-06-19T11:45:00Z",
            "agent": "missiora_ai",
            "error": True
        }), 500