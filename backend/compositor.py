from PIL import Image, ImageDraw, ImageFont
from typing import Dict
import os


class FacialFeatureCompositor:
    """
    Creates composite images by layering facial feature selections
    Like an artist drawing proportions first - creates a realistic wireframe
    that can be used as a reference for AI sketch generation
    """

    def __init__(self):
        self.canvas_size = (512, 512)
        # More realistic face proportions
        self.face_width = 260
        self.face_height = 360

    def create_composite(self, features: Dict) -> Image.Image:
        """
        Layer facial features like an artist sketching proportions
        Creates a detailed wireframe with proper anatomical proportions
        """
        width, height = self.canvas_size
        center_x = width // 2

        # Start with light gray canvas for better visibility
        composite = Image.new('RGBA', (width, height), (245, 245, 245, 255))

        # Layer 1: Face shape (base structure) - centered
        if 'faceShape' in features:
            face_layer = self._create_face_shape_layer(features['faceShape'], width, height)
            composite = Image.alpha_composite(composite, face_layer)

        # Layer 2: Facial hair outline (if applicable, drawn before other features for depth)
        if features.get('facialHair') and features['facialHair'] != 'clean shaven':
            hair_layer = self._create_facial_hair_layer(features['facialHair'], width, height)
            composite = Image.alpha_composite(composite, hair_layer)

        # Layer 3: Hair
        if 'hairType' in features:
            hair_layer = self._create_hair_layer(features['hairType'], width, height)
            composite = Image.alpha_composite(composite, hair_layer)

        # Layer 4: Eyebrows
        if 'eyebrows' in features:
            eyebrow_layer = self._create_eyebrow_layer(features['eyebrows'], width, height)
            composite = Image.alpha_composite(composite, eyebrow_layer)

        # Layer 5: Eyes
        if 'eyeShape' in features:
            eye_layer = self._create_eye_layer(features['eyeShape'], width, height)
            composite = Image.alpha_composite(composite, eye_layer)

        # Layer 6: Nose
        if 'noseType' in features:
            nose_layer = self._create_nose_layer(features['noseType'], width, height)
            composite = Image.alpha_composite(composite, nose_layer)

        # Layer 7: Mouth
        if 'mouthShape' in features:
            mouth_layer = self._create_mouth_layer(features['mouthShape'], width, height)
            composite = Image.alpha_composite(composite, mouth_layer)

        # Layer 8: Distinctive marks
        if features.get('distinctiveMarks') and features['distinctiveMarks'] != 'none':
            marks_layer = self._create_marks_layer(features['distinctiveMarks'], width, height)
            composite = Image.alpha_composite(composite, marks_layer)

        # Convert back to RGB
        final = Image.new('RGB', (width, height), (245, 245, 245))
        final.paste(composite, (0, 0), composite)

        return final

    def _create_face_shape_layer(self, shape: str, width: int, height: int) -> Image.Image:
        """Create face outline layer with proper proportions"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2

        # Better proportioned face boundaries
        face_left = center_x - self.face_width // 2
        face_right = center_x + self.face_width // 2
        face_top = center_y - self.face_height // 2
        face_bottom = center_y + self.face_height // 2

        if shape == 'oval':
            draw.ellipse([face_left, face_top, face_right, face_bottom], outline='black', width=4)
        elif shape == 'round':
            # More circular
            face_adjust = (self.face_height - self.face_width) // 2
            draw.ellipse([face_left, face_top + face_adjust, face_right, face_bottom - face_adjust], outline='black', width=4)
        elif shape == 'square':
            draw.rectangle([face_left, face_top, face_right, face_bottom], outline='black', width=4)
        elif shape == 'diamond':
            points = [(center_x, face_top), (face_right, center_y), (center_x, face_bottom), (face_left, center_y)]
            draw.polygon(points, outline='black', width=4)
        elif shape == 'heart':
            # Heart shape with proper proportions
            draw.arc([face_left, face_top, center_x - 10, face_top + 100], 180, 360, fill='black', width=4)
            draw.arc([center_x + 10, face_top, face_right, face_top + 100], 180, 360, fill='black', width=4)
            draw.line([(face_left, face_top + 50), (center_x, face_bottom)], fill='black', width=4)
            draw.line([(face_right, face_top + 50), (center_x, face_bottom)], fill='black', width=4)
        else:  # oblong
            draw.ellipse([face_left + 20, face_top, face_right - 20, face_bottom], outline='black', width=4)

        return layer

    def _create_eyebrow_layer(self, eyebrow_type: str, width: int, height: int) -> Image.Image:
        """Create eyebrow layer with realistic positioning"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        eye_spacing = 75  # Distance from center to each eye
        eyebrow_y = center_y - 70

        left_x = center_x - eye_spacing
        right_x = center_x + eye_spacing

        if eyebrow_type == 'straight':
            draw.line([(left_x-40, eyebrow_y), (left_x+40, eyebrow_y)], fill='black', width=5)
            draw.line([(right_x-40, eyebrow_y), (right_x+40, eyebrow_y)], fill='black', width=5)
        elif eyebrow_type == 'arched':
            draw.arc([left_x-40, eyebrow_y-15, left_x+40, eyebrow_y+5], 180, 360, fill='black', width=5)
            draw.arc([right_x-40, eyebrow_y-15, right_x+40, eyebrow_y+5], 180, 360, fill='black', width=5)
        elif eyebrow_type == 'rounded':
            draw.arc([left_x-40, eyebrow_y-10, left_x+40, eyebrow_y+10], 180, 360, fill='black', width=5)
            draw.arc([right_x-40, eyebrow_y-10, right_x+40, eyebrow_y+10], 180, 360, fill='black', width=5)
        elif eyebrow_type == 'angled':
            draw.line([(left_x-40, eyebrow_y+5), (left_x-10, eyebrow_y-5), (left_x+40, eyebrow_y)], fill='black', width=5)
            draw.line([(right_x-40, eyebrow_y), (right_x+10, eyebrow_y-5), (right_x+40, eyebrow_y+5)], fill='black', width=5)
        elif eyebrow_type == 'bushy':
            draw.line([(left_x-40, eyebrow_y), (left_x+40, eyebrow_y)], fill='black', width=8)
            draw.line([(right_x-40, eyebrow_y), (right_x+40, eyebrow_y)], fill='black', width=8)
        elif eyebrow_type == 'thin':
            draw.line([(left_x-40, eyebrow_y), (left_x+40, eyebrow_y)], fill='black', width=3)
            draw.line([(right_x-40, eyebrow_y), (right_x+40, eyebrow_y)], fill='black', width=3)
        else:
            draw.line([(left_x-40, eyebrow_y), (left_x+40, eyebrow_y)], fill='black', width=5)
            draw.line([(right_x-40, eyebrow_y), (right_x+40, eyebrow_y)], fill='black', width=5)

        return layer

    def _create_eye_layer(self, eye_shape: str, width: int, height: int) -> Image.Image:
        """Create eyes layer with realistic proportions"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        eye_spacing = 75
        eye_y = center_y - 40

        left_x = center_x - eye_spacing
        right_x = center_x + eye_spacing

        if eye_shape == 'almond':
            # Almond shaped eyes
            draw.ellipse([left_x-35, eye_y-18, left_x+35, eye_y+18], outline='black', width=4)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-35, eye_y-18, right_x+35, eye_y+18], outline='black', width=4)
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')
        elif eye_shape == 'round':
            # Round eyes
            draw.ellipse([left_x-28, eye_y-28, left_x+28, eye_y+28], outline='black', width=4)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-28, eye_y-28, right_x+28, eye_y+28], outline='black', width=4)
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')
        elif eye_shape == 'hooded':
            # Hooded eyes with heavy upper lid
            draw.ellipse([left_x-35, eye_y-15, left_x+35, eye_y+15], outline='black', width=4)
            draw.arc([left_x-35, eye_y-25, left_x+35, eye_y-5], 180, 360, fill='black', width=3)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-35, eye_y-15, right_x+35, eye_y+15], outline='black', width=4)
            draw.arc([right_x-35, eye_y-25, right_x+35, eye_y-5], 180, 360, fill='black', width=3)
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')
        elif eye_shape == 'upturned':
            # Upturned eyes
            points_l = [(left_x-35, eye_y+5), (left_x, eye_y-10), (left_x+35, eye_y-15)]
            points_r = [(right_x-35, eye_y-15), (right_x, eye_y-10), (right_x+35, eye_y+5)]
            draw.line(points_l, fill='black', width=4)
            draw.line(points_r, fill='black', width=4)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')
        elif eye_shape == 'downturned':
            # Downturned eyes
            points_l = [(left_x-35, eye_y-15), (left_x, eye_y-10), (left_x+35, eye_y+5)]
            points_r = [(right_x-35, eye_y+5), (right_x, eye_y-10), (right_x+35, eye_y-15)]
            draw.line(points_l, fill='black', width=4)
            draw.line(points_r, fill='black', width=4)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')
        else:  # monolid or default
            draw.ellipse([left_x-35, eye_y-15, left_x+35, eye_y+15], outline='black', width=4)
            draw.ellipse([left_x-10, eye_y-10, left_x+10, eye_y+10], fill='black')
            draw.ellipse([right_x-35, eye_y-15, right_x+35, eye_y+15], outline='black', width=4)
            draw.ellipse([right_x-10, eye_y-10, right_x+10, eye_y+10], fill='black')

        return layer

    def _create_nose_layer(self, nose_type: str, width: int, height: int) -> Image.Image:
        """Create nose layer with realistic proportions"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        nose_start_y = center_y - 20
        nose_end_y = center_y + 50

        if nose_type == 'straight':
            draw.line([(center_x, nose_start_y), (center_x, nose_end_y)], fill='black', width=4)
            draw.arc([center_x-18, nose_end_y-12, center_x+18, nose_end_y+12], 0, 180, fill='black', width=4)
            # Nostrils
            draw.ellipse([center_x-15, nose_end_y, center_x-8, nose_end_y+7], outline='black', width=2)
            draw.ellipse([center_x+8, nose_end_y, center_x+15, nose_end_y+7], outline='black', width=2)
        elif nose_type == 'aquiline':
            # Hook/curved nose
            draw.arc([center_x-15, nose_start_y-10, center_x+15, nose_end_y], 180, 270, fill='black', width=4)
            draw.arc([center_x-18, nose_end_y-12, center_x+18, nose_end_y+12], 0, 180, fill='black', width=4)
            draw.ellipse([center_x-15, nose_end_y, center_x-8, nose_end_y+7], outline='black', width=2)
            draw.ellipse([center_x+8, nose_end_y, center_x+15, nose_end_y+7], outline='black', width=2)
        elif nose_type == 'broad':
            draw.line([(center_x, nose_start_y), (center_x, nose_end_y)], fill='black', width=5)
            draw.arc([center_x-22, nose_end_y-15, center_x+22, nose_end_y+15], 0, 180, fill='black', width=4)
            draw.ellipse([center_x-18, nose_end_y, center_x-10, nose_end_y+8], outline='black', width=2)
            draw.ellipse([center_x+10, nose_end_y, center_x+18, nose_end_y+8], outline='black', width=2)
        elif nose_type == 'button':
            draw.line([(center_x, nose_start_y), (center_x, nose_end_y-5)], fill='black', width=4)
            draw.ellipse([center_x-16, nose_end_y-12, center_x+16, nose_end_y+8], outline='black', width=4)
            draw.ellipse([center_x-12, nose_end_y+2, center_x-7, nose_end_y+7], fill='black')
            draw.ellipse([center_x+7, nose_end_y+2, center_x+12, nose_end_y+7], fill='black')
        elif nose_type == 'narrow':
            draw.line([(center_x, nose_start_y), (center_x, nose_end_y)], fill='black', width=3)
            draw.arc([center_x-14, nose_end_y-10, center_x+14, nose_end_y+10], 0, 180, fill='black', width=3)
            draw.ellipse([center_x-12, nose_end_y, center_x-7, nose_end_y+5], outline='black', width=2)
            draw.ellipse([center_x+7, nose_end_y, center_x+12, nose_end_y+5], outline='black', width=2)
        else:  # roman or default
            # Prominent bridge
            draw.line([(center_x, nose_start_y), (center_x, nose_end_y)], fill='black', width=5)
            draw.line([(center_x-3, nose_start_y), (center_x-3, nose_end_y)], fill='black', width=2)
            draw.arc([center_x-18, nose_end_y-12, center_x+18, nose_end_y+12], 0, 180, fill='black', width=4)
            draw.ellipse([center_x-15, nose_end_y, center_x-8, nose_end_y+7], outline='black', width=2)
            draw.ellipse([center_x+8, nose_end_y, center_x+15, nose_end_y+7], outline='black', width=2)

        return layer

    def _create_mouth_layer(self, mouth_shape: str, width: int, height: int) -> Image.Image:
        """Create mouth layer with realistic proportions"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        mouth_y = center_y + 90

        if mouth_shape == 'full':
            # Full lips - upper and lower
            draw.arc([center_x-45, mouth_y-18, center_x+45, mouth_y], 0, 180, fill='black', width=5)
            draw.arc([center_x-45, mouth_y, center_x+45, mouth_y+28], 180, 360, fill='black', width=5)
        elif mouth_shape == 'thin':
            # Thin lips
            draw.line([(center_x-42, mouth_y), (center_x+42, mouth_y)], fill='black', width=4)
            draw.arc([center_x-42, mouth_y-5, center_x+42, mouth_y+5], 0, 180, fill='black', width=3)
        elif mouth_shape == 'wide':
            # Wide mouth
            draw.arc([center_x-55, mouth_y-15, center_x+55, mouth_y+2], 0, 180, fill='black', width=5)
            draw.arc([center_x-55, mouth_y-2, center_x+55, mouth_y+20], 180, 360, fill='black', width=5)
        elif mouth_shape == 'small':
            # Small mouth
            draw.arc([center_x-30, mouth_y-12, center_x+30, mouth_y], 0, 180, fill='black', width=4)
            draw.arc([center_x-30, mouth_y, center_x+30, mouth_y+18], 180, 360, fill='black', width=4)
        elif mouth_shape == 'bow':
            # Bow-shaped (cupid's bow)
            draw.line([(center_x-45, mouth_y-8), (center_x-15, mouth_y-12), (center_x, mouth_y-8), (center_x+15, mouth_y-12), (center_x+45, mouth_y-8)], fill='black', width=4)
            draw.arc([center_x-45, mouth_y-8, center_x+45, mouth_y+20], 180, 360, fill='black', width=5)
        elif mouth_shape == 'downturned':
            # Downturned mouth
            draw.arc([center_x-45, mouth_y+5, center_x+45, mouth_y+30], 0, 180, fill='black', width=5)
        else:
            # Default
            draw.arc([center_x-42, mouth_y-15, center_x+42, mouth_y], 0, 180, fill='black', width=4)
            draw.arc([center_x-42, mouth_y, center_x+42, mouth_y+22], 180, 360, fill='black', width=4)

        return layer

    def _create_hair_layer(self, hair_type: str, width: int, height: int) -> Image.Image:
        """Create hair layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        face_top = center_y - self.face_height // 2

        if hair_type == 'bald':
            # Just head outline
            draw.arc([center_x-90, face_top-60, center_x+90, face_top+40], 180, 360, fill='black', width=4)
        elif hair_type == 'receding hairline':
            # M-shaped hairline
            draw.arc([center_x-90, face_top-50, center_x-20, face_top+20], 180, 270, fill='black', width=5)
            draw.arc([center_x+20, face_top-50, center_x+90, face_top+20], 270, 360, fill='black', width=5)
            draw.arc([center_x-30, face_top-20, center_x+30, face_top+20], 0, 180, fill='black', width=5)
        elif 'curly' in hair_type:
            # Curly hair - wavy top
            draw.arc([center_x-100, face_top-70, center_x+100, face_top+30], 180, 360, fill='black', width=5)
            for i in range(-80, 81, 20):
                draw.arc([center_x+i-10, face_top-60, center_x+i+10, face_top-40], 0, 360, fill='black', width=2)
        elif 'wavy' in hair_type:
            # Wavy hair
            draw.arc([center_x-100, face_top-70, center_x+100, face_top+30], 180, 360, fill='black', width=5)
            points = []
            for i in range(-90, 91, 30):
                points.append((center_x+i, face_top-50 + (10 if i % 60 == 0 else -10)))
            draw.line(points, fill='black', width=3)
        else:  # straight black or default
            # Straight hair
            draw.arc([center_x-100, face_top-70, center_x+100, face_top+30], 180, 360, fill='black', width=5)
            for i in range(-90, 91, 15):
                draw.line([(center_x+i, face_top-60), (center_x+i, face_top-20)], fill='black', width=2)

        return layer

    def _create_facial_hair_layer(self, facial_hair_type: str, width: int, height: int) -> Image.Image:
        """Create facial hair layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2
        mouth_y = center_y + 90

        if facial_hair_type == 'mustache':
            # Mustache above mouth
            draw.arc([center_x-50, mouth_y-35, center_x-10, mouth_y-10], 0, 180, fill='black', width=6)
            draw.arc([center_x+10, mouth_y-35, center_x+50, mouth_y-10], 0, 180, fill='black', width=6)
        elif facial_hair_type == 'beard':
            # Full beard
            face_bottom = center_y + self.face_height // 2
            draw.arc([center_x-70, mouth_y, center_x+70, face_bottom+30], 0, 180, fill='black', width=8)
            # Connect to sideburns
            draw.line([(center_x-70, mouth_y+20), (center_x-100, center_y)], fill='black', width=6)
            draw.line([(center_x+70, mouth_y+20), (center_x+100, center_y)], fill='black', width=6)
        elif facial_hair_type == 'goatee':
            # Goatee below mouth
            draw.ellipse([center_x-25, mouth_y+15, center_x+25, mouth_y+65], outline='black', fill=(100, 100, 100, 128), width=4)
        elif facial_hair_type == 'stubble':
            # Light stubble around mouth and chin
            for i in range(100):
                import random
                x = center_x + random.randint(-70, 70)
                y = mouth_y + random.randint(-15, 55)
                draw.point((x, y), fill='black')

        return layer

    def _create_marks_layer(self, mark_type: str, width: int, height: int) -> Image.Image:
        """Create distinctive marks layer"""
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)

        center_x = width // 2
        center_y = height // 2

        if 'scar' in mark_type:
            # Scar on left cheek
            scar_x = center_x - 60
            scar_y = center_y + 20
            draw.line([(scar_x, scar_y), (scar_x+30, scar_y+40)], fill='darkred', width=3)
        elif 'mole' in mark_type:
            # Mole on right cheek
            mole_x = center_x + 50
            mole_y = center_y + 30
            draw.ellipse([mole_x-4, mole_y-4, mole_x+4, mole_y+4], fill='black')
        elif 'broken nose' in mark_type:
            # Indication of broken nose (bump on bridge)
            nose_y = center_y + 10
            draw.line([(center_x-8, nose_y), (center_x+8, nose_y)], fill='black', width=6)
        elif 'birthmark' in mark_type:
            # Birthmark on forehead
            mark_y = center_y - 100
            draw.ellipse([center_x-15, mark_y-10, center_x+15, mark_y+10], fill=(139, 69, 19, 128), outline='brown', width=2)

        return layer
