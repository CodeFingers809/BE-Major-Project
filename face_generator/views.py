from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FaceFeatureCategory, FaceFeature, FaceComposition
from .serializers import (
    FaceFeatureCategorySerializer,
    FaceFeatureSerializer,
    FaceCompositionSerializer,
)
from PIL import Image, ImageDraw
import requests
import io
import os
from django.core.files.base import ContentFile
from django.conf import settings
from .local_flux import (
    generate_sketch_fast,
    revise_sketch as revise_sketch_local,
    colorize_sketch as colorize_sketch_local,
)


class FaceFeatureCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for facial feature categories"""

    queryset = FaceFeatureCategory.objects.all()
    serializer_class = FaceFeatureCategorySerializer


class FaceFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for individual facial features"""

    queryset = FaceFeature.objects.all()
    serializer_class = FaceFeatureSerializer


class FaceCompositionViewSet(viewsets.ModelViewSet):
    """API endpoint for face compositions"""

    queryset = FaceComposition.objects.all()
    serializer_class = FaceCompositionSerializer

    @action(detail=True, methods=["post"])
    def generate_composite(self, request, pk=None):
        """Generate a composite image from selected features"""
        composition = self.get_object()

        # Create a blank canvas
        canvas = Image.new("RGB", (512, 512), "white")
        draw = ImageDraw.Draw(canvas)

        # This will be enhanced with actual feature layering
        # For now, save the blank canvas
        buffer = io.BytesIO()
        canvas.save(buffer, format="PNG")
        composition.composite_image.save(
            f"composite_{composition.id}.png", ContentFile(buffer.getvalue()), save=True
        )

        return Response({"status": "composite generated"})

    @action(detail=True, methods=["post"])
    def generate_sketch(self, request, pk=None):
        """Generate realistic pencil sketch using LOCAL Flux Indo Realism on M4"""
        composition = self.get_object()

        # Build prompt for realistic criminal sketch
        features_prompt = composition.get_prompt()

        # Pencil sketch prompt for authentic police sketch artist style
        full_prompt = (
            f"black and white pencil sketch on paper, "
            f"police sketch artist drawing, "
            f"Indian person, "
            f"{features_prompt}, "
            f"realistic facial features, "
            f"South Asian features, "
            f"detailed line art, "
            f"monochrome criminal identification sketch, "
            f"harsh lighting, frontal view, "
            f"mugshot style, "
            f"NOT idealized or pretty, "
            f"authentic law enforcement sketch, "
            f"realistic proportions, "
            f"hand-drawn appearance, "
            f"graphite pencil texture, "
            f"sketch on white paper"
        )

        try:
            # Use LOCAL MFLUX with Indo-Realism LoRA
            import time

            output_filename = f"sketch_{composition.id}_{int(time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "sketches", output_filename)

            # Ensure sketches directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"[Django] Starting local Flux generation...")
            print(f"[Django] Prompt: {full_prompt[:100]}...")

            # Generate using local model (fast mode = 10 steps, ~15-20s on M4)
            generate_sketch_fast(
                prompt=full_prompt,
                output_path=output_path,
                quality="fast",  # Options: "fast" (10 steps), "balanced" (15), "best" (20)
            )

            # Save to model
            composition.sketch_image = f"sketches/{output_filename}"
            composition.save()

            print(
                f"[Django] Generation complete, saved to {composition.sketch_image.url}"
            )

            return Response(
                {
                    "status": "sketch generated locally",
                    "image_url": composition.sketch_image.url,
                    "method": "local_mflux_m4",
                }
            )

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            print(f"[Django] Generation error: {error_details}")

            return Response(
                {"error": f"Local generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def revise_sketch(self, request, pk=None):
        """Revise/edit an existing sketch using Flux 2.1 Klein img2img"""
        composition = self.get_object()

        # Get revision parameters from request
        revision_prompt = request.data.get("prompt", "")
        strength = float(request.data.get("strength", 0.6))
        quality = request.data.get("quality", "balanced")

        # Check if sketch exists
        if not composition.sketch_image:
            return Response(
                {"error": "No sketch to revise. Generate a sketch first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            import time

            # Get existing sketch path
            sketch_path = os.path.join(settings.MEDIA_ROOT, str(composition.sketch_image))

            if not os.path.exists(sketch_path):
                return Response(
                    {"error": "Sketch file not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Build revision prompt with existing features
            features_prompt = composition.get_prompt()
            full_prompt = f"{features_prompt}, {revision_prompt}" if revision_prompt else features_prompt

            output_filename = f"revised_{composition.id}_{int(time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "sketches", output_filename)

            print(f"[Django] Revising sketch with strength {strength}...")
            print(f"[Django] Revision prompt: {full_prompt[:100]}...")

            revise_sketch_local(
                prompt=full_prompt,
                init_image_path=sketch_path,
                output_path=output_path,
                strength=strength,
                quality=quality,
            )

            # Update composition with revised sketch
            composition.sketch_image = f"sketches/{output_filename}"
            composition.save()

            return Response(
                {
                    "status": "sketch revised",
                    "image_url": composition.sketch_image.url,
                    "method": "flux_2.1_klein_img2img",
                }
            )

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[Django] Revision error: {error_details}")

            return Response(
                {"error": f"Revision failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def colorize(self, request, pk=None):
        """Colorize a B&W sketch using Flux 2.1 Klein - preserves structure"""
        composition = self.get_object()

        # Get colorization parameters
        color_prompt = request.data.get("prompt", "")
        quality = request.data.get("quality", "balanced")

        # Check if sketch exists
        if not composition.sketch_image:
            return Response(
                {"error": "No sketch to colorize. Generate a sketch first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            import time

            # Get sketch path
            sketch_path = os.path.join(settings.MEDIA_ROOT, str(composition.sketch_image))

            if not os.path.exists(sketch_path):
                return Response(
                    {"error": "Sketch file not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Build colorization prompt with features
            features_prompt = composition.get_prompt()
            full_prompt = f"{features_prompt}, {color_prompt}" if color_prompt else features_prompt

            output_filename = f"colored_{composition.id}_{int(time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "final", output_filename)

            # Ensure final directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"[Django] Colorizing sketch...")
            print(f"[Django] Color prompt: {full_prompt[:100]}...")

            colorize_sketch_local(
                prompt=full_prompt,
                sketch_path=sketch_path,
                output_path=output_path,
                quality=quality,
            )

            # Save to final_image field
            composition.final_image = f"final/{output_filename}"
            composition.save()

            return Response(
                {
                    "status": "sketch colorized",
                    "image_url": composition.final_image.url,
                    "method": "flux_2.1_klein_colorization",
                }
            )

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[Django] Colorization error: {error_details}")

            return Response(
                {"error": f"Colorization failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def index(request):
    """Main page view"""
    return render(request, "index.html")
