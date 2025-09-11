from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
import json

User = get_user_model()


class TemplateCategory(models.Model):
    """
    Categories for organizing flyer templates
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True,
                            help_text="Font Awesome icon class")
    color = models.CharField(
        max_length=7, default='#3498db', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'template_categories'
        verbose_name = _('Template Category')
        verbose_name_plural = _('Template Categories')
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class FlyerTemplate(models.Model):
    """
    PNG templates uploaded by users for flyer generation
    """
    TEMPLATE_TYPES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('promotion', 'Promotion'),
        ('general', 'General Event'),
        ('holiday', 'Holiday'),
        ('custom', 'Custom'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='templates')
    category = models.ForeignKey(
        TemplateCategory, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template_type = models.CharField(
        max_length=20, choices=TEMPLATE_TYPES, default='general')

    # Template file
    image_file = models.ImageField(
        upload_to='templates/',
        validators=[FileExtensionValidator(
            allowed_extensions=['png', 'jpg', 'jpeg'])],
        help_text="Upload PNG, JPG, or JPEG files only"
    )

    # Template dimensions
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    # Dynamic areas configuration
    dynamic_areas = models.JSONField(
        default=dict,
        help_text="JSON configuration for dynamic areas (photo, name, message, etc.)"
    )

    # Template metadata
    is_public = models.BooleanField(
        default=False, help_text="Allow other users to use this template")
    is_featured = models.BooleanField(default=False)
    usage_count = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(default=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flyer_templates'
        verbose_name = _('Flyer Template')
        verbose_name_plural = _('Flyer Templates')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.template_type})"

    def get_dynamic_areas(self):
        """Return parsed dynamic areas configuration"""
        try:
            return json.loads(self.dynamic_areas) if isinstance(self.dynamic_areas, str) else self.dynamic_areas
        except (json.JSONDecodeError, TypeError):
            return {}

    def increment_usage(self):
        """Increment the usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class TemplateDynamicArea(models.Model):
    """
    Individual dynamic areas within a template (photo, name, text, etc.)
    """
    AREA_TYPES = [
        ('photo', 'Photo'),
        ('name', 'Name/Title'),
        ('message', 'Message'),
        ('date', 'Date'),
        ('custom_text', 'Custom Text'),
    ]

    FONT_FAMILIES = [
        ('Arial', 'Arial'),
        ('Helvetica', 'Helvetica'),
        ('Times New Roman', 'Times New Roman'),
        ('Georgia', 'Georgia'),
        ('Verdana', 'Verdana'),
        ('Trebuchet MS', 'Trebuchet MS'),
        ('Impact', 'Impact'),
        ('Comic Sans MS', 'Comic Sans MS'),
    ]

    template = models.ForeignKey(
        FlyerTemplate, on_delete=models.CASCADE, related_name='areas')
    area_type = models.CharField(max_length=20, choices=AREA_TYPES)
    label = models.CharField(
        max_length=100, help_text="Display label for this area")

    # Position and size
    x_position = models.PositiveIntegerField(
        help_text="X coordinate from top-left")
    y_position = models.PositiveIntegerField(
        help_text="Y coordinate from top-left")
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    # Text styling (for text areas)
    font_family = models.CharField(
        max_length=50, choices=FONT_FAMILIES, default='Arial')
    font_size = models.PositiveIntegerField(default=24)
    font_color = models.CharField(
        max_length=7, default='#000000', help_text="Hex color code")
    font_weight = models.CharField(max_length=10, default='normal', choices=[
        ('normal', 'Normal'),
        ('bold', 'Bold'),
    ])
    text_align = models.CharField(max_length=10, default='center', choices=[
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ])

    # Photo styling (for photo areas)
    border_radius = models.PositiveIntegerField(
        default=0, help_text="Border radius in pixels")
    border_width = models.PositiveIntegerField(
        default=0, help_text="Border width in pixels")
    border_color = models.CharField(
        max_length=7, default='#000000', help_text="Border color")

    # Validation
    is_required = models.BooleanField(default=True)
    max_length = models.PositiveIntegerField(
        null=True, blank=True, help_text="Max characters for text areas")

    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'template_dynamic_areas'
        verbose_name = _('Template Dynamic Area')
        verbose_name_plural = _('Template Dynamic Areas')
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.template.name} - {self.label} ({self.area_type})"


class TemplateRating(models.Model):
    """
    User ratings for public templates
    """
    template = models.ForeignKey(
        FlyerTemplate, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'template_ratings'
        verbose_name = _('Template Rating')
        verbose_name_plural = _('Template Ratings')
        unique_together = ['template', 'user']

    def __str__(self):
        return f"{self.template.name} - {self.rating} stars by {self.user.get_full_name()}"


class TemplateUsageLog(models.Model):
    """
    Log of template usage for analytics
    """
    template = models.ForeignKey(
        FlyerTemplate, on_delete=models.CASCADE, related_name='usage_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)  # birthday, anniversary, etc.
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'template_usage_logs'
        verbose_name = _('Template Usage Log')
        verbose_name_plural = _('Template Usage Logs')
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.template.name} used by {self.user.get_full_name()}"
