from django.contrib import admin
from .models import FaceFeatureCategory, FaceFeature, FaceComposition

@admin.register(FaceFeatureCategory)
class FaceFeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'description']
    list_editable = ['order']
    ordering = ['order']

@admin.register(FaceFeature)
class FaceFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'image']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['name', 'description', 'prompt_text']
    ordering = ['category__order', 'order']

@admin.register(FaceComposition)
class FaceCompositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'composite_image', 'sketch_image']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    filter_horizontal = ['selected_features']
