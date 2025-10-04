import json
import requests
import websocket
import uuid
import io
import base64
from PIL import Image
from typing import Dict, Optional


class ComfyUIClient:
    """
    Client to interact with ComfyUI API for sketch-to-photo generation
    Optimized for face preservation and Indian facial features
    """

    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def queue_prompt(self, prompt: Dict, sketch_image: Image.Image) -> str:
        """Queue a prompt with sketch image to ComfyUI"""

        # Upload sketch image
        image_data = self._image_to_bytes(sketch_image)
        upload_response = requests.post(
            f"http://{self.server_address}/upload/image",
            files={"image": ("sketch_input.png", image_data, "image/png")},
            data={"overwrite": "true"}
        )

        if upload_response.status_code != 200:
            raise Exception(f"Failed to upload sketch: {upload_response.text}")

        # Queue the workflow
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')

        response = requests.post(
            f"http://{self.server_address}/prompt",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        return response.json()['prompt_id']

    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> Image.Image:
        """Get generated image from ComfyUI"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        response = requests.get(
            f"http://{self.server_address}/view",
            params=data
        )
        return Image.open(io.BytesIO(response.content))

    def get_history(self, prompt_id: str) -> Dict:
        """Get generation history"""
        response = requests.get(f"http://{self.server_address}/history/{prompt_id}")
        return response.json()

    def generate_sketch_from_composite(
        self,
        composite_image: Image.Image,
        description: str
    ) -> Image.Image:
        """
        Generate a sketch from composite wireframe using ComfyUI

        Args:
            composite_image: PIL Image of the layered composite (wireframe)
            description: Text description of features
        """

        # Load sketch workflow
        with open('comfyui_sketch_workflow.json', 'r') as f:
            workflow = json.load(f)

        # Build sketch prompt
        sketch_prompt = self._build_sketch_prompt(description)
        negative_prompt = "color, colored, photorealistic, photograph, blurry, low quality, watermark, signature, deformed face, distorted features, multiple faces, cartoon, anime, painting"

        # Update workflow
        workflow["2"]["inputs"]["text"] = sketch_prompt
        workflow["3"]["inputs"]["text"] = negative_prompt
        workflow["6"]["inputs"]["image"] = "composite_input.png"

        # Random seed for variation
        import time
        workflow["7"]["inputs"]["seed"] = int(time.time())

        # Queue prompt with composite as reference
        prompt_id = self.queue_prompt(workflow, composite_image)

        # Wait and get result
        result = self._wait_for_completion(prompt_id)

        # Get output sketch
        output_images = result[prompt_id]['outputs']['10']['images']
        return self.get_image(
            output_images[0]['filename'],
            output_images[0]['subfolder'],
            output_images[0]['type']
        )

    def generate_from_sketch(
        self,
        sketch_image: Image.Image,
        description: str,
        preserve_structure: bool = True
    ) -> Image.Image:
        """
        Generate photorealistic image from sketch with maximum face preservation

        Args:
            sketch_image: PIL Image of the sketch
            description: Text description (facial features, skin tone, etc)
            preserve_structure: If True, uses high ControlNet strength
        """

        # Load workflow template
        with open('comfyui_workflow.json', 'r') as f:
            workflow = json.load(f)

        # Build prompt with Indian face specificity
        positive_prompt = self._build_positive_prompt(description)
        negative_prompt = self._build_negative_prompt()

        # Update workflow
        workflow["2"]["inputs"]["text"] = positive_prompt
        workflow["3"]["inputs"]["text"] = negative_prompt
        workflow["6"]["inputs"]["image"] = "sketch_input.png"

        # Set ControlNet strength (higher = more sketch preservation)
        workflow["5"]["inputs"]["strength"] = 0.98 if preserve_structure else 0.85

        # Increase denoise for better quality while preserving structure
        workflow["7"]["inputs"]["denoise"] = 0.65 if preserve_structure else 0.8
        workflow["7"]["inputs"]["cfg"] = 9.0 if preserve_structure else 8.0
        workflow["7"]["inputs"]["steps"] = 35

        # Random seed
        import time
        workflow["7"]["inputs"]["seed"] = int(time.time())

        # Queue prompt
        prompt_id = self.queue_prompt(workflow, sketch_image)

        # Wait for completion and get result
        result = self._wait_for_completion(prompt_id)

        # Get output image
        output_images = result[prompt_id]['outputs']['10']['images']
        return self.get_image(
            output_images[0]['filename'],
            output_images[0]['subfolder'],
            output_images[0]['type']
        )

    def _build_sketch_prompt(self, description: str) -> str:
        """Build optimized prompt for sketch generation from composite"""
        base = "black and white pencil sketch of an Indian person"
        features = f"{description}" if description else "detailed facial features"
        structure = "(following the exact proportions and feature placement:1.4), (maintain wireframe structure:1.3)"
        style = "police sketch artist drawing, line art sketch on paper, monochrome drawing, criminal identification sketch, frontal view"
        quality = "South Asian features, realistic proportions, detailed shading, professional sketch"

        return f"{base}, ({features}:1.2), {structure}, {style}, {quality}"

    def _build_positive_prompt(self, description: str) -> str:
        """Build optimized positive prompt for Indian faces"""
        base = "photorealistic portrait, Indian person"
        features = f"{description}" if description else "detailed facial features"
        structure = "(preserve exact face structure:1.5), (maintain sketch proportions:1.5), (same facial features:1.4)"
        style = "professional police mugshot, frontal view, neutral expression, harsh overhead lighting, plain gray background"
        quality = "natural Indian skin tone, sharp focus, high quality photograph, documentary style, realistic"

        return f"{base}, ({features}:1.2), {structure}, {style}, {quality}"

    def _build_negative_prompt(self) -> str:
        """Build negative prompt to avoid face changes"""
        return (
            "cartoon, anime, drawing, painting, sketch lines, pencil marks, deformed face, "
            "distorted features, multiple faces, blurry, low quality, watermark, "
            "signature, different face structure, modified proportions, unrealistic, "
            "artistic style, wrong ethnicity, western features, different nose, "
            "different eyes, different mouth, changed face shape, altered features, "
            "different person, regenerated face, fantasy, illustration"
        )

    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes"""
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        return img_buffer.getvalue()

    def _wait_for_completion(self, prompt_id: str, timeout: int = 120) -> Dict:
        """Wait for ComfyUI to complete generation"""
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            if prompt_id in history:
                return history
            time.sleep(1)

        raise TimeoutError(f"Generation timed out after {timeout}s")


# Example usage
if __name__ == "__main__":
    client = ComfyUIClient()

    # Load sketch
    sketch = Image.open("test_sketch.png")

    # Generate with description
    result = client.generate_from_sketch(
        sketch_image=sketch,
        description="male, wheatish complexion, mustache, oval face shape, almond eyes",
        preserve_structure=True
    )

    result.save("output.png")
    print("Generated image saved as output.png")
