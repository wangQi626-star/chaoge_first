"""
Resume views for API endpoints.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
import os
import re
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from html import escape

from .models import Resume
from .serializers import ResumeSerializer, ResumeListSerializer
from .career_advice import CareerAdviceError, CareerAdviceService
from templates.models import ResumeTemplate


class ResumeViewSet(viewsets.ModelViewSet):
    """简历CRUD API"""
    permission_classes = [permissions.IsAuthenticated]
    PDF_FONT_NAME = 'STSong-Light'
    career_advice_service = CareerAdviceService()

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ResumeListSerializer
        return ResumeSerializer

    def perform_create(self, serializer):
        # 1. 保存简历
        resume = serializer.save(user=self.request.user)

        # 2. 核心联动：如果这份简历用了某个模板，模板的总使用次数就 +1
        if resume.template:
            resume.template.usage_count += 1
            resume.template.save(update_fields=['usage_count'])

    @action(detail=True, methods=['post'])
    def career_advice(self, request, pk=None):
        resume = self.get_object()

        try:
            advice = self.career_advice_service.analyze(resume)
            return Response(advice)
        except CareerAdviceError as exc:
            message = str(exc)
            error_status = status.HTTP_503_SERVICE_UNAVAILABLE if 'DEEPSEEK_API_KEY' in message else status.HTTP_502_BAD_GATEWAY
            return Response({'error': message}, status=error_status)

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """生成PDF"""
        resume = self.get_object()
        template = resume.template

        if not template:
            resume.status = 'failed'
            resume.error_message = '请选择模板'
            resume.save()
            return Response({'error': '请选择模板'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resume_data = resume.resume_data

            self._ensure_pdf_font()
            rendered_html = self._prepare_pdf_html(
                self._render_pdf_template(template, resume_data)
            )

            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(
                src=rendered_html,
                dest=pdf_buffer,
                encoding='utf-8'
            )

            if pisa_status.err:
                raise Exception('PDF生成失败')

            filename = f"resume_{resume.user.id}_{resume.id}.pdf"
            filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)

            with open(filepath, 'wb') as f:
                f.write(pdf_buffer.getvalue())

            resume.pdf_file = f'pdfs/{filename}'
            resume.status = 'generated'
            resume.save()

            template.usage_count += 1
            template.save()

            return Response({
                'message': 'PDF生成成功',
                'pdf_url': resume.pdf_file.url
            })

        except Exception as e:
            resume.status = 'failed'
            resume.error_message = str(e)
            resume.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _ensure_pdf_font(self):
        if self.PDF_FONT_NAME in pdfmetrics.getRegisteredFontNames():
            return
        pdfmetrics.registerFont(UnicodeCIDFont(self.PDF_FONT_NAME))

    def _prepare_pdf_html(self, html):
        pdf_style = f'''
        <meta charset="utf-8">
        <style>
            html, body, table, tr, td, div, p, span, h1, h2, h3, h4, h5, h6, li {{
                font-family: "{self.PDF_FONT_NAME}" !important;
            }}
        </style>
        '''

        if '<head>' in html:
            return html.replace('<head>', f'<head>{pdf_style}', 1)
        if '<html' in html:
            return re.sub(r'(<html[^>]*>)', r'\1<head>' + pdf_style + '</head>', html, count=1)
        return f'<html><head>{pdf_style}</head><body>{html}</body></html>'

    def _render_pdf_template(self, template, resume_data):
        theme = self._get_pdf_theme(template)
        personal = resume_data.get('personal', {})
        sections = ''.join([
            self._render_pdf_section('教育经历', self._render_pdf_education(resume_data.get('education', [])), theme),
            self._render_pdf_section('工作经历', self._render_pdf_experience(resume_data.get('experience', [])), theme),
            self._render_pdf_section('项目经历', self._render_pdf_projects(resume_data.get('projects', [])), theme),
            self._render_pdf_section('技能证书', self._render_pdf_skills(resume_data.get('skills', [])), theme),
            self._render_pdf_section('个人简介', self._render_pdf_summary(personal.get('summary', '')), theme),
        ])

        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: "{self.PDF_FONT_NAME}";
                    margin: 0;
                    padding: 22px;
                    background: {theme["page_bg"]};
                    color: {theme["text"]};
                    font-size: 12px;
                    line-height: 1.6;
                }}
                .resume-shell {{
                    background: #ffffff;
                    border: 1px solid {theme["border"]};
                    padding: 0;
                }}
                .resume-top {{
                    background: {theme["header_bg"]};
                    color: {theme["header_text"]};
                    padding: 24px 28px 20px;
                }}
                .resume-kicker {{
                    font-size: 10px;
                    letter-spacing: 3px;
                    color: {theme["kicker"]};
                    margin-bottom: 10px;
                }}
                .resume-name {{
                    font-size: 28px;
                    font-weight: bold;
                    margin: 0 0 14px 0;
                }}
                .personal-table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .personal-meta {{
                    vertical-align: top;
                    padding-right: 16px;
                }}
                .personal-photo-wrap {{
                    width: 112px;
                    vertical-align: top;
                    text-align: right;
                }}
                .personal-photo {{
                    width: 88px;
                    height: 112px;
                    border: 3px solid {theme["photo_border"]};
                }}
                .personal-row {{
                    margin-bottom: 8px;
                    color: {theme["header_text"]};
                }}
                .personal-label {{
                    color: {theme["label"]};
                    font-weight: bold;
                }}
                .resume-body {{
                    padding: 20px 28px 24px;
                }}
                .section {{
                    margin-bottom: 18px;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: bold;
                    color: {theme["section_title"]};
                    border-left: 5px solid {theme["accent"]};
                    border-bottom: 1px solid {theme["border"]};
                    padding: 0 0 6px 10px;
                    margin: 0 0 12px 0;
                }}
                .entry {{
                    border: 1px solid {theme["card_border"]};
                    padding: 10px 12px;
                    margin-bottom: 10px;
                }}
                .entry-table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .entry-title {{
                    font-size: 13px;
                    font-weight: bold;
                    color: {theme["title"]};
                }}
                .entry-date {{
                    font-size: 11px;
                    color: {theme["muted"]};
                    text-align: right;
                }}
                .entry-subtitle {{
                    color: {theme["subtitle"]};
                    margin-top: 4px;
                }}
                .entry-content {{
                    color: {theme["text"]};
                    margin-top: 6px;
                }}
                .skills-box {{
                    border: 1px solid {theme["card_border"]};
                    padding: 10px 12px;
                    color: {theme["text"]};
                }}
                .summary-box {{
                    border: 1px solid {theme["card_border"]};
                    padding: 10px 12px;
                    color: {theme["text"]};
                }}
            </style>
        </head>
        <body>
            <div class="resume-shell">
                <div class="resume-top">
                    <div class="resume-kicker">{theme["kicker_text"]}</div>
                    <div class="resume-name">{escape(personal.get("name", ""))}</div>
                    {self._render_pdf_personal_info(personal)}
                </div>
                <div class="resume-body">
                    {sections}
                </div>
            </div>
        </body>
        </html>
        '''

    def _get_pdf_theme(self, template):
        name = (template.name or '').lower()
        if '创意' in name:
            return {
                'page_bg': '#fff7ef',
                'header_bg': '#a33c5d',
                'header_text': '#fff7ef',
                'kicker': '#ffd8b0',
                'kicker_text': 'PORTFOLIO STYLE',
                'label': '#ffd8b0',
                'accent': '#f3a65a',
                'border': '#f0d7c0',
                'card_border': '#f3d7c6',
                'photo_border': '#ffd8b0',
                'section_title': '#a33c5d',
                'title': '#7c2744',
                'subtitle': '#90546c',
                'text': '#5b4450',
                'muted': '#d18652',
            }
        if '专业' in name:
            return {
                'page_bg': '#eef3f8',
                'header_bg': '#15324c',
                'header_text': '#ffffff',
                'kicker': '#9dc0e5',
                'kicker_text': 'PROFESSIONAL PROFILE',
                'label': '#c8dcf1',
                'accent': '#15324c',
                'border': '#c7d7ea',
                'card_border': '#d9e4f2',
                'photo_border': '#d8e6f5',
                'section_title': '#15324c',
                'title': '#15324c',
                'subtitle': '#47607a',
                'text': '#33485c',
                'muted': '#6c84a0',
            }
        return {
            'page_bg': '#f4efe6',
            'header_bg': '#fffdfa',
            'header_text': '#2d241d',
            'kicker': '#8b5e3c',
            'kicker_text': 'CURATED RESUME',
            'label': '#8b5e3c',
            'accent': '#8b5e3c',
            'border': '#d8c8b8',
            'card_border': '#e5d8cb',
            'photo_border': '#d8c8b8',
            'section_title': '#5e4028',
            'title': '#2d241d',
            'subtitle': '#6b5747',
            'text': '#4f4237',
            'muted': '#8a7666',
        }

    def _render_pdf_personal_info(self, personal):
        photo = personal.get('photo', '')
        photo_html = ''
        if photo:
            photo_html = f'''
            <td class="personal-photo-wrap">
                <img src="{photo}" alt="photo" class="personal-photo" />
            </td>
            '''

        rows = ''.join([
            self._render_pdf_personal_row('姓名', personal.get('name', '')),
            self._render_pdf_personal_row('邮箱', personal.get('email', '')),
            self._render_pdf_personal_row('手机', personal.get('phone', '')),
            self._render_pdf_personal_row('应聘职位', personal.get('position', '')),
        ])

        return f'''
        <table class="personal-table">
            <tr>
                <td class="personal-meta">
                    {rows}
                </td>
                {photo_html}
            </tr>
        </table>
        '''

    def _render_pdf_personal_row(self, label, value):
        return f'<div class="personal-row"><span class="personal-label">{escape(label)}：</span>{escape(value or "")}</div>'

    def _render_pdf_section(self, title, content, theme):
        if not content:
            return ''
        return f'''
        <div class="section">
            <div class="section-title">{escape(title)}</div>
            {content}
        </div>
        '''

    def _render_pdf_education(self, items):
        if not items:
            return ''
        return ''.join([
            self._render_pdf_entry(item.get('school', ''), item.get('period', ''), f'{item.get("degree", "")} - {item.get("major", "")}', '')
            for item in items
        ])

    def _render_pdf_experience(self, items):
        if not items:
            return ''
        return ''.join([
            self._render_pdf_entry(item.get('company', ''), item.get('period', ''), item.get('position', ''), item.get('description', ''))
            for item in items
        ])

    def _render_pdf_projects(self, items):
        if not items:
            return ''
        return ''.join([
            self._render_pdf_entry(item.get('name', ''), item.get('period', ''), item.get('role', ''), item.get('description', ''))
            for item in items
        ])

    def _render_pdf_skills(self, items):
        if not items:
            return ''
        return f'<div class="skills-box">{escape(", ".join(items))}</div>'

    def _render_pdf_summary(self, summary):
        if not summary:
            return ''
        return f'<div class="summary-box">{escape(summary)}</div>'

    def _render_pdf_entry(self, title, period, subtitle, content):
        subtitle_html = f'<div class="entry-subtitle">{escape(subtitle)}</div>' if subtitle else ''
        content_html = f'<div class="entry-content">{escape(content)}</div>' if content else ''
        return f'''
        <div class="entry">
            <table class="entry-table">
                <tr>
                    <td class="entry-title">{escape(title)}</td>
                    <td class="entry-date">{escape(period)}</td>
                </tr>
            </table>
            {subtitle_html}
            {content_html}
        </div>
        '''

    def _render_template(self, html_content, resume_data):
        """渲染HTML模板"""
        html = self._normalize_template(html_content)

        personal = resume_data.get('personal', {})
        education = resume_data.get('education', [])
        experience = resume_data.get('experience', [])
        projects = resume_data.get('projects', [])
        skills = resume_data.get('skills', [])

        replacements = {
            '{{name}}': personal.get('name', ''),
            '{{email}}': personal.get('email', ''),
            '{{phone}}': personal.get('phone', ''),
            '{{position}}': personal.get('position', ''),
            '{{summary}}': personal.get('summary', ''),
            '{{personal_info_html}}': self._render_personal_info(personal),
            '{{education_html}}': self._render_education(education),
            '{{experience_html}}': self._render_experience(experience),
            '{{projects_html}}': self._render_projects(projects),
            '{{skills_html}}': self._render_skills(skills),
            '{{summary_html}}': self._render_summary(personal.get('summary', '')),
        }

        conditional_values = {
            'name': personal.get('name', ''),
            'email': personal.get('email', ''),
            'phone': personal.get('phone', ''),
            'position': personal.get('position', ''),
            'summary': personal.get('summary', ''),
            'personal_info_html': replacements['{{personal_info_html}}'],
            'education_html': replacements['{{education_html}}'],
            'experience_html': replacements['{{experience_html}}'],
            'projects_html': replacements['{{projects_html}}'],
            'skills_html': replacements['{{skills_html}}'],
            'summary_html': replacements['{{summary_html}}'],
        }

        html = re.sub(
            r'{{#if\s+(\w+)}}([\s\S]*?){{/if}}',
            lambda match: match.group(2) if conditional_values.get(match.group(1)) else '',
            html
        )

        for key, value in replacements.items():
            html = html.replace(key, value)

        return html

    def _normalize_template(self, html_content):
        html = html_content
        html = re.sub(
            r'<h1>\s*{{name}}\s*</h1>\s*<div class="contact">\s*{{email}}\s*\|\s*{{phone}}\s*\|\s*{{position}}\s*</div>',
            '{{personal_info_html}}',
            html
        )
        html = re.sub(r'{{#if\s+summary}}[\s\S]*?{{/if}}', '', html)

        if '{{skills_html}}' in html and '{{summary_html}}' not in html:
            html = html.replace('{{skills_html}}', '{{skills_html}}{{summary_html}}')

        if '{{personal_info_html}}' not in html:
            html = re.sub(r'<body([^>]*)>', r'<body\1>{{personal_info_html}}', html, count=1)

        if '{{summary_html}}' not in html:
            html = re.sub(r'</body>', '{{summary_html}}</body>', html, count=1)

        return html

    def _render_personal_info(self, personal):
        photo = personal.get('photo', '')
        photo_html = ''
        if photo:
            photo_html = f'''
            <td class="personal-photo-wrap">
                <img src="{photo}" alt="photo" class="personal-photo" />
            </td>
            '''

        return f'''
        <table class="personal-info">
            <tr>
                <td class="personal-meta">
                    <div class="personal-row"><span class="personal-label">姓名：</span><span class="personal-value">{personal.get("name", "")}</span></div>
                    <div class="personal-row"><span class="personal-label">邮箱：</span><span class="personal-value">{personal.get("email", "")}</span></div>
                    <div class="personal-row"><span class="personal-label">手机：</span><span class="personal-value">{personal.get("phone", "")}</span></div>
                    <div class="personal-row"><span class="personal-label">应聘职位：</span><span class="personal-value">{personal.get("position", "")}</span></div>
                </td>
                {photo_html}
            </tr>
        </table>
        '''

    def _render_summary(self, summary):
        if not summary:
            return ''
        return f'''
        <div class="section">
            <h2>个人简介</h2>
            <div class="item-content">{summary}</div>
        </div>
        '''

    def _render_education(self, education_list):
        if not education_list:
            return ''
        html = '<div class="section"><h2>教育经历</h2>'
        for edu in education_list:
            html += f'''
            <div class="item">
                <div class="item-header">
                    <span class="item-title">{edu.get("school", "")}</span>
                    <span class="item-date">{edu.get("period", "")}</span>
                </div>
                <div class="item-subtitle">{edu.get("degree", "")} - {edu.get("major", "")}</div>
            </div>
            '''
        html += '</div>'
        return html

    def _render_experience(self, experience_list):
        if not experience_list:
            return ''
        html = '<div class="section"><h2>工作经历</h2>'
        for exp in experience_list:
            html += f'''
            <div class="item">
                <div class="item-header">
                    <span class="item-title">{exp.get("company", "")}</span>
                    <span class="item-date">{exp.get("period", "")}</span>
                </div>
                <div class="item-subtitle">{exp.get("position", "")}</div>
                <div class="item-content">{exp.get("description", "")}</div>
            </div>
            '''
        html += '</div>'
        return html

    def _render_projects(self, projects_list):
        if not projects_list:
            return ''
        html = '<div class="section"><h2>项目经历</h2>'
        for proj in projects_list:
            html += f'''
            <div class="item">
                <div class="item-header">
                    <span class="item-title">{proj.get("name", "")}</span>
                    <span class="item-date">{proj.get("period", "")}</span>
                </div>
                <div class="item-subtitle">{proj.get("role", "")}</div>
                <div class="item-content">{proj.get("description", "")}</div>
            </div>
            '''
        html += '</div>'
        return html

    def _render_skills(self, skills_list):
        if not skills_list:
            return ''
        return '<div class="section"><h2>技能证书</h2><div class="skills">' + ', '.join(skills_list) + '</div></div>'

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载PDF"""
        resume = self.get_object()
        if not resume.pdf_file:
            return Response({'error': 'PDF文件不存在'}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(
            open(resume.pdf_file.path, 'rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f"{resume.title}.pdf"
        )

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """生成分享链接"""
        resume = self.get_object()
        token = resume.generate_share_token()
        share_url = f"{request.scheme}://{request.get_host()}/share/{token}"
        resume.share_count += 1
        resume.save()
        return Response({'share_url': share_url, 'token': token})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """用户简历统计"""
        from django.db.models import Count
        from templates.models import ResumeTemplate

        user_resumes = self.get_queryset()
        total = user_resumes.count()
        by_status = dict(user_resumes.values('status').annotate(count=Count('id')).values_list('status', 'count'))

        template_stats = list(user_resumes.values('template__name').annotate(count=Count('id')).order_by('-count')[:5])

        return Response({
            'total': total,
            'by_status': by_status,
            'top_templates': template_stats
        })
