from django.db import models


class ShowcaseApp(models.Model):
    """Optional model to manage featured or upcoming apps from Django admin."""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, help_text="External URL (e.g. https://simpleplanner.blottogbar.no)")
    ascii_icon = models.TextField(blank=True, help_text="Monospace ASCII icon / badge")
    status = models.CharField(
        max_length=20,
        choices=[
            ('live', 'Live in Production'),
            ('beta', 'In Beta'),
            ('upcoming', 'Coming Soon'),
            ('concept', 'Concept'),
        ],
        default='live'
    )
    badge_label = models.CharField(max_length=50, blank=True, default='Live')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Showcase App'
        verbose_name_plural = 'Showcase Apps'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
