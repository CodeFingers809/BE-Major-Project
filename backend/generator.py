import requests
import urllib.parse
from PIL import Image
import io
import time
import base64
from typing import Optional
from comfyui_client import ComfyUIClient


class SketchGenerator:
    """
    Generates and refines police sketches from descriptions using ComfyUI
    """

    def __init__(self, use_comfyui: bool = True):
        self.use_comfyui = use_comfyui
        self.base_url = "https://image.pollinations.ai/prompt/"

        if use_comfyui:
            try:
                self.comfyui = ComfyUIClient()
                print("SketchGenerator: Using ComfyUI for sketch generation")
            except Exception as e:
                print(f"SketchGenerator: ComfyUI not available ({e}), falling back to Pollinations.ai")
                self.use_comfyui = False

    def generate_sketch(self, description: str, reference_image: Optional[Image.Image] = None) -> Image.Image:
        """
        Generate a black and white sketch from description
        Uses ComfyUI with composite image for proper proportions

        Args:
            description: Text description of facial features
            reference_image: Composite wireframe image for proportional guidance
        """

        # Try ComfyUI first if available and we have a composite
        if self.use_comfyui and reference_image:
            try:
                print("Generating sketch using ComfyUI with composite reference...")
                return self.comfyui.generate_sketch_from_composite(
                    composite_image=reference_image,
                    description=description
                )
            except Exception as e:
                print(f"ComfyUI sketch generation failed: {e}, falling back to Pollinations.ai")
                self.use_comfyui = False

        # Fallback to Pollinations.ai
        print("Generating sketch using Pollinations.ai...")
        sketch_prompt = self._build_sketch_prompt(description, has_reference=reference_image is not None)
        encoded_prompt = urllib.parse.quote(sketch_prompt)

        if reference_image:
            enhanced_prompt = f"{sketch_prompt}, following the exact facial proportions and feature placement shown, maintain the structure and layout"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)

        image_url = f"{self.base_url}{encoded_prompt}?width=512&height=512&seed={int(time.time())}"

        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            else:
                raise Exception(f"API returned status code {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to generate sketch: {str(e)}")

    def _build_sketch_prompt(self, description: str, has_reference: bool = False) -> str:
        """Build optimized prompt for sketch generation"""
        base_prompt = f"black and white pencil sketch of an Indian person, {description}, police sketch artist drawing, detailed facial features, South Asian features, realistic proportions, line art sketch on paper, monochrome drawing, criminal identification sketch"

        if has_reference:
            base_prompt += ", following the facial structure and proportions provided"

        return base_prompt


class ImageColorizer:
    """
    Colorizes sketches while preserving the exact sketch structure
    Uses ComfyUI with ControlNet for maximum face preservation
    """

    def __init__(self, use_comfyui: bool = True):
        self.use_comfyui = use_comfyui
        self.base_url = "https://image.pollinations.ai/prompt/"

        if use_comfyui:
            try:
                self.comfyui = ComfyUIClient()
                print("ImageColorizer: Using ComfyUI for colorization")
            except Exception as e:
                print(f"ImageColorizer: ComfyUI not available ({e}), falling back to Pollinations.ai")
                self.use_comfyui = False

    def colorize_sketch(self, sketch_image: Image.Image, description: str) -> Image.Image:
        """
        Colorize a sketch while strictly preserving its structure
        Uses ComfyUI + ControlNet with high strength for maximum preservation
        """

        # Try ComfyUI first (local, better quality, uses ControlNet)
        if self.use_comfyui:
            try:
                print("Colorizing sketch using ComfyUI with ControlNet...")
                return self.comfyui.generate_from_sketch(
                    sketch_image=sketch_image,
                    description=description,
                    preserve_structure=True  # Uses 0.98 ControlNet strength
                )
            except Exception as e:
                print(f"ComfyUI colorization failed: {e}, falling back to Pollinations.ai")
                self.use_comfyui = False

        # Fallback to Pollinations.ai
        print("Colorizing sketch using Pollinations.ai...")
        color_prompt = self._build_colorization_prompt(description)
        encoded_prompt = urllib.parse.quote(color_prompt)
        image_url = f"{self.base_url}{encoded_prompt}?width=512&height=512&nologo=true&enhance=true&seed={int(time.time())}"

        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            else:
                raise Exception(f"API returned status code {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to colorize sketch: {str(e)}")

    def _build_colorization_prompt(self, description: str) -> str:
        """Build optimized prompt for colorization"""
        return f"colorize this police sketch into a realistic mugshot photograph, Indian person, {description}, frontal view, neutral expression, harsh police station lighting, plain background, realistic Indian skin tone, South Asian facial features, criminal booking photo, high resolution, sharp focus, STRICTLY follow the sketch details and features, documentary photography style"
