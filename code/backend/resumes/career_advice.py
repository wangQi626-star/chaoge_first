import json
import re
import urllib.error
import urllib.request

from django.conf import settings
from django.utils import timezone


class CareerAdviceError(Exception):
    """Raised when generating career advice fails."""


class CareerAdviceService:
    def analyze(self, resume):
        api_key = (settings.DEEPSEEK_API_KEY or '').strip()
        if not api_key:
            raise CareerAdviceError('未配置 DEEPSEEK_API_KEY，无法生成职业建议。')

        resume_data = resume.resume_data or {}
        payload = {
            'model': settings.DEEPSEEK_MODEL,
            'temperature': 0.6,
            'response_format': {'type': 'json_object'},
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        '你是一名资深职业规划顾问和招聘顾问。'
                        '你必须基于用户简历内容给出务实、具体、可执行的中文建议。'
                        '不要输出 Markdown，只能输出 JSON。'
                    ),
                },
                {
                    'role': 'user',
                    'content': self._build_prompt(resume.title, resume_data),
                },
            ],
        }

        request = urllib.request.Request(
            settings.DEEPSEEK_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw_body = response.read().decode('utf-8')
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode('utf-8', errors='ignore')
            raise CareerAdviceError(f'DeepSeek 请求失败：{error_body[:300]}') from exc
        except urllib.error.URLError as exc:
            raise CareerAdviceError('无法连接 DeepSeek 服务，请稍后重试。') from exc

        try:
            data = json.loads(raw_body)
            content = data['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise CareerAdviceError('DeepSeek 返回结果格式异常。') from exc

        parsed = self._parse_json_content(content)
        return self._normalize_response(resume, parsed)

    def _build_prompt(self, title, resume_data):
        personal = resume_data.get('personal', {}) or {}
        education = resume_data.get('education', []) or []
        experience = resume_data.get('experience', []) or []
        projects = resume_data.get('projects', []) or []
        skills = resume_data.get('skills', []) or []

        education_text = self._render_items(
            education,
            [('school', '学校'), ('degree', '学历'), ('major', '专业'), ('period', '时间')],
        )
        experience_text = self._render_items(
            experience,
            [('company', '公司'), ('position', '岗位'), ('period', '时间'), ('description', '描述')],
        )
        project_text = self._render_items(
            projects,
            [('name', '项目'), ('role', '角色'), ('period', '时间'), ('description', '描述')],
        )

        return f"""
请根据以下简历信息输出职业建议，只能返回 JSON 对象，不要输出任何解释文字。

简历标题：{title or '未命名简历'}
姓名：{personal.get('name', '')}
求职方向：{personal.get('position', '')}
邮箱：{personal.get('email', '')}
电话：{personal.get('phone', '')}
个人简介：{personal.get('summary', '')}
技能证书：{', '.join([str(skill) for skill in skills if skill])}

教育经历：
{education_text}

工作经历：
{experience_text}

项目经历：
{project_text}

输出 JSON schema 如下：
{{
  "short_term_goal": {{
    "title": "一句话标题",
    "description": "短期目标总结，80字以内",
    "actions": ["行动建议1", "行动建议2", "行动建议3"]
  }},
  "skill_suggestions": {{
    "title": "一句话标题",
    "description": "技能提升总结，80字以内",
    "actions": ["技能建议1", "技能建议2", "技能建议3"]
  }},
  "long_term_plan": {{
    "title": "一句话标题",
    "description": "长期规划总结，80字以内",
    "actions": ["长期建议1", "长期建议2", "长期建议3"]
  }},
  "job_recommendations": [
    {{
      "title": "岗位名称",
      "match_score": 86,
      "reason": "为什么适合这个岗位，60字以内",
      "preparation": "下一步准备方向，40字以内",
      "keywords": ["关键词1", "关键词2", "关键词3"]
    }}
  ]
}}

要求：
1. `job_recommendations` 返回 4 到 6 个岗位。
2. `match_score` 必须是 0 到 100 的整数。
3. 内容必须结合简历已有经历，不要泛泛而谈。
4. 避免空字段，字段内容要精炼、职业化、可执行。
        """.strip()

    def _render_items(self, items, fields):
        if not items:
            return '暂无'

        lines = []
        for index, item in enumerate(items, start=1):
            parts = []
            for key, label in fields:
                value = (item or {}).get(key, '')
                if value:
                    parts.append(f'{label}：{value}')
            lines.append(f'{index}. ' + ('；'.join(parts) if parts else '暂无'))
        return '\n'.join(lines)

    def _parse_json_content(self, content):
        if isinstance(content, dict):
            return content

        if not isinstance(content, str):
            raise CareerAdviceError('DeepSeek 返回内容为空。')

        cleaned = content.strip()
        if cleaned.startswith('```'):
            cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r'\{[\s\S]*\}', cleaned)
            if not match:
                raise CareerAdviceError('无法解析 DeepSeek 返回的 JSON 内容。')
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError as exc:
                raise CareerAdviceError('DeepSeek 返回的 JSON 结构不合法。') from exc

    def _normalize_response(self, resume, payload):
        personal = (resume.resume_data or {}).get('personal', {}) or {}
        skills = (resume.resume_data or {}).get('skills', []) or []

        return {
            'resume': {
                'id': resume.id,
                'title': resume.title,
                'name': personal.get('name', ''),
                'position': personal.get('position', ''),
                'template_name': getattr(resume.template, 'name', ''),
                'skills': [str(skill) for skill in skills if skill][:8],
            },
            'short_term_goal': self._normalize_section(payload.get('short_term_goal'), '1 年内达成明确岗位突破'),
            'skill_suggestions': self._normalize_section(payload.get('skill_suggestions'), '补齐关键技能短板'),
            'long_term_plan': self._normalize_section(payload.get('long_term_plan'), '形成 3-5 年成长路径'),
            'job_recommendations': self._normalize_jobs(payload.get('job_recommendations')),
            'analyzed_at': timezone.now().isoformat(),
        }

    def _normalize_section(self, section, fallback_title):
        if isinstance(section, str):
            title = fallback_title
            description = section.strip()
            actions = []
        elif isinstance(section, dict):
            title = str(section.get('title') or fallback_title).strip()
            description = str(
                section.get('description')
                or section.get('content')
                or section.get('summary')
                or ''
            ).strip()
            actions = self._normalize_list(
                section.get('actions')
                or section.get('action_items')
                or section.get('suggestions')
            )
        else:
            title = fallback_title
            description = ''
            actions = []

        if not description and actions:
            description = actions[0]
        if not description:
            description = '结合当前简历内容，建议先明确目标岗位并持续补充具有证明力的项目成果。'

        return {
            'title': title,
            'description': description,
            'actions': actions[:3],
        }

    def _normalize_jobs(self, jobs):
        if not isinstance(jobs, list):
            jobs = []

        normalized = []
        for item in jobs:
            if not isinstance(item, dict):
                continue

            title = str(item.get('title') or item.get('job') or item.get('name') or '').strip()
            if not title:
                continue

            raw_score = item.get('match_score', item.get('score', 0))
            try:
                match_score = int(float(raw_score))
            except (TypeError, ValueError):
                match_score = 0
            match_score = max(0, min(match_score, 100))

            normalized.append({
                'title': title,
                'match_score': match_score,
                'reason': str(item.get('reason') or item.get('fit_reason') or '').strip() or '与当前简历中的经历和技能匹配度较高。',
                'preparation': str(item.get('preparation') or item.get('next_step') or '').strip() or '建议进一步补充与岗位对应的项目成果和量化成绩。',
                'keywords': self._normalize_list(item.get('keywords'))[:4],
            })

        return normalized[:6]

    def _normalize_list(self, value):
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [item.strip() for item in re.split(r'[；;\n]', value) if item.strip()]
        return []
