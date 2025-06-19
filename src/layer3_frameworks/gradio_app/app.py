"""Standalone Gradio CV Tools App"""

from .launcher import create_gradio_app

if __name__ == "__main__":
    demo = create_gradio_app()
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False
    )