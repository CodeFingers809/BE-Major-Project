from django.db import models


class FaceFeatureCategory(models.Model):
    """Categories for facial features"""

    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Face Feature Categories"

    def __str__(self):
        return self.name


class FaceFeature(models.Model):
    """Individual facial features with image references"""

    category = models.ForeignKey(
        FaceFeatureCategory, on_delete=models.CASCADE, related_name="features"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="feature_images/", null=True, blank=True)
    prompt_text = models.TextField(help_text="Text to include in AI generation prompt")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["category__order", "order"]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class FaceComposition(models.Model):
    """Stores a complete face composition from user selections"""

    created_at = models.DateTimeField(auto_now_add=True)
    selected_features = models.ManyToManyField(FaceFeature)
    composite_image = models.ImageField(upload_to="composites/", null=True, blank=True)
    sketch_image = models.ImageField(upload_to="sketches/", null=True, blank=True)
    final_image = models.ImageField(upload_to="final/", null=True, blank=True)
    additional_notes = models.TextField(blank=True)
    user_prompt = models.TextField(
        blank=True,
        help_text="Free-form user description (extra details not covered by selectors)",
    )
    reference_image = models.ImageField(
        upload_to="references/",
        null=True,
        blank=True,
        help_text="Optional reference image (CCTV capture, blurry photo, etc.)",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Composition {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def get_prompt(self):
        """Generate AI prompt from selected features"""
        features_text = ", ".join([f.prompt_text for f in self.selected_features.all()])
        return features_text


class GenerationVersion(models.Model):
    """Tracks each version of a generated image (sketch, revision, colorized)"""

    IMAGE_TYPES = [
        ("sketch", "Initial Sketch"),
        ("revision", "Revision"),
        ("colorized", "Colorized"),
    ]

    composition = models.ForeignKey(
        FaceComposition, on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.IntegerField(default=1)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)
    image = models.ImageField(upload_to="versions/")
    prompt_used = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_version = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        ordering = ["version_number"]

    def __str__(self):
        return f"v{self.version_number} ({self.image_type}) — Composition {self.composition_id}"
