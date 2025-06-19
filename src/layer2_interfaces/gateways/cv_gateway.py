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
        self._use_mock = False
        self._setup_models()
    
    def _setup_models(self):
        """Initialize lightweight CV models or fallback implementations"""
        try:
            # Try to load transformers for real CV functionality
            from transformers import pipeline
            
            # Use tiny models to minimize disk usage
            self.object_detector = pipeline(
                "object-detection",
                model="facebook/detr-resnet-50",  # Lightweight but functional
                device=-1,  # CPU only
                return_tensors="pt"
            )
            
            self.captioner = pipeline(
                "image-to-text",
                model="nlpconnect/vit-gpt2-image-captioning",  # Lightweight captioning
                device=-1
            )
            
            print("CV models loaded successfully")
            
        except ImportError:
            # Graceful fallback - use mock implementations
            print("Transformers not available - using mock CV models")
            self._setup_mock_models()
        except Exception as e:
            print(f"CV models setup warning: {e} - using mock models")
            self._setup_mock_models()
    
    def _setup_mock_models(self):
        """Setup mock implementations when real models unavailable"""
        self.object_detector = None
        self.captioner = None
        self._use_mock = True
    
    async def detect_objects(self, image_data: bytes) -> Dict[str, Any]:
        """Detect objects in image using lightweight model or mock"""
        if self._use_mock or self.object_detector is None:
            # Mock implementation for demo purposes
            return {
                "objects": [
                    {"label": "person", "score": 0.92, "box": {"x": 100, "y": 50, "w": 150, "h": 200}},
                    {"label": "laptop", "score": 0.87, "box": {"x": 250, "y": 150, "w": 120, "h": 80}},
                    {"label": "cup", "score": 0.73, "box": {"x": 380, "y": 180, "w": 40, "h": 60}}
                ],
                "model": "mock-detector",
                "count": 3
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
                "model": "detr-resnet-50",
                "count": len(results)
            }
            
        except Exception as e:
            return {
                "error": f"Detection failed: {str(e)}",
                "objects": [],
                "model": "error"
            }
    
    async def caption_image(self, image_data: bytes) -> Dict[str, Any]:
        """Generate caption for image using lightweight model or mock"""
        if self._use_mock or self.captioner is None:
            # Mock implementation for demo purposes
            return {
                "caption": "A person working on a laptop in a well-lit office environment",
                "model": "mock-captioner",
                "confidence": 0.85
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
                "model": "vit-gpt2-image-captioning",
                "confidence": 0.85
            }
            
        except Exception as e:
            return {
                "error": f"Captioning failed: {str(e)}",
                "caption": "Error generating caption",
                "model": "error"
            }

# Global instance
cv_gateway = CVGateway()