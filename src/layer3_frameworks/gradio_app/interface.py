"""Gradio Interface - Computer Vision Tools"""

import gradio as gr
import asyncio
from io import BytesIO
import numpy as np
from PIL import Image

def describe_image(image_array):
    """
    Lightweight image description using the CV gateway
    Args:
        image_array: numpy array from Gradio Image input
    Returns:
        str: Image description
    """
    try:
        # Import CV gateway
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
        from layer2_interfaces.gateways.cv_gateway import cv_gateway
        
        # Convert numpy array to PIL Image, then to bytes
        if isinstance(image_array, np.ndarray):
            pil_image = Image.fromarray(image_array.astype('uint8'))
        else:
            pil_image = image_array
            
        # Convert to bytes
        img_buffer = BytesIO()
        pil_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        # Run async CV analysis in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(cv_gateway.caption_image(image_bytes))
            
            if "error" in result:
                return f"Analysis failed: {result['error']}"
            
            caption = result.get('caption', 'No description available')
            model = result.get('model', 'unknown')
            
            return f"Description: {caption}\n\nModel: {model}"
            
        finally:
            loop.close()
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def detect_objects(image_array):
    """
    Object detection using the CV gateway
    Args:
        image_array: numpy array from Gradio Image input
    Returns:
        str: Detected objects list
    """
    try:
        # Import CV gateway
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
        from layer2_interfaces.gateways.cv_gateway import cv_gateway
        
        # Convert numpy array to bytes
        if isinstance(image_array, np.ndarray):
            pil_image = Image.fromarray(image_array.astype('uint8'))
        else:
            pil_image = image_array
            
        img_buffer = BytesIO()
        pil_image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        # Run async object detection
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(cv_gateway.detect_objects(image_bytes))
            
            if "error" in result:
                return f"Detection failed: {result['error']}"
            
            objects = result.get('objects', [])
            count = result.get('count', 0)
            model = result.get('model', 'unknown')
            
            if count == 0:
                return f"No objects detected.\nModel: {model}"
            
            output = f"Detected {count} objects:\n"
            for obj in objects:
                label = obj.get('label', 'unknown')
                score = obj.get('score', 0.0)
                output += f"- {label}: {score:.2f}\n"
            
            output += f"\nModel: {model}"
            return output
            
        finally:
            loop.close()
            
    except Exception as e:
        return f"Error detecting objects: {str(e)}"

def create_cv_interface():
    """Create the Gradio interface for computer vision tools"""
    
    with gr.Blocks(
        title="Missiora CV Tools",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("# 🔍 Computer Vision Tools")
        gr.Markdown("Upload an image for AI-powered analysis using lightweight models.")
        
        with gr.Tab("Image Captioning"):
            with gr.Row():
                with gr.Column():
                    caption_image = gr.Image(
                        type="numpy",
                        label="Upload Image for Description"
                    )
                    caption_btn = gr.Button("Generate Caption", variant="primary")
                
                with gr.Column():
                    caption_output = gr.Textbox(
                        label="Generated Description",
                        lines=6,
                        interactive=False
                    )
            
            caption_btn.click(
                fn=describe_image,
                inputs=[caption_image],
                outputs=[caption_output]
            )
        
        with gr.Tab("Object Detection"):
            with gr.Row():
                with gr.Column():
                    detect_image = gr.Image(
                        type="numpy",
                        label="Upload Image for Object Detection"
                    )
                    detect_btn = gr.Button("Detect Objects", variant="primary")
                
                with gr.Column():
                    detect_output = gr.Textbox(
                        label="Detected Objects",
                        lines=8,
                        interactive=False
                    )
            
            detect_btn.click(
                fn=detect_objects,
                inputs=[detect_image],
                outputs=[detect_output]
            )
        
        # Examples section
        gr.Markdown("### Example Tasks")
        gr.Markdown("- Upload a photo to get an AI-generated description")
        gr.Markdown("- Detect and identify objects in images")
        gr.Markdown("- Powered by lightweight computer vision models")
    
    return interface

# For standalone testing
if __name__ == "__main__":
    interface = create_cv_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )