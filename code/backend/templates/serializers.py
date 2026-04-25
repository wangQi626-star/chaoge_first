"""
Template serializers for API serialization.
"""

from rest_framework import serializers
from .models import ResumeTemplate


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """简历模板序列化器"""

    class Meta:
        model = ResumeTemplate
        fields = ['id', 'name', 'description', 'thumbnail', 'html_content', 'css_content', 
                  'is_active', 'usage_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'usage_count', 'created_at', 'updated_at']


class ResumeTemplateListSerializer(serializers.ModelSerializer):
    """简历模板列表序列化器（不包含HTML内容）"""

    class Meta:
        model = ResumeTemplate
        fields = ['id', 'name', 'description', 'thumbnail', 'html_content', 'is_active', 'usage_count', 'created_at']
