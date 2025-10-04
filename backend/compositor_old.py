from PIL import Image, ImageDraw
import os
from typing import Dict
from io import BytesIO


class FacialFeatureCompositor:
    """
    Creates composite images by layering facial feature selections
    Like an artist drawing proportions first
    """

    def __init__(self):
        self.canvas_size = (512, 512)

    def create_composite(self, features: Dict) -> Image.Image:
        """
        Layer facial features like an artist sketching proportions
        Each feature is drawn as an outline/stroke on white background
        """
        width, height = self.canvas_size

        # Start with white canvas
        composite = Image.new('RGBA', (width, height), (255, 255, 255, 255))

        # Layer 1: Face shape (base structure)
        if 'faceShape' in features:
            face_layer = self._create_face_shape_layer(features['faceShape'], width, height)
            composite = Image.alpha_composite(composite, face_layer)

        # Layer 2: Eyebrows (top features)
        if 'eyebrows' in features:
            eyebrow_layer = self._create_eyebrow_layer(features['eyebrows'], width, height)
            composite = Image.alpha_composite(composite, eyebrow_layer)

        # Layer 3: Eyes
        if 'eyeShape' in features:
            eye_layer = self._create_eye_layer(features['eyeShape'], width, height)
            composite = Image.alpha_composite(composite, eye_layer)

        # Layer 4: Nose
        if 'noseType' in features:
            nose_layer = self._create_nose_layer(features['noseType'], width, height)
            composite = Image.alpha_composite(composite, nose_layer)

        # Layer 5: Mouth
        if 'mouthShape' in features:
            mouth_layer = self._create_mouth_layer(features['mouthShape'], width, height)
            composite = Image.alpha_composite(composite, mouth_layer)

        # Convert back to RGB
        final = Image.new('RGB', (width, height), 'white')
        final.paste(composite, (0, 0), composite)

        return final

    def _create_face_shape_layer(self, shape: str, width: int, height: int) -> Image.Image:
        """Create face outline layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x, center_y = width // 2, height // 2

        if shape == 'oval':
            draw.ellipse([100, 80, 412, 480], outline='black', width=3)
        elif shape == 'round':
            draw.ellipse([100, 100, 412, 460], outline='black', width=3)
        elif shape == 'square':
            draw.rectangle([100, 100, 412, 450], outline='black', width=3)
        elif shape == 'diamond':
            points = [(center_x, 80), (380, center_y), (center_x, 460), (132, center_y)]
            draw.polygon(points, outline='black', width=3)
        elif shape == 'heart':
            draw.arc([80, 80, 240, 200], 180, 360, fill='black', width=3)
            draw.arc([272, 80, 432, 200], 180, 360, fill='black', width=3)
            draw.line([(80, 140), (center_x, 460)], fill='black', width=3)
            draw.line([(432, 140), (center_x, 460)], fill='black', width=3)
        else:  # oblong
            draw.ellipse([120, 80, 392, 480], outline='black', width=3)

        return layer

    def _create_eyebrow_layer(self, eyebrow_type: str, width: int, height: int) -> Image.Image:
        """Create eyebrow layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        left_x, right_x = 180, 332
        y = 170

        if eyebrow_type == 'straight':
            draw.line([(left_x-35, y), (left_x+35, y)], fill='black', width=4)
            draw.line([(right_x-35, y), (right_x+35, y)], fill='black', width=4)
        elif eyebrow_type == 'arched':
            draw.arc([left_x-35, y-15, left_x+35, y+5], 180, 360, fill='black', width=4)
            draw.arc([right_x-35, y-15, right_x+35, y+5], 180, 360, fill='black', width=4)
        elif eyebrow_type == 'bushy':
            draw.line([(left_x-35, y), (left_x+35, y)], fill='black', width=6)
            draw.line([(right_x-35, y), (right_x+35, y)], fill='black', width=6)
        elif eyebrow_type == 'thin':
            draw.line([(left_x-35, y), (left_x+35, y)], fill='black', width=2)
            draw.line([(right_x-35, y), (right_x+35, y)], fill='black', width=2)
        else:
            draw.line([(left_x-35, y), (left_x+35, y)], fill='black', width=4)
            draw.line([(right_x-35, y), (right_x+35, y)], fill='black', width=4)

        return layer

    def _create_eye_layer(self, eye_shape: str, width: int, height: int) -> Image.Image:
        """Create eyes layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        left_x, right_x = 180, 332
        y = 200

        if eye_shape == 'almond':
            draw.ellipse([left_x-30, y-15, left_x+30, y+15], outline='black', width=3)
            draw.ellipse([left_x-8, y-8, left_x+8, y+8], fill='black')
            draw.ellipse([right_x-30, y-15, right_x+30, y+15], outline='black', width=3)
            draw.ellipse([right_x-8, y-8, right_x+8, y+8], fill='black')
        elif eye_shape == 'round':
            draw.ellipse([left_x-25, y-25, left_x+25, y+25], outline='black', width=3)
            draw.ellipse([left_x-8, y-8, left_x+8, y+8], fill='black')
            draw.ellipse([right_x-25, y-25, right_x+25, y+25], outline='black', width=3)
            draw.ellipse([right_x-8, y-8, right_x+8, y+8], fill='black')
        else:
            draw.ellipse([left_x-30, y-15, left_x+30, y+15], outline='black', width=3)
            draw.ellipse([left_x-8, y-8, left_x+8, y+8], fill='black')
            draw.ellipse([right_x-30, y-15, right_x+30, y+15], outline='black', width=3)
            draw.ellipse([right_x-8, y-8, right_x+8, y+8], fill='black')

        return layer

    def _create_nose_layer(self, nose_type: str, width: int, height: int) -> Image.Image:
        """Create nose layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        y = 280

        if nose_type == 'straight':
            draw.line([(center_x, 220), (center_x, y)], fill='black', width=3)
            draw.arc([center_x-15, y-10, center_x+15, y+10], 0, 180, fill='black', width=3)
        elif nose_type == 'broad':
            draw.line([(center_x, 220), (center_x, y)], fill='black', width=4)
            draw.arc([center_x-20, y-12, center_x+20, y+12], 0, 180, fill='black', width=3)
        elif nose_type == 'button':
            draw.line([(center_x, 220), (center_x, y-10)], fill='black', width=3)
            draw.ellipse([center_x-15, y-15, center_x+15, y+5], outline='black', width=3)
        else:
            draw.line([(center_x, 220), (center_x, y)], fill='black', width=3)
            draw.arc([center_x-15, y-10, center_x+15, y+10], 0, 180, fill='black', width=3)

        return layer

    def _create_mouth_layer(self, mouth_shape: str, width: int, height: int) -> Image.Image:
        """Create mouth layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        y = 360

        if mouth_shape == 'full':
            draw.arc([center_x-40, y-15, center_x+40, y+5], 0, 180, fill='black', width=4)
            draw.arc([center_x-40, y-5, center_x+40, y+25], 180, 360, fill='black', width=4)
        elif mouth_shape == 'thin':
            draw.line([(center_x-40, y), (center_x+40, y)], fill='black', width=3)
        elif mouth_shape == 'wide':
            draw.arc([center_x-50, y-15, center_x+50, y+5], 0, 180, fill='black', width=4)
        else:
            draw.arc([center_x-40, y-15, center_x+40, y+5], 0, 180, fill='black', width=3)

        return layer
        """Draw face outline based on shape"""
        center_x, center_y = width // 2, height // 2

        if shape == 'oval':
            draw.ellipse([100, 80, 412, 480], outline='black', width=2)
        elif shape == 'round':
            draw.ellipse([100, 100, 412, 460], outline='black', width=2)
        elif shape == 'square':
            draw.rectangle([100, 100, 412, 450], outline='black', width=2)
        elif shape == 'diamond':
            points = [(center_x, 80), (380, center_y), (center_x, 460), (132, center_y)]
            draw.polygon(points, outline='black', width=2)
        elif shape == 'heart':
            draw.arc([80, 80, 240, 200], 180, 360, fill='black', width=2)
            draw.arc([272, 80, 432, 200], 180, 360, fill='black', width=2)
            draw.line([(80, 140), (center_x, 460)], fill='black', width=2)
            draw.line([(432, 140), (center_x, 460)], fill='black', width=2)
        else:  # oblong
            draw.ellipse([120, 80, 392, 480], outline='black', width=2)

    def _draw_eyes(self, draw: ImageDraw.Draw, shape: str, width: int, height: int):
        """Draw eyes based on shape"""
        left_eye_x, right_eye_x = 180, 332
        eye_y = 200

        if shape == 'almond':
            # Left eye
            draw.ellipse([left_eye_x-30, eye_y-15, left_eye_x+30, eye_y+15], outline='black', width=2)
            draw.ellipse([left_eye_x-8, eye_y-8, left_eye_x+8, eye_y+8], fill='black')
            # Right eye
            draw.ellipse([right_eye_x-30, eye_y-15, right_eye_x+30, eye_y+15], outline='black', width=2)
            draw.ellipse([right_eye_x-8, eye_y-8, right_eye_x+8, eye_y+8], fill='black')
        elif shape == 'round':
            # Left eye
            draw.ellipse([left_eye_x-25, eye_y-25, left_eye_x+25, eye_y+25], outline='black', width=2)
            draw.ellipse([left_eye_x-8, eye_y-8, left_eye_x+8, eye_y+8], fill='black')
            # Right eye
            draw.ellipse([right_eye_x-25, eye_y-25, right_eye_x+25, eye_y+25], outline='black', width=2)
            draw.ellipse([right_eye_x-8, eye_y-8, right_eye_x+8, eye_y+8], fill='black')
        else:
            # Default almond-like eyes
            draw.ellipse([left_eye_x-30, eye_y-15, left_eye_x+30, eye_y+15], outline='black', width=2)
            draw.ellipse([left_eye_x-8, eye_y-8, left_eye_x+8, eye_y+8], fill='black')
            draw.ellipse([right_eye_x-30, eye_y-15, right_eye_x+30, eye_y+15], outline='black', width=2)
            draw.ellipse([right_eye_x-8, eye_y-8, right_eye_x+8, eye_y+8], fill='black')

    def _draw_nose(self, draw: ImageDraw.Draw, nose_type: str, width: int, height: int):
        """Draw nose based on type"""
        center_x = width // 2
        nose_y = 280

        if nose_type == 'straight':
            draw.line([(center_x, 220), (center_x, nose_y)], fill='black', width=2)
            draw.arc([center_x-15, nose_y-10, center_x+15, nose_y+10], 0, 180, fill='black', width=2)
        elif nose_type == 'broad':
            draw.line([(center_x, 220), (center_x, nose_y)], fill='black', width=3)
            draw.arc([center_x-20, nose_y-12, center_x+20, nose_y+12], 0, 180, fill='black', width=2)
        else:
            draw.line([(center_x, 220), (center_x, nose_y)], fill='black', width=2)
            draw.arc([center_x-15, nose_y-10, center_x+15, nose_y+10], 0, 180, fill='black', width=2)

    def _draw_mouth(self, draw: ImageDraw.Draw, mouth_shape: str, width: int, height: int):
        """Draw mouth based on shape"""
        center_x = width // 2
        mouth_y = 360

        if mouth_shape == 'full':
            draw.arc([center_x-40, mouth_y-15, center_x+40, mouth_y+15], 0, 180, fill='black', width=3)
            draw.arc([center_x-40, mouth_y-5, center_x+40, mouth_y+25], 180, 360, fill='black', width=3)
        elif mouth_shape == 'thin':
            draw.line([(center_x-40, mouth_y), (center_x+40, mouth_y)], fill='black', width=2)
        elif mouth_shape == 'wide':
            draw.arc([center_x-50, mouth_y-15, center_x+50, mouth_y+15], 0, 180, fill='black', width=3)
        else:
            draw.arc([center_x-40, mouth_y-15, center_x+40, mouth_y+15], 0, 180, fill='black', width=2)

    def _draw_eyebrows(self, draw: ImageDraw.Draw, eyebrow_type: str, width: int, height: int):
        """Draw eyebrows based on type"""
        left_brow_x, right_brow_x = 180, 332
        brow_y = 170

        if eyebrow_type == 'straight':
            draw.line([(left_brow_x-35, brow_y), (left_brow_x+35, brow_y)], fill='black', width=3)
            draw.line([(right_brow_x-35, brow_y), (right_brow_x+35, brow_y)], fill='black', width=3)
        elif eyebrow_type == 'arched':
            draw.arc([left_brow_x-35, brow_y-10, left_brow_x+35, brow_y+10], 180, 360, fill='black', width=3)
            draw.arc([right_brow_x-35, brow_y-10, right_brow_x+35, brow_y+10], 180, 360, fill='black', width=3)
        elif eyebrow_type == 'bushy':
            draw.line([(left_brow_x-35, brow_y), (left_brow_x+35, brow_y)], fill='black', width=5)
            draw.line([(right_brow_x-35, brow_y), (right_brow_x+35, brow_y)], fill='black', width=5)
        else:
            draw.line([(left_brow_x-35, brow_y), (left_brow_x+35, brow_y)], fill='black', width=3)
            draw.line([(right_brow_x-35, brow_y), (right_brow_x+35, brow_y)], fill='black', width=3)
