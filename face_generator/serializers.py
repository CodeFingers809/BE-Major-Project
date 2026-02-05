from rest_framework import serializers
from .models import FaceFeatureCategory, FaceFeature, FaceComposition

class FaceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceFeature
        fields = ['id', 'name', 'description', 'image', 'prompt_text', 'order']

class FaceFeatureCategorySerializer(serializers.ModelSerializer):
    features = FaceFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = FaceFeatureCategory
        fields = ['id', 'name', 'description', 'order', 'features']

class FaceCompositionSerializer(serializers.ModelSerializer):
    selected_features = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FaceFeature.objects.all()
    )
    prompt = serializers.SerializerMethodField()

    class Meta:
        model = FaceComposition
        fields = ['id', 'created_at', 'selected_features', 'composite_image',
                  'sketch_image', 'final_image', 'additional_notes', 'prompt']

    def get_prompt(self, obj):
        return obj.get_prompt()
