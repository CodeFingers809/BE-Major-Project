from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FaceFeatureCategory, FaceFeature, FaceComposition, GenerationVersion
from .serializers import (
    FaceFeatureCategorySerializer,
    FaceFeatureSerializer,
    FaceCompositionSerializer,
    GenerationVersionSerializer,
)
from PIL import Image, ImageDraw
import requests
import io
import os
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from .bfl_flux import (
    generate_sketch,
    revise_sketch,
    colorize_sketch,
)
from .face_matcher import match_face


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

    def _next_version(self, composition):
        """Get next version number for a composition"""
        last = composition.versions.order_by("-version_number").first()
        return (last.version_number + 1) if last else 1

    def _save_version(
        self, composition, image_path, image_type, prompt_used, parent=None
    ):
        """Create a GenerationVersion record"""
        ver = GenerationVersion(
            composition=composition,
            version_number=self._next_version(composition),
            image_type=image_type,
            prompt_used=prompt_used,
            parent_version=parent,
        )
        rel_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
        ver.image.name = rel_path
        ver.save()
        return ver

    @action(detail=True, methods=["post"])
    def generate_composite(self, request, pk=None):
        """Generate a composite image from selected features"""
        composition = self.get_object()

        canvas = Image.new("RGB", (512, 512), "white")
        draw = ImageDraw.Draw(canvas)

        buffer = io.BytesIO()
        canvas.save(buffer, format="PNG")
        composition.composite_image.save(
            f"composite_{composition.id}.png", ContentFile(buffer.getvalue()), save=True
        )

        return Response({"status": "composite generated"})

    @action(detail=True, methods=["post"])
    def generate_sketch(self, request, pk=None):
        """Generate realistic pencil sketch mugshot using BFL Flux API"""
        composition = self.get_object()
        features_description = composition.get_prompt()

        try:
            import time as _time

            output_filename = f"sketch_{composition.id}_{int(_time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "sketches", output_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Get optional reference image path
            ref_image_path = None
            if composition.reference_image:
                ref_image_path = composition.reference_image.path
                if not os.path.exists(ref_image_path):
                    ref_image_path = None

            print(f"[Django] Starting sketch generation...")
            print(f"[Django] Features: {features_description[:100]}...")
            if composition.user_prompt:
                print(f"[Django] User prompt: {composition.user_prompt[:100]}...")
            if ref_image_path:
                print(f"[Django] Reference image: {ref_image_path}")

            generate_sketch(
                features_description=features_description,
                output_path=output_path,
                user_prompt=composition.user_prompt,
                reference_image_path=ref_image_path,
            )

            composition.sketch_image = f"sketches/{output_filename}"
            composition.save()

            ver = self._save_version(
                composition, output_path, "sketch", features_description
            )

            return Response(
                {
                    "status": "sketch generated",
                    "image_url": composition.sketch_image.url,
                    "method": "flux_kontext_pro" if ref_image_path else "flux_dev",
                    "version": GenerationVersionSerializer(ver).data,
                }
            )

        except Exception as e:
            import traceback

            print(f"[Django] Generation error: {traceback.format_exc()}")
            return Response(
                {"error": f"Generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def revise_sketch(self, request, pk=None):
        """Revise/edit an existing sketch using Flux Kontext Pro"""
        composition = self.get_object()

        revision_prompt = request.data.get("prompt", "")
        overlay_b64 = request.data.get("overlay_image", "")
        conversation_history = request.data.get("conversation_history", [])
        parent_version_id = request.data.get("parent_version_id", None)

        if not revision_prompt:
            return Response(
                {"error": "Please describe what changes to make."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not composition.sketch_image:
            return Response(
                {"error": "No sketch to revise. Generate a sketch first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            import time as _time

            sketch_path = os.path.join(
                settings.MEDIA_ROOT, str(composition.sketch_image)
            )

            if not os.path.exists(sketch_path):
                return Response(
                    {"error": "Sketch file not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # If there's a drawing overlay, composite it onto the sketch
            init_path = sketch_path
            if overlay_b64:
                init_path = self._composite_overlay(
                    sketch_path, overlay_b64, composition.id
                )

            output_filename = f"revised_{composition.id}_{int(_time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "sketches", output_filename)

            print(f"[Django] Revising sketch with Kontext Pro...")
            print(f"[Django] Edit: {revision_prompt[:100]}...")

            # Find parent version — use the one the frontend is working from if provided
            parent = None
            if parent_version_id:
                try:
                    parent = GenerationVersion.objects.get(
                        id=parent_version_id, composition=composition
                    )
                    print(
                        f"[Django] Using explicit parent: v{parent.version_number} (id={parent.id})"
                    )
                except GenerationVersion.DoesNotExist:
                    pass
            if not parent:
                parent = composition.versions.order_by("-version_number").first()

            revise_sketch(
                edit_instruction=revision_prompt,
                init_image_path=init_path,
                output_path=output_path,
                conversation_history=conversation_history,
            )

            composition.sketch_image = f"sketches/{output_filename}"
            composition.save()

            ver = self._save_version(
                composition, output_path, "revision", revision_prompt, parent=parent
            )

            return Response(
                {
                    "status": "sketch revised",
                    "image_url": composition.sketch_image.url,
                    "method": "flux_kontext_pro",
                    "version": GenerationVersionSerializer(ver).data,
                }
            )

        except Exception as e:
            import traceback

            print(f"[Django] Revision error: {traceback.format_exc()}")
            return Response(
                {"error": f"Revision failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _composite_overlay(self, base_path, overlay_b64, comp_id):
        """Merge a drawing overlay (transparent PNG) onto the base sketch image."""
        import time as _time

        base = Image.open(base_path).convert("RGBA")
        overlay_data = base64.b64decode(overlay_b64)
        overlay = Image.open(io.BytesIO(overlay_data)).convert("RGBA")
        overlay = overlay.resize(base.size, Image.LANCZOS)
        merged = Image.alpha_composite(base, overlay)
        merged = merged.convert("RGB")

        out_name = f"overlay_{comp_id}_{int(_time.time())}.png"
        out_path = os.path.join(settings.MEDIA_ROOT, "sketches", out_name)
        merged.save(out_path)
        file_size = os.path.getsize(out_path) / 1024
        print(f"[Django] Overlay composited: {out_path} ({file_size:.1f} KB)")
        return out_path

    @action(detail=True, methods=["post"])
    def colorize(self, request, pk=None):
        """Colorize a B&W sketch into a realistic mugshot using Kontext Pro"""
        composition = self.get_object()

        if not composition.sketch_image:
            return Response(
                {"error": "No sketch to colorize. Generate a sketch first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            import time as _time

            sketch_path = os.path.join(
                settings.MEDIA_ROOT, str(composition.sketch_image)
            )

            if not os.path.exists(sketch_path):
                return Response(
                    {"error": "Sketch file not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            features_description = composition.get_prompt()

            output_filename = f"colored_{composition.id}_{int(_time.time())}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "final", output_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"[Django] Colorizing sketch with Kontext Pro...")

            parent = composition.versions.order_by("-version_number").first()

            colorize_sketch(
                features_description=features_description,
                sketch_path=sketch_path,
                output_path=output_path,
            )

            composition.final_image = f"final/{output_filename}"
            composition.save()

            ver = self._save_version(
                composition,
                output_path,
                "colorized",
                f"[colorize] {features_description}",
                parent=parent,
            )

            return Response(
                {
                    "status": "sketch colorized",
                    "image_url": composition.final_image.url,
                    "method": "flux_kontext_pro",
                    "version": GenerationVersionSerializer(ver).data,
                }
            )

        except Exception as e:
            import traceback

            print(f"[Django] Colorization error: {traceback.format_exc()}")
            return Response(
                {"error": f"Colorization failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def match_criminals(self, request, pk=None):
        """Match the colorized face against the criminal database"""
        composition = self.get_object()

        if not composition.final_image:
            return Response(
                {"error": "No colorized image. Colorize the sketch first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            colorized_path = os.path.join(
                settings.MEDIA_ROOT, str(composition.final_image)
            )

            if not os.path.exists(colorized_path):
                return Response(
                    {"error": "Colorized image file not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            criminal_db_path = os.path.join(settings.BASE_DIR, "criminalDB")

            if not os.path.isdir(criminal_db_path):
                return Response(
                    {"error": "Criminal database folder not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            print(f"[Django] Running face matching against criminal DB...")
            matches = match_face(
                query_image_path=colorized_path,
                criminal_db_path=criminal_db_path,
                top_k=10,
            )

            # Add image URLs for frontend display
            for m in matches:
                m["image_url"] = f"/criminalDB/{m['filename']}"

            return Response(
                {
                    "status": "matching complete",
                    "matches": matches,
                }
            )

        except Exception as e:
            import traceback

            print(f"[Django] Matching error: {traceback.format_exc()}")
            return Response(
                {"error": f"Matching failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        """Get all versions for a composition"""
        composition = self.get_object()
        versions = composition.versions.all()
        return Response(GenerationVersionSerializer(versions, many=True).data)

    @action(detail=False, methods=["get"])
    def all_history(self, request):
        """Get ALL compositions with their versions, for the persistent sidebar"""
        compositions = FaceComposition.objects.prefetch_related("versions").all()
        data = []
        for comp in compositions:
            versions = comp.versions.all()
            if not versions.exists():
                continue  # skip compositions with no generated versions
            data.append(
                {
                    "id": comp.id,
                    "created_at": comp.created_at.isoformat(),
                    "versions": GenerationVersionSerializer(versions, many=True).data,
                }
            )
        return Response(data)

    @action(detail=True, methods=["post"], url_path="restore/(?P<version_id>[0-9]+)")
    def restore_version(self, request, pk=None, version_id=None):
        """Restore a previous version as the current active image"""
        composition = self.get_object()

        try:
            version = GenerationVersion.objects.get(
                id=version_id, composition=composition
            )
        except GenerationVersion.DoesNotExist:
            return Response(
                {"error": "Version not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Set as current image based on type
        if version.image_type == "colorized":
            composition.final_image = version.image.name
        else:
            composition.sketch_image = version.image.name
        composition.save()

        return Response(
            {
                "status": "version restored",
                "image_url": version.image.url,
                "image_type": version.image_type,
                "version": GenerationVersionSerializer(version).data,
            }
        )


def index(request):
    """Main page view"""
    return render(request, "index.html")
