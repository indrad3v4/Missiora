"""Gradio Computer Vision Tools Launcher"""

import gradio as gr
import os
from io import BytesIO
import base64
from PIL import Image
import requests
import torch

class CVToolsApp:
    """Computer Vision tools using Gradio and Hugging Face models"""
    
    def __init__(self):
        self.setup_models()
    
    def setup_models(self):
        """Initialize CV models from Hugging Face Hub"""
        try:
            # Use lightweight models for demonstration
            self.object_detector = None
            self.captioner = None
            self.segmenter = None
            
            # Try to load models if transformers is available
            try:
                from transformers import pipeline
                
                # Object Detection - lightweight model
                self.object_detector = pipeline(
                    "object-detection",
                    model="facebook/detr-resnet-50",
                    device=-1  # CPU only for now
                )
                
                # Image Captioning
                self.captioner = pipeline(
                    "image-to-text",
                    model="Salesforce/blip-image-captioning-base",
                    device=-1  # CPU only
                )
                
            except Exception as model_error:
                print(f"Model loading failed: {model_error}")
            
        except Exception as e:
            print(f"Warning: CV models setup failed: {e}")
    
    def process_image(self, image, task_type):
        """Process image based on selected task"""
        if image is None:
            return "Please upload an image first.", None
        
        try:
            # Convert to PIL Image if needed
            if isinstance(image, str):
                # Base64 string
                image_data = base64.b64decode(image.split(',')[1])
                image = Image.open(BytesIO(image_data))
            elif not isinstance(image, Image.Image):
                image = Image.fromarray(image)
            
            if task_type == "Object Detection (YOLOv8, HF Hub)":
                return self.detect_objects(image)
            elif task_type == "Segment (SAM)":
                return self.segment_image(image)
            elif task_type == "Caption (BLIP-2)":
                return self.caption_image(image)
            else:
                return "Unknown task type.", None
                
        except Exception as e:
            return f"Error processing image: {str(e)}", None
    
    def detect_objects(self, image):
        """Perform object detection"""
        if self.object_detector is None:
            return "Object detection model not available. Install transformers and torch.", image
        
        try:
            results = self.object_detector(image)
            
            # Format results
            detection_text = "Detected Objects:\n"
            for result in results:
                label = result['label']
                score = result['score']
                detection_text += f"- {label}: {score:.2f}\n"
            
            return detection_text, image
            
        except Exception as e:
            return f"Object detection failed: {str(e)}", image
    
    def segment_image(self, image):
        """Image segmentation (placeholder)"""
        return "Segmentation feature coming soon. SAM model requires additional setup.", image
    
    def caption_image(self, image):
        """Generate caption using BLIP-2"""
        if self.captioner is None:
            return "Image captioning model not available. Install transformers.", image
        
        try:
            result = self.captioner(image)
            caption = result[0]['generated_text'] if result else "No caption generated."
            
            return f"Generated Caption:\n{caption}", image
            
        except Exception as e:
            return f"Captioning failed: {str(e)}", image

def create_gradio_app():
    """Create and configure Gradio interface"""
    cv_app = CVToolsApp()
    
    with gr.Blocks(
        title="Missiora CV Tools",
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="amber"
        )
    ) as demo:
        gr.Markdown("# 🔍 Computer Vision Tools")
        gr.Markdown("Upload an image and select a CV task to analyze it using state-of-the-art models.")
        
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    type="pil",
                    label="Upload Image"
                )
                
                task_dropdown = gr.Dropdown(
                    choices=[
                        "Object Detection (YOLOv8, HF Hub)",
                        "Segment (SAM)", 
                        "Caption (BLIP-2)"
                    ],
                    value="Object Detection (YOLOv8, HF Hub)",
                    label="CV Task"
                )
                
                process_btn = gr.Button(
                    "Process Image",
                    variant="primary"
                )
            
            with gr.Column(scale=1):
                result_text = gr.Textbox(
                    label="Results",
                    lines=10,
                    interactive=False
                )
                
                result_image = gr.Image(
                    label="Processed Image",
                    type="pil"
                )
        
        # Event handlers
        process_btn.click(
            fn=cv_app.process_image,
            inputs=[image_input, task_dropdown],
            outputs=[result_text, result_image]
        )
        
        # Examples
        gr.Examples(
            examples=[
                ["Object Detection (YOLOv8, HF Hub)"],
                ["Caption (BLIP-2)"],
                ["Segment (SAM)"]
            ],
            inputs=[task_dropdown],
            label="Try these tasks"
        )
    
    return demo

def launch_gradio_app(host="0.0.0.0", port=7860):
    """Launch the Gradio app"""
    demo = create_gradio_app()
    demo.launch(
        server_name=host,
        server_port=port,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    launch_gradio_app()