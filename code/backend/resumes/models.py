"""
Resume models for storing user resumes.
"""

from django.db import models
from django.conf import settings
import secrets
import uuid

class Resume(models.Model):
    """简历模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('generated', '已生成'),
        ('failed', '生成失败'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='resumes',
        verbose_name='用户'
    )
    template = models.ForeignKey(
        'templates.ResumeTemplate',
        on_delete=models.SET_NULL,
        null=True,
        related_name='resumes',
        verbose_name='模板'
    )
    title = models.CharField(max_length=200, verbose_name='简历标题')
    resume_data = models.JSONField(default=dict, verbose_name='简历数据')
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, verbose_name='PDF文件')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    share_token = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        default=uuid.uuid4  # 👈 核心修改：让它自动生成不重复的随机码
    )
    share_count = models.IntegerField(default=0, verbose_name='分享次数')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'resumes_resume'
        verbose_name = '简历'
        verbose_name_plural = '简历'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def generate_share_token(self):
        """生成分享令牌"""
        if not self.share_token:
            self.share_token = secrets.token_urlsafe(32)
            self.save()
        return self.share_token
