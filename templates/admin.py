from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TemplateCategory, FlyerTemplate, TemplateDynamicArea,
    TemplateRating, TemplateUsageLog
)


@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_box', 'is_active',
                    'sort_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')

    def color_box(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_box.short_description = 'Color'


class TemplateDynamicAreaInline(admin.TabularInline):
    model = TemplateDynamicArea
    extra = 1
    ordering = ('sort_order',)


@admin.register(FlyerTemplate)
class FlyerTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'template_type', 'category',
                    'is_public', 'is_featured', 'usage_count', 'created_at')
    list_filter = ('template_type', 'is_public', 'is_featured',
                   'is_active', 'created_at', 'category')
    search_fields = ('name', 'description', 'owner__email',
                     'owner__first_name', 'owner__last_name')
    readonly_fields = ('usage_count', 'width', 'height',
                       'created_at', 'updated_at')
    inlines = [TemplateDynamicAreaInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'category')


@admin.register(TemplateDynamicArea)
class TemplateDynamicAreaAdmin(admin.ModelAdmin):
    list_display = ('template', 'label', 'area_type', 'x_position',
                    'y_position', 'width', 'height', 'sort_order')
    list_filter = ('area_type', 'is_required')
    search_fields = ('template__name', 'label')
    ordering = ('template', 'sort_order')


@admin.register(TemplateRating)
class TemplateRatingAdmin(admin.ModelAdmin):
    list_display = ('template', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('template__name', 'user__email', 'review')
    readonly_fields = ('created_at',)


@admin.register(TemplateUsageLog)
class TemplateUsageLogAdmin(admin.ModelAdmin):
    list_display = ('template', 'user', 'event_type', 'generated_at')
    list_filter = ('event_type', 'generated_at')
    search_fields = ('template__name', 'user__email')
    readonly_fields = ('generated_at',)
    date_hierarchy = 'generated_at'
