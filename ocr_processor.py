from langchain_ollama import OllamaLLM
from PIL import Image
import json
from typing import Optional, Dict, Any, List
import os

class OCRProcessor:
    def __init__(self, model_name: str):
        self.model = OllamaLLM(model=model_name)

    def process_image(self, image_path: str, format_type: str = "markdown") -> str:
        """
        Process an image and extract text in the specified format
        
        Args:
            image_path: Path to the image file
            format_type: One of ["markdown", "text", "json", "structured", "key_value"]
        """
        # Prepare prompts based on format type
        prompts = {
            "markdown": "Extract text from this image and format it as markdown.",
            "text": "Extract all text from this image in plain text format.",
            "json": "Extract text from this image and return it as a JSON structure.",
            "structured": "Extract any tables, lists, or structured data from this image.",
            "key_value": "Extract key-value pairs from this image."
        }
        
        prompt = prompts.get(format_type, prompts["text"])
        
        try:
            result = self.model.predict(prompt)
            return result
        except Exception as e:
            return f"Error processing image: {str(e)}"