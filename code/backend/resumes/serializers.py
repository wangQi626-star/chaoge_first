"""
Resume serializers for API serialization.
"""

from rest_framework import serializers
from .models import Resume
from templates.serializers import ResumeTemplateSerializer


class ResumeSerializer(serializers.ModelSerializer):
    """简历序列化器"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_detail = ResumeTemplateSerializer(source='template', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Resume
        fields = ['id', 'title', 'template', 'template_detail', 'template_name', 'user', 'username', 
                  'resume_data', 'pdf_file', 'status', 'error_message', 
                  'created_at', 'updated_at']
        read_only_fields = [
            'id',
            'template_detail',
            'template_name',
            'user',
            'username',
            'pdf_file',
            'status',
            'error_message',
            'created_at',
            'updated_at',
        ]


class ResumeListSerializer(serializers.ModelSerializer):
    """简历列表序列化器"""
    template_name = serializers.CharField(source='template.name', read_only=True)

    class Meta:
        model = Resume
        fields = ['id', 'title', 'template', 'template_name', 'status', 'created_at', 'updated_at']
