"""Computer Vision Gateway - Lightweight CV operations using tiny models"""

import asyncio
from typing import Dict, Any, Optional
from io import BytesIO
import base64

class CVGateway:
    """Lightweight computer vision gateway using tiny HuggingFace models"""
    
    def __init__(self):
        self.object_detector = None
        self.captioner = None
        self._setup_models()
    
    def _setup_models(self):
        """Initialize tiny models for minimal disk usage"""
        try:
            from transformers import pipeline
            
            # Use tiny testing models to minimize disk usage
            self.object_detector = pipeline(
                "object-detection",
                model="hf-internal-testing/tiny-random-detr",
                device=-1  # CPU only
            )
            
            self.captioner = pipeline(
                "image-to-text", 
                model="hf-internal-testing/tiny-random-BlipForConditionalGeneration",
                device=-1
            )
            
        except ImportError:
            # Graceful fallback if transformers not available
            pass
        except Exception as e:
            print(f"CV models setup warning: {e}")
    
    async def detect_objects(self, image_data: bytes) -> Dict[str, Any]:
        """Detect objects in image using lightweight model"""
        if self.object_detector is None:
            return {
                "error": "Object detection not available",
                "objects": [],
                "model": "fallback"
            }
        
        try:
            from PIL import Image
            
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Run detection
            results = self.object_detector(image)
            
            return {
                "objects": [
                    {
                        "label": obj.get("label", "unknown"),
                        "score": float(obj.get("score", 0.0)),
                        "box": obj.get("box", {})
                    }
                    for obj in results
                ],
                "model": "tiny-random-detr",
                "count": len(results)
            }
            
        except Exception as e:
            return {
                "error": f"Detection failed: {str(e)}",
                "objects": [],
                "model": "error"
            }
    
    async def caption_image(self, image_data: bytes) -> Dict[str, Any]:
        """Generate caption for image using lightweight model"""
        if self.captioner is None:
            return {
                "error": "Image captioning not available",
                "caption": "No caption model loaded",
                "model": "fallback"
            }
        
        try:
            from PIL import Image
            
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Generate caption
            result = self.captioner(image)
            
            caption = ""
            if result and len(result) > 0:
                caption = result[0].get("generated_text", "No caption generated")
            
            return {
                "caption": caption,
                "model": "tiny-random-BlipForConditionalGeneration",
                "confidence": 0.85  # Mock confidence for demo
            }
            
        except Exception as e:
            return {
                "error": f"Captioning failed: {str(e)}",
                "caption": "Error generating caption",
                "model": "error"
            }

# Global instance
cv_gateway = CVGateway()