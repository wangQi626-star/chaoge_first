"""
Django Admin configuration for templates app.
"""

from django.contrib import admin
from .models import ResumeTemplate


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    """简历模板Admin"""
    list_display = ['name', 'is_active', 'usage_count', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']


admin.site.unregister(ResumeTemplate)
