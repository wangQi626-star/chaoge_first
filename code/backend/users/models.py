"""
User models for authentication and profile management.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """扩展Django内置User模型"""
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users_customuser'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """用户profile，区分管理员和普通用户"""
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('user', '普通用户'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    bio = models.TextField(blank=True, verbose_name='个人简介')

    class Meta:
        db_table = 'users_userprofile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def is_admin(self):
        return self.role == 'admin'
