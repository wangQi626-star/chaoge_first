"""
Template models for resume templates.
"""

from django.db import models


class ResumeTemplate(models.Model):
    """简历模板模型"""
    CATEGORY_CHOICES = [
        ('classic', '经典'),
        ('modern', '现代'),
        ('creative', '创意'),
        ('simple', '简约'),
        ('colorful', '多彩'),
    ]

    name = models.CharField(max_length=100, verbose_name='模板名称')
    description = models.TextField(blank=True, verbose_name='模板描述')
    thumbnail = models.ImageField(upload_to='templates/thumbnails/', blank=True, verbose_name='缩略图')
    html_content = models.TextField(verbose_name='HTML模板内容')
    css_content = models.TextField(blank=True, verbose_name='CSS样式')
    color_scheme = models.JSONField(default=dict, verbose_name='配色方案')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='classic', verbose_name='分类')
    is_custom = models.BooleanField(default=False, verbose_name='是否自定义')
    creator = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建者')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    usage_count = models.IntegerField(default=0, verbose_name='使用次数')

    class Meta:
        db_table = 'templates_template'
        verbose_name = '简历模板'
        verbose_name_plural = '简历模板'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
