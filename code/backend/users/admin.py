"""
Django Admin configuration for users app.
"""

import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .models import CustomUser, UserProfile

admin.site.site_header = '简历管理后台'
admin.site.site_title = '简历管理后台'
admin.site.index_title = '控制台'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    extra = 0
    can_delete = False
    verbose_name = '用户资料'
    verbose_name_plural = '用户资料'
    fields = ('role', 'bio')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """自定义用户 Admin"""

    change_list_template = 'admin/users/customuser/change_list.html'
    list_display = [
        'username',
        'email',
        'phone',
        'role_display',
        'resume_count',
        'quick_edit_button',
        'resume_entry',
        'is_active',
        'created_at',
    ]
    list_filter = ['is_staff', 'is_active', 'created_at', 'profile__role']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-created_at']
    actions = None
    inlines = [UserProfileInline]
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined', 'resume_entry']

    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('phone', 'avatar')}),
        ('管理信息', {'fields': ('resume_entry', 'created_at', 'updated_at')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('email', 'phone')}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/quick-edit/',
                self.admin_site.admin_view(self.quick_edit_view),
                name='users_customuser_quick_edit',
            ),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('profile').annotate(admin_resume_count=Count('resumes'))

    @admin.display(description='角色')
    def role_display(self, obj):
        return getattr(getattr(obj, 'profile', None), 'get_role_display', lambda: '未设置')()

    @admin.display(description='简历数', ordering='admin_resume_count')
    def resume_count(self, obj):
        return getattr(obj, 'admin_resume_count', 0)

    @admin.display(description='编辑')
    def quick_edit_button(self, obj):
        if not obj.pk:
            return '-'
        url = reverse('admin:users_customuser_quick_edit', args=[obj.pk])
        return format_html(
            '<button type="button" class="button quick-edit-trigger" data-url="{}">编辑信息</button>',
            url,
        )

    @admin.display(description='查看简历')
    def resume_entry(self, obj):
        if not obj.pk:
            return '保存后可查看'
        url = reverse('admin:resumes_resume_changelist') + f'?user__id__exact={obj.pk}'
        count = getattr(obj, 'admin_resume_count', obj.resumes.count())
        return format_html('<a href="{}">查看该用户的简历（{}）</a>', url, count)

    def quick_edit_view(self, request, user_id):
        user = CustomUser.objects.select_related('profile').filter(pk=user_id).first()
        if not user:
            return JsonResponse({'error': '用户不存在'}, status=404)

        profile, _ = UserProfile.objects.get_or_create(user=user)

        if request.method == 'GET':
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'is_active': user.is_active,
                'role': profile.role,
                'bio': profile.bio,
                'role_choices': [{'value': value, 'label': label} for value, label in UserProfile.ROLE_CHOICES],
            })

        if request.method != 'POST':
            return JsonResponse({'error': '请求方式不支持'}, status=405)

        try:
            payload = json.loads(request.body.decode('utf-8'))
        except (TypeError, ValueError, json.JSONDecodeError):
            return JsonResponse({'error': '提交数据格式不正确'}, status=400)

        username = (payload.get('username') or '').strip()
        email = (payload.get('email') or '').strip()
        phone = (payload.get('phone') or '').strip()
        bio = (payload.get('bio') or '').strip()
        role = (payload.get('role') or '').strip()
        is_active = bool(payload.get('is_active'))

        if not username:
            return JsonResponse({'error': '用户名不能为空'}, status=400)
        if CustomUser.objects.exclude(pk=user.pk).filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)
        if role not in dict(UserProfile.ROLE_CHOICES):
            return JsonResponse({'error': '角色不合法'}, status=400)

        user.username = username
        user.email = email
        user.phone = phone
        user.is_active = is_active
        user.save(update_fields=['username', 'email', 'phone', 'is_active'])

        profile.role = role
        profile.bio = bio
        profile.save(update_fields=['role', 'bio'])

        return JsonResponse({
            'message': '用户信息已更新',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'is_active': user.is_active,
                'role': profile.role,
                'role_label': profile.get_role_display(),
                'bio': profile.bio,
            },
        })


admin.site.unregister(Group)
