"""
TRIZ-Fixed Vision Routes - Solves OpenAI Rate Limiting Contradiction
Replaces analyze_vision with free alternatives
"""

from flask import jsonify, request
import time

def setup_vision_routes(app):
    """Setup the fixed vision routes"""
    
    @app.route('/api/vision/analyze', methods=['POST'])
    def analyze_vision_fixed():
        """Free Vision analysis - TRIZ solution for rate limiting"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Import our free vision engine
            from vision_engine import vision_engine
            
            # Get image data and timestamp
            image_data = data.get('image', '')
            timestamp = data.get('timestamp', int(time.time() * 1000))
            
            # Use free vision analysis (no OpenAI dependency)
            analysis_result = vision_engine.analyze_image(image_data, timestamp)
            
            # Emit token tracking event for the token tracker
            if analysis_result['status'] == 'success':
                print(f"✓ Vision analysis: {analysis_result['token_cost']} tokens deducted")
                
                # Add AR-specific metadata for better user experience
                analysis_result['ar_ready'] = True
                analysis_result['overlay_instructions'] = "Point camera at business objects for smart insights"
                
                # Add suggested actions for detected objects
                if analysis_result['objects']:
                    for obj in analysis_result['objects']:
                        obj['suggested_actions'] = vision_engine.get_suggested_actions(obj['label'])
            
            return jsonify(analysis_result)
            
        except Exception as e:
            print(f"Vision analysis error: {e}")
            return jsonify({
                'error': 'Vision analysis failed',
                'objects': [],
                'scene_description': 'Analysis unavailable',
                'status': 'error',
                'ar_ready': False
            }), 500
    
    return app