"""
Django Admin configuration for resumes app.
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """简历 Admin"""

    list_display = [
        'title',
        'user',
        'candidate_name',
        'candidate_position',
        'template',
        'status',
        'pdf_entry',
        'created_at',
    ]
    list_filter = ['status', 'created_at', 'template', 'user']
    search_fields = ['title', 'user__username', 'user__email']
    raw_id_fields = ['user', 'template']
    readonly_fields = [
        'title',
        'user',
        'template',
        'status',
        'error_message',
        'pdf_entry',
        'personal_overview',
        'education_preview',
        'experience_preview',
        'projects_preview',
        'skills_preview',
        'summary_preview',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('基础信息', {
            'fields': ('title', 'user', 'template', 'status', 'pdf_entry', 'error_message')
        }),
        ('个人信息', {
            'fields': ('personal_overview', 'summary_preview')
        }),
        ('教育经历', {
            'fields': ('education_preview',)
        }),
        ('工作经历', {
            'fields': ('experience_preview',)
        }),
        ('项目经历', {
            'fields': ('projects_preview',)
        }),
        ('技能证书', {
            'fields': ('skills_preview',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'template')

    @admin.display(description='姓名')
    def candidate_name(self, obj):
        return (obj.resume_data or {}).get('personal', {}).get('name', '') or '-'

    @admin.display(description='应聘职位')
    def candidate_position(self, obj):
        return (obj.resume_data or {}).get('personal', {}).get('position', '') or '-'

    @admin.display(description='PDF')
    def pdf_entry(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">查看 PDF</a>', obj.pdf_file.url)
        return '未生成'

    @admin.display(description='个人信息')
    def personal_overview(self, obj):
        personal = (obj.resume_data or {}).get('personal', {}) or {}
        user_url = reverse('admin:users_customuser_change', args=[obj.user_id])
        rows = [
            ('姓名', personal.get('name', '') or '-'),
            ('邮箱', personal.get('email', '') or '-'),
            ('手机', personal.get('phone', '') or '-'),
            ('应聘职位', personal.get('position', '') or '-'),
        ]
        content = format_html_join(
            '',
            '<div style="margin-bottom:8px;"><strong style="display:inline-block;min-width:88px;">{}：</strong>{}</div>',
            rows,
        )
        return format_html(
            '<div>{}</div><div style="margin-top:12px;"><a href="{}">查看用户信息</a></div>',
            content,
            user_url,
        )

    @admin.display(description='教育经历')
    def education_preview(self, obj):
        return self._render_entries(
            (obj.resume_data or {}).get('education', []),
            [
                ('school', '学校'),
                ('degree', '学历'),
                ('major', '专业'),
                ('period', '时间'),
            ],
            empty_text='暂无教育经历',
        )

    @admin.display(description='工作经历')
    def experience_preview(self, obj):
        return self._render_entries(
            (obj.resume_data or {}).get('experience', []),
            [
                ('company', '公司'),
                ('position', '职位'),
                ('period', '时间'),
                ('description', '描述'),
            ],
            empty_text='暂无工作经历',
        )

    @admin.display(description='项目经历')
    def projects_preview(self, obj):
        return self._render_entries(
            (obj.resume_data or {}).get('projects', []),
            [
                ('name', '项目'),
                ('role', '角色'),
                ('period', '时间'),
                ('description', '描述'),
            ],
            empty_text='暂无项目经历',
        )

    @admin.display(description='技能证书')
    def skills_preview(self, obj):
        skills = (obj.resume_data or {}).get('skills', []) or []
        if not skills:
            return '暂无技能证书'
        return format_html_join(
            '',
            '<span style="display:inline-block;margin:0 8px 8px 0;padding:4px 10px;border-radius:999px;background:#eef5ff;color:#2563eb;">{}</span>',
            ((skill,) for skill in skills if skill),
        )

    @admin.display(description='个人简介')
    def summary_preview(self, obj):
        summary = (obj.resume_data or {}).get('personal', {}).get('summary', '') or ''
        if not summary:
            return '暂无个人简介'
        return format_html('<div style="max-width:860px;line-height:1.8;white-space:pre-wrap;">{}</div>', summary)

    def _render_entries(self, entries, fields, empty_text):
        if not entries:
            return empty_text

        blocks = []
        for index, entry in enumerate(entries, start=1):
            lines = []
            for key, label in fields:
                value = (entry or {}).get(key, '')
                if value:
                    lines.append(
                        format_html(
                            '<div style="margin-bottom:6px;"><strong style="display:inline-block;min-width:72px;">{}：</strong>{}</div>',
                            label,
                            value,
                        )
                    )
            block = format_html(
                '<div style="padding:12px 14px;margin-bottom:12px;border:1px solid #e5e7eb;border-radius:12px;background:#fff;">'
                '<div style="margin-bottom:8px;font-weight:700;color:#111827;">第 {} 条</div>{}</div>',
                index,
                format_html_join('', '{}', ((line,) for line in lines)) if lines else '暂无内容',
            )
            blocks.append(block)

        return format_html_join('', '{}', ((block,) for block in blocks))
