from django.contrib import admin
from .models import ShowcaseApp


@admin.register(ShowcaseApp)
class ShowcaseAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'badge_label', 'url', 'order')
    list_editable = ('status', 'badge_label', 'order')
    prepopulated_fields = {'slug': ('title',)}
