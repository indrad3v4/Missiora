"""CV Controller - REST API for computer vision analysis"""

import base64
import asyncio
from flask import Blueprint, jsonify, request
from ...layer2_interfaces.gateways.cv_gateway import cv_gateway

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/api/cv/analyse', methods=['POST'])
def analyse_image():
    """Analyse uploaded image for caption and object detection"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400
        
        # Decode base64 image
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            
        except Exception as decode_error:
            return jsonify({"error": f"Failed to decode image: {str(decode_error)}"}), 400
        
        # Run CV analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Get both caption and object detection
            caption_result = loop.run_until_complete(cv_gateway.caption_image(image_bytes))
            detection_result = loop.run_until_complete(cv_gateway.detect_objects(image_bytes))
            
            return jsonify({
                "caption": caption_result.get('caption', 'Unable to generate caption'),
                "objects": detection_result.get('objects', []),
                "confidence": caption_result.get('confidence', 0.5),
                "model_used": {
                    "caption": caption_result.get('model', 'unknown'),
                    "detection": detection_result.get('model', 'unknown')
                }
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({
            "error": f"CV analysis failed: {str(e)}",
            "caption": "Unable to process image",
            "objects": []
        }), 500

@cv_bp.route('/api/cv/status', methods=['GET'])
def cv_status():
    """Get CV service status"""
    return jsonify({
        "status": "online",
        "models_available": {
            "caption": cv_gateway.captioner is not None,
            "detection": cv_gateway.object_detector is not None
        },
        "mock_mode": getattr(cv_gateway, '_use_mock', True)
    })