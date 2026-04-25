from django.core.management.base import BaseCommand
from templates.models import ResumeTemplate
import json

class Command(BaseCommand):
    help = '注入 9 套带照片排版且点缀高级艺术元素的顶尖简历模板'

    def handle(self, *args, **kwargs):
        templates_data = [
            {
                "name": "01 杂志大片 (带巨型水印)",
                "description": "背景带有巨大的无衬线字母水印，照片采用画册级方块裁切，充满时尚杂志的先锋感。",
                "category": "modern",
                "html_content": """
                    <style>
                        .tpl-1 { padding: 60px; font-family: -apple-system, "Helvetica Neue", sans-serif; min-height: 1120px; color: #222; position: relative; overflow: hidden; background: #fff; }
                        /* 高级小元素：巨型背景水印 */
                        .watermark { position: absolute; top: -20px; right: -20px; font-size: 180px; font-weight: 900; color: rgba(0,0,0,0.03); z-index: 0; pointer-events: none; letter-spacing: -5px; }
                        /* 证件照与头部信息重构 */
                        .header-zone { position: relative; z-index: 1; border-bottom: 2px solid #111; padding-bottom: 30px; margin-bottom: 40px; }
                        .personal-info { width: 100%; border-collapse: collapse; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 46px; font-weight: 800; letter-spacing: 1px; display: block; margin-bottom: 8px; text-transform: uppercase; }
                        .personal-row:nth-child(4) .personal-value { font-size: 16px; color: #777; display: block; margin-bottom: 20px; letter-spacing: 2px; text-transform: uppercase; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: inline-block; margin-right: 25px; font-size: 13px; font-weight: 500; border: 1px solid #ddd; padding: 4px 12px; border-radius: 20px; }
                        .personal-photo-wrap { text-align: right; width: 150px; vertical-align: top; }
                        .personal-photo { width: 130px; height: 160px; object-fit: cover; filter: grayscale(20%); box-shadow: 10px 10px 0px #F0F0F0; }
                        /* 模块排版 */
                        .section-wrapper { display: flex; margin-bottom: 40px; position: relative; z-index: 1; }
                        h2 { width: 160px; flex-shrink: 0; font-size: 13px; color: #000; text-transform: uppercase; letter-spacing: 3px; margin: 0; font-weight: 700; }
                        .content-area { flex: 1; }
                        .item { margin-bottom: 25px; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
                        .item-title { font-weight: 700; font-size: 16px; }
                        .item-date { color: #888; font-size: 12px; font-family: monospace; }
                        .item-subtitle { color: #666; font-size: 14px; margin-bottom: 8px; }
                        .item-content { font-size: 13.5px; line-height: 1.8; color: #444; }
                    </style>
                    <div class="tpl-1">
                        <div class="watermark">PROFILE</div>
                        <div class="header-zone">
                            {{personal_info_html}}
                        </div>
                        {{#if summary_html}}<div class="section-wrapper"><h2>Summary</h2><div class="content-area">{{summary_html}}</div></div>{{/if}}
                        {{#if experience_html}}<div class="section-wrapper"><h2>Experience</h2><div class="content-area">{{experience_html}}</div></div>{{/if}}
                        {{#if education_html}}<div class="section-wrapper"><h2>Education</h2><div class="content-area">{{education_html}}</div></div>{{/if}}
                        {{#if skills_html}}<div class="section-wrapper"><h2>Skills</h2><div class="content-area">{{skills_html}}</div></div>{{/if}}
                    </div>
                """
            },
            {
                "name": "02 古典常青藤 (带菱形纹样)",
                "description": "哈佛商学院风格，照片采用椭圆复古相框，标题两侧配有古典菱形点缀，极其老钱风。",
                "category": "classic",
                "html_content": """
                    <style>
                        .tpl-2 { padding: 60px 80px; font-family: "Georgia", serif; min-height: 1120px; color: #111; background: #FFFCF8; position: relative; border: 1px solid #EBE5D9; outline: 1px solid #EBE5D9; outline-offset: 8px; margin: 20px; }
                        /* 高级小元素：四角古典十字标 */
                        .tpl-2::before { content: '✤'; position: absolute; top: 10px; left: 10px; color: #CCC; }
                        .tpl-2::after { content: '✤'; position: absolute; top: 10px; right: 10px; color: #CCC; }
                        /* 证件照与头部 */
                        .header-zone { margin-bottom: 40px; border-bottom: 1px solid #111; padding-bottom: 20px; }
                        .personal-info { width: 100%; border-collapse: collapse; }
                        .personal-meta { text-align: center; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 38px; text-transform: uppercase; letter-spacing: 4px; display: block; margin-bottom: 10px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 15px; font-style: italic; color: #444; display: block; margin-bottom: 15px; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: inline-block; margin: 0 10px; font-size: 12px; color: #555; }
                        .personal-photo-wrap { width: 120px; text-align: center; }
                        .personal-photo { width: 100px; height: 125px; object-fit: cover; border-radius: 50%; border: 3px double #CCC; padding: 3px; }
                        /* 模块排版 */
                        .section { margin-bottom: 30px; text-align: justify; }
                        h2 { font-size: 14px; text-transform: uppercase; font-weight: bold; text-align: center; margin-bottom: 20px; letter-spacing: 2px; }
                        /* 高级小元素：标题两侧的菱形 */
                        h2::before, h2::after { content: ' ◆ '; font-size: 9px; color: #999; vertical-align: middle; margin: 0 15px; }
                        .item { margin-bottom: 20px; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; }
                        .item-title { font-weight: bold; font-size: 15px; }
                        .item-subtitle { font-style: italic; margin-bottom: 6px; font-size: 14px; color: #333; }
                        .item-content { font-size: 13px; line-height: 1.7; }
                    </style>
                    <div class="tpl-2">
                        <div class="header-zone">
                            {{personal_info_html}}
                        </div>
                        {{#if summary_html}}<div class="section"><h2>Profile</h2>{{summary_html}}</div>{{/if}}
                        {{#if experience_html}}<div class="section"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                        {{#if education_html}}<div class="section"><h2>Education</h2>{{education_html}}</div>{{/if}}
                        {{#if skills_html}}<div class="section"><h2>Skills</h2>{{skills_html}}</div>{{/if}}
                    </div>
                """
            },
            {
                "name": "03 莫兰迪艺术拱门 (带几何图形)",
                "description": "莫兰迪灰绿侧边栏，照片镶嵌在背景里的半圆拱门图形中，充满了现代艺术馆的治愈感。",
                "category": "modern",
                "html_content": """
                    <style>
                        .tpl-3 { display: flex; min-height: 1120px; font-family: 'Helvetica Neue', sans-serif; color: #2C3539; background: #FFF; }
                        .sidebar { width: 34%; background: #EAECE6; padding: 50px 35px; box-sizing: border-box; position: relative; overflow: hidden; }
                        .main { width: 66%; padding: 50px 45px; box-sizing: border-box; }
                        /* 高级小元素：莫兰迪拱门背景 */
                        .arch-bg { position: absolute; top: -50px; left: 50%; transform: translateX(-50%); width: 220px; height: 350px; background: rgba(255,255,255,0.4); border-radius: 110px 110px 0 0; z-index: 0; }
                        /* 证件照重写 (竖向排列) */
                        .sidebar .personal-info { display: block; position: relative; z-index: 1; margin-bottom: 40px; text-align: center; }
                        .sidebar .personal-meta, .sidebar .personal-row, .sidebar tbody, .sidebar tr, .sidebar td { display: block; width: 100%; }
                        .sidebar .personal-photo-wrap { margin-bottom: 25px; display: flex; justify-content: center; }
                        .sidebar .personal-photo { width: 140px; height: 140px; object-fit: cover; border-radius: 50%; border: 4px solid #FFF; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
                        .sidebar .personal-label { display: none; }
                        .sidebar .personal-row:nth-child(1) .personal-value { font-size: 32px; font-weight: 700; color: #1A202C; }
                        .sidebar .personal-row:nth-child(4) .personal-value { font-size: 14px; color: #5A6A62; margin-top: 5px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
                        .sidebar .personal-row:nth-child(2), .sidebar .personal-row:nth-child(3) { font-size: 12px; color: #4A5568; margin-bottom: 8px; background: rgba(255,255,255,0.6); padding: 6px; border-radius: 8px; }
                        /* 模块排版 */
                        h2 { font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 1px solid #CBD5E0; }
                        .sidebar h2 { border-bottom-color: #BFC9C2; color: #3E4C45; margin-top: 30px; }
                        .item { margin-bottom: 25px; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; }
                        .item-title { font-weight: 700; font-size: 16px; color: #2D3748; }
                        .item-date { font-size: 12px; color: #718096; }
                        .item-content { font-size: 13.5px; line-height: 1.8; color: #4A5568; margin-top: 6px; }
                    </style>
                    <div class="tpl-3">
                        <div class="sidebar">
                            <div class="arch-bg"></div>
                            {{personal_info_html}}
                            {{#if skills_html}}<div class="section"><h2>Skills</h2><div style="font-size:13px; line-height:1.8;">{{skills_html}}</div></div>{{/if}}
                        </div>
                        <div class="main">
                            {{#if summary_html}}<div class="section"><h2>Profile</h2>{{summary_html}}</div>{{/if}}
                            {{#if experience_html}}<div class="section"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                            {{#if education_html}}<div class="section"><h2>Education</h2>{{education_html}}</div>{{/if}}
                            {{#if projects_html}}<div class="section"><h2>Projects</h2>{{projects_html}}</div>{{/if}}
                        </div>
                    </div>
                """
            },
            {
                "name": "04 瑞士网格 (带准星装饰)",
                "description": "极度理性的网格系统。角落带有印刷排版级别的准星（Crosshairs），照片被严格限制为黑白正方形。",
                "category": "creative",
                "html_content": """
                    <style>
                        .tpl-4 { padding: 40px; font-family: "Helvetica Neue", sans-serif; min-height: 1120px; background: #fff; color: #111; }
                        .wrapper { border: 1px solid #111; height: 100%; display: flex; flex-direction: column; position: relative; }
                        /* 高级小元素：四个角的印刷十字准星 */
                        .crosshair { position: absolute; width: 20px; height: 20px; }
                        .crosshair::before { content: ''; position: absolute; top: 9px; left: -5px; width: 30px; height: 1px; background: #111; }
                        .crosshair::after { content: ''; position: absolute; top: -5px; left: 9px; width: 1px; height: 30px; background: #111; }
                        .tl { top: -10px; left: -10px; } .tr { top: -10px; right: -10px; } .bl { bottom: -10px; left: -10px; } .br { bottom: -10px; right: -10px; }
                        /* 证件照与头部 */
                        .header { border-bottom: 1px solid #111; background: #F9F9F9; }
                        .personal-info { width: 100%; border-collapse: collapse; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 48px; font-weight: 800; letter-spacing: -2px; display: block; margin-bottom: 10px; padding-left: 30px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 16px; font-weight: 600; display: block; padding-left: 30px; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: block; padding-left: 30px; font-size: 12px; color: #555; }
                        .personal-photo-wrap { text-align: right; width: 160px; border-left: 1px solid #111; }
                        .personal-photo { width: 160px; height: 160px; object-fit: cover; filter: grayscale(100%); display: block; }
                        /* 网格系统 */
                        .grid { display: grid; grid-template-columns: 1fr 1fr; flex: 1; }
                        .box { border-right: 1px solid #111; border-bottom: 1px solid #111; padding: 30px; }
                        .box:nth-child(even) { border-right: none; }
                        .box-full { grid-column: span 2; border-right: none; }
                        h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 2px; margin-top: 0; margin-bottom: 20px; font-weight: 800; display: inline-block; background: #111; color: #fff; padding: 4px 10px; }
                        .item-title { font-size: 16px; font-weight: 700; }
                        .item-content { font-size: 13px; line-height: 1.6; color: #333; }
                    </style>
                    <div class="tpl-4">
                        <div class="wrapper">
                            <div class="crosshair tl"></div><div class="crosshair tr"></div>
                            <div class="crosshair bl"></div><div class="crosshair br"></div>
                            <div class="header">{{personal_info_html}}</div>
                            <div class="grid">
                                {{#if summary_html}}<div class="box box-full"><h2>Summary</h2>{{summary_html}}</div>{{/if}}
                                {{#if experience_html}}<div class="box box-full"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                                {{#if education_html}}<div class="box"><h2>Education</h2>{{education_html}}</div>{{/if}}
                                {{#if skills_html}}<div class="box"><h2>Skills</h2>{{skills_html}}</div>{{/if}}
                            </div>
                        </div>
                    </div>
                """
            },
            {
                "name": "05 悬浮卡片 (高斯模糊微光)",
                "description": "极具现代科技感的 UI 设计。背景带有微弱的紫色极光效果，悬浮照片（Squircle圆角矩形）质感无敌。",
                "category": "modern",
                "html_content": """
                    <style>
                        .tpl-5 { padding: 40px; font-family: -apple-system, sans-serif; color: #333; min-height: 1120px; background: #FAFAFB; position: relative; overflow: hidden; }
                        /* 高级小元素：背景高斯模糊极光 */
                        .glow-blob { position: absolute; top: -100px; right: -100px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%); border-radius: 50%; z-index: 0; pointer-events: none; }
                        .card { background: #FFFFFF; border-radius: 20px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.03); min-height: 1040px; box-sizing: border-box; position: relative; z-index: 1; border: 1px solid rgba(255,255,255,0.5); backdrop-filter: blur(10px); }
                        /* 证件照与头部 */
                        .personal-info { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 34px; font-weight: 800; color: #111827; display: block; margin-bottom: 6px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 16px; color: #6B7280; display: block; margin-bottom: 15px; font-weight: 500; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: inline-block; font-size: 13px; color: #4B5563; background: #F3F4F6; padding: 6px 14px; border-radius: 20px; margin-right: 10px; }
                        .personal-photo-wrap { text-align: right; width: 140px; }
                        .personal-photo { width: 110px; height: 110px; object-fit: cover; border-radius: 30px; box-shadow: 0 10px 20px rgba(99,102,241,0.15); }
                        /* 模块排版 */
                        h2 { font-size: 14px; color: #4F46E5; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; border-bottom: 2px solid #EEF2FF; padding-bottom: 8px; }
                        .item { margin-bottom: 25px; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; }
                        .item-title { font-weight: 700; font-size: 16px; color: #1F2937; }
                        .item-date { color: #9CA3AF; font-size: 13px; font-weight: 500; }
                        .item-content { font-size: 14px; line-height: 1.7; color: #4B5563; }
                    </style>
                    <div class="tpl-5">
                        <div class="glow-blob"></div>
                        <div class="card">
                            {{personal_info_html}}
                            {{#if summary_html}}<div class="section"><h2>About Me</h2>{{summary_html}}</div>{{/if}}
                            {{#if experience_html}}<div class="section"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                            <div style="display:flex; gap:40px;">
                                <div style="flex:1;">{{#if education_html}}<div class="section"><h2>Education</h2>{{education_html}}</div>{{/if}}</div>
                                <div style="flex:1;">{{#if skills_html}}<div class="section"><h2>Skills</h2>{{skills_html}}</div>{{/if}}</div>
                            </div>
                        </div>
                    </div>
                """
            },
            {
                "name": "06 炭黑切角 (赛博斜线修饰)",
                "description": "非对称深灰侧边栏。标题带有 // 斜杠装饰，姓名处带有极简荧光黄点缀，证件照完美适配深色背景。",
                "category": "modern",
                "html_content": """
                    <style>
                        .tpl-6 { display: flex; font-family: 'Helvetica', sans-serif; color: #333; min-height: 1120px; }
                        .sidebar { width: 35%; background: #222; color: #FFF; padding: 50px 35px; box-sizing: border-box; position: relative; }
                        .main { width: 65%; background: #FFF; padding: 50px 45px; box-sizing: border-box; }
                        /* 高级小元素：荧光黄高亮方块 */
                        .accent-square { position: absolute; top: 50px; left: 0; width: 8px; height: 40px; background: #FFD700; }
                        /* 证件照重写 (深色背景适配) */
                        .sidebar .personal-info { display: block; margin-bottom: 40px; }
                        .sidebar .personal-meta, .sidebar .personal-row, .sidebar tbody, .sidebar tr, .sidebar td { display: block; width: 100%; }
                        .sidebar .personal-photo-wrap { margin-bottom: 25px; }
                        .sidebar .personal-photo { width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #FFD700; }
                        .sidebar .personal-label { display: none; }
                        .sidebar .personal-row:nth-child(1) .personal-value { font-size: 36px; font-weight: 800; color: #FFF; letter-spacing: 1px; }
                        .sidebar .personal-row:nth-child(4) .personal-value { font-size: 15px; color: #AAA; margin-top: 5px; margin-bottom: 20px; text-transform: uppercase; }
                        .sidebar .personal-row:nth-child(2), .sidebar .personal-row:nth-child(3) { font-size: 13px; color: #888; margin-bottom: 5px; }
                        /* 模块排版 */
                        h2 { font-size: 16px; text-transform: uppercase; color: #111; border-bottom: 2px solid #111; padding-bottom: 8px; margin-bottom: 25px; font-weight: 800; }
                        /* 高级小元素：// 标题装饰 */
                        .sidebar h2 { color: #888; border-bottom-color: #444; font-size: 14px; }
                        h2::before { content: '// '; color: #FFD700; }
                        .item { margin-bottom: 25px; }
                        .item-title { font-weight: bold; font-size: 16px; color: #000; }
                        .sidebar .item-title { color: #FFF; font-size: 14px; margin-bottom: 5px; }
                        .item-date { color: #666; font-size: 13px; margin-bottom: 5px; }
                        .item-content { font-size: 13.5px; line-height: 1.7; color: #444; }
                    </style>
                    <div class="tpl-6">
                        <div class="sidebar">
                            <div class="accent-square"></div>
                            {{personal_info_html}}
                            {{#if skills_html}}<div class="section"><h2>Expertise</h2>{{skills_html}}</div>{{/if}}
                            {{#if education_html}}<div class="section" style="margin-top:40px;"><h2>Education</h2><div style="font-size:13px; color:#CCC;">{{education_html}}</div></div>{{/if}}
                        </div>
                        <div class="main">
                            {{#if summary_html}}<div class="section"><h2>Profile</h2>{{summary_html}}</div>{{/if}}
                            {{#if experience_html}}<div class="section"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                            {{#if projects_html}}<div class="section"><h2>Projects</h2>{{projects_html}}</div>{{/if}}
                        </div>
                    </div>
                """
            },
            {
                "name": "07 解构主义 (重影偏移)",
                "description": "极具艺术张力，证件照带有夸张的色块偏移底框，姓名放大极限错位，Kinfolk 画册级的阅读体验。",
                "category": "creative",
                "html_content": """
                    <style>
                        .tpl-7 { padding: 60px; font-family: "Georgia", serif; color: #111; min-height: 1120px; background: #FFFCF9; }
                        /* 证件照与头部极度错落排版 */
                        .header-zone { margin-bottom: 60px; }
                        .personal-info { width: 100%; border-collapse: collapse; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 65px; font-style: italic; font-weight: 700; display: block; line-height: 0.9; margin-bottom: 15px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 16px; color: #777; font-family: "Helvetica", sans-serif; text-transform: uppercase; letter-spacing: 3px; display: block; margin-bottom: 20px; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: block; font-size: 13px; font-family: "Helvetica", sans-serif; color: #000; font-weight: bold; margin-bottom: 5px; }
                        .personal-photo-wrap { text-align: right; width: 200px; vertical-align: middle; }
                        /* 高级小元素：照片的夸张偏移色块阴影 */
                        .personal-photo { width: 140px; height: 180px; object-fit: cover; box-shadow: 15px 15px 0px #E5D5C5; border: 1px solid #111; }
                        /* 模块排版 */
                        h2 { font-size: 18px; font-weight: normal; border-bottom: 1px solid #CCC; padding-bottom: 10px; margin-bottom: 25px; letter-spacing: 1px; }
                        .item { display: flex; gap: 30px; margin-bottom: 25px; }
                        .item-date { width: 100px; flex-shrink: 0; font-size: 12px; color: #888; font-family: "Helvetica", sans-serif; padding-top: 3px; }
                        .item-main { flex: 1; }
                        .item-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; }
                        .item-content { font-family: "Helvetica", sans-serif; font-size: 13.5px; line-height: 1.8; color: #444; }
                    </style>
                    <div class="tpl-7">
                        <div class="header-zone">
                            {{personal_info_html}}
                        </div>
                        {{#if experience_html}}<div class="section"><h2>Professional Journey</h2>{{experience_html}}</div>{{/if}}
                        {{#if education_html}}<div class="section"><h2>Academic Background</h2>{{education_html}}</div>{{/if}}
                        {{#if skills_html}}<div class="section"><h2>Core Capabilities</h2><div style="font-family:'Helvetica',sans-serif;font-size:13.5px;">{{skills_html}}</div></div>{{/if}}
                    </div>
                """
            },
            {
                "name": "08 包豪斯空间 (几何点缀)",
                "description": "极简到极致的排版，只用字号建立视觉秩序，背景配有红蓝黄包豪斯三原色小几何块点缀，照片裁切锐利。",
                "category": "simple",
                "html_content": """
                    <style>
                        .tpl-8 { padding: 70px 80px; font-family: 'Helvetica Neue', Arial, sans-serif; color: #000; min-height: 1120px; background: #fff; position: relative; overflow: hidden; }
                        /* 高级小元素：包豪斯三原色几何装饰 */
                        .b-red { position: absolute; top: 60px; right: 50px; width: 15px; height: 15px; background: #E63946; border-radius: 50%; }
                        .b-blue { position: absolute; bottom: 80px; left: 50px; width: 20px; height: 20px; background: #1D3557; }
                        .b-yellow { position: absolute; top: 300px; right: -10px; width: 40px; height: 5px; background: #F4A261; }
                        /* 证件照与头部 */
                        .personal-info { width: 100%; border-collapse: collapse; margin-bottom: 50px; }
                        .personal-row .personal-label { display: none; }
                        .personal-row:nth-child(1) .personal-value { font-size: 38px; font-weight: 900; letter-spacing: -1px; display: block; margin-bottom: 5px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 16px; color: #555; display: block; margin-bottom: 25px; font-weight: 600; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: inline-block; font-size: 12px; font-weight: 500; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-right: 20px; }
                        .personal-photo-wrap { text-align: right; width: 140px; }
                        .personal-photo { width: 110px; height: 110px; object-fit: cover; clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%); filter: contrast(1.2) grayscale(100%); }
                        /* 模块排版 */
                        h2 { font-size: 13px; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; color: #000; margin-bottom: 25px; }
                        .item { margin-bottom: 30px; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; }
                        .item-title { font-size: 17px; font-weight: 800; letter-spacing: -0.5px; }
                        .item-date { font-size: 12px; color: #A0A0A0; font-weight: 500; }
                        .item-subtitle { font-size: 14px; font-weight: 500; color: #444; margin-top: 4px; margin-bottom: 10px; }
                        .item-content { font-size: 13px; line-height: 1.7; color: #555; }
                    </style>
                    <div class="tpl-8">
                        <div class="b-red"></div><div class="b-blue"></div><div class="b-yellow"></div>
                        {{personal_info_html}}
                        {{#if summary_html}}<div class="section" style="margin-bottom:45px;"><h2>Profile</h2>{{summary_html}}</div>{{/if}}
                        {{#if experience_html}}<div class="section" style="margin-bottom:45px;"><h2>Experience</h2>{{experience_html}}</div>{{/if}}
                        <div style="display:flex; gap:50px;">
                            <div style="flex:1;">{{#if education_html}}<div class="section"><h2>Education</h2>{{education_html}}</div>{{/if}}</div>
                            <div style="flex:1;">{{#if skills_html}}<div class="section"><h2>Skills</h2>{{skills_html}}</div>{{/if}}</div>
                        </div>
                    </div>
                """
            },
            {
                "name": "09 极简悬线 (空灵留白)",
                "description": "极度空灵。照片采用正圆排版，时间轴带有淡淡的穿插竖线，适合互联网、产品经理，逻辑极度清晰。",
                "category": "modern",
                "html_content": """
                    <style>
                        .tpl-9 { padding: 60px; font-family: 'Avenir', sans-serif; color: #2C3E50; min-height: 1120px; background: #FCFCFC; }
                        /* 证件照与头部 */
                        .personal-info { width: 100%; border-collapse: collapse; border-bottom: 1px solid #EAEAEA; padding-bottom: 30px; margin-bottom: 40px; }
                        .personal-row .personal-label { display: none; }
                        .personal-meta { text-align: center; }
                        .personal-row:nth-child(1) .personal-value { font-size: 34px; font-weight: 300; letter-spacing: 4px; color: #1A1A1A; display: block; margin-bottom: 8px; }
                        .personal-row:nth-child(4) .personal-value { font-size: 14px; color: #666; display: block; margin-bottom: 15px; letter-spacing: 1px; }
                        .personal-row:nth-child(2), .personal-row:nth-child(3) { display: inline-block; font-size: 13px; color: #888; margin: 0 10px; }
                        .personal-photo-wrap { width: 120px; text-align: center; }
                        .personal-photo { width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 1px solid #EAEAEA; padding: 4px; }
                        /* 模块排版 */
                        h2 { font-size: 14px; color: #A0A0A0; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 3px; font-weight: 600; text-align: center; }
                        /* 高级小元素：悬空时间轴 */
                        .timeline-wrapper { position: relative; padding-left: 30px; margin-bottom: 50px; }
                        .timeline-wrapper::before { content: ''; position: absolute; left: 6px; top: 8px; bottom: 0; width: 1px; background: #DCDCDC; }
                        .item { position: relative; margin-bottom: 35px; }
                        .item::before { content: ''; position: absolute; left: -28px; top: 8px; width: 6px; height: 6px; border-radius: 50%; background: #FCFCFC; border: 2px solid #A0A0A0; }
                        .item-header { display: flex; justify-content: space-between; align-items: baseline; }
                        .item-title { font-weight: 600; font-size: 16px; color: #111; }
                        .item-date { color: #999; font-size: 12px; letter-spacing: 0.5px; }
                        .item-content { font-size: 13px; line-height: 1.8; color: #555; margin-top: 10px; }
                    </style>
                    <div class="tpl-9">
                        {{personal_info_html}}
                        {{#if summary_html}}<div><h2>— Profile —</h2><div style="text-align:center; margin-bottom:50px; font-size:14px; color:#555; line-height:1.8; padding: 0 40px;">{{summary_html}}</div></div>{{/if}}
                        {{#if experience_html}}<div><h2>— Experience —</h2><div class="timeline-wrapper">{{experience_html}}</div></div>{{/if}}
                        {{#if education_html}}<div><h2>— Education —</h2><div class="timeline-wrapper" style="margin-bottom:0;">{{education_html}}</div></div>{{/if}}
                    </div>
                """
            }
        ]

        count = 0
        for data in templates_data:
            ResumeTemplate.objects.update_or_create(name=data['name'], defaults=data)
            count += 1
            self.stdout.write(self.style.SUCCESS(f'成功注入终极装饰排版: {data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'完成！共处理了 {count} 个完美融合证件照与高级小元素的模板。'))