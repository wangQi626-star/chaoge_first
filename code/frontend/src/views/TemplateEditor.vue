<template>
  <div class="template-editor">
    <el-card class="editor-card">
      <template #header>
        <div class="header-row">
          <div class="title-area">
            <h2>自定义模板引擎</h2>
            <p class="subtitle">通过参数配置，生成独一无二的专属简历排版结构。</p>
          </div>
          <el-button :icon="ArrowLeft" @click="$router.push('/')">返回首页</el-button>
        </div>
      </template>

      <el-form :model="form" label-width="120px" class="editor-form">
        <div class="form-section">
          <div class="section-title">01 / 基础信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="模板名称">
                <el-input v-model="form.name" placeholder="例如：我的高级质感模板" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="模板风格">
                <el-select v-model="form.category" placeholder="选择风格" style="width: 100%;">
                  <el-option label="经典风格 (Classic)" value="classic" />
                  <el-option label="现代风格 (Modern)" value="modern" />
                  <el-option label="创意风格 (Creative)" value="creative" />
                  <el-option label="简约风格 (Simple)" value="simple" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="模板描述">
                <el-input v-model="form.description" type="textarea" :rows="2" placeholder="简单描述这个模板的特点..." />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="section-title">02 / 版式与字体</div>
          <el-row :gutter="20">
            <el-col :span="24">
              <el-form-item label="整体布局">
                <el-radio-group v-model="form.layout">
                  <el-radio-button value="single">经典单栏</el-radio-button>
                  <el-radio-button value="double">左右等分 (50/50)</el-radio-button>
                  <el-radio-button value="sidebar">左侧边栏 (35/65)</el-radio-button>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="模块样式">
                <el-radio-group v-model="form.module_style">
                  <el-radio value="minimal">极简留白</el-radio>
                  <el-radio value="line">标题底边线</el-radio>
                  <el-radio value="left-border">左侧强调线</el-radio>
                  <el-radio value="card">UI悬浮卡片 (带阴影)</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="字体风格">
                <el-select v-model="form.font_family" style="width: 100%;">
                  <el-option label="现代黑体 (Sans-serif)" value="sans" />
                  <el-option label="优雅衬线 (Serif)" value="serif" />
                  <el-option label="极客代码 (Monospace)" value="mono" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="内容间距">
                <el-select v-model="form.spacing" style="width: 100%;">
                  <el-option label="紧凑 (Compact)" value="compact" />
                  <el-option label="适中 (Normal)" value="normal" />
                  <el-option label="宽松 (Spacious)" value="spacious" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="基础字号">
                <el-input-number v-model="form.font_size" :min="12" :max="18" controls-position="right" style="width: 100%;" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="section-title">03 / 品牌配色</div>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="主色调" class="color-item">
                <el-color-picker v-model="form.color_scheme.primary" show-alpha />
                <div class="color-tip">大标题/侧边栏</div>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="辅助色" class="color-item">
                <el-color-picker v-model="form.color_scheme.secondary" show-alpha />
                <div class="color-tip">小标题/副文本</div>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="强调色" class="color-item">
                <el-color-picker v-model="form.color_scheme.accent" show-alpha />
                <div class="color-tip">线条/装饰边框</div>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="背景色" class="color-item">
                <el-color-picker v-model="form.color_scheme.background" show-alpha />
                <div class="color-tip">页面整体背景</div>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-actions">
          <el-button size="large" @click="previewTemplate">实时预览排版</el-button>
          <el-button type="primary" size="large" @click="saveTemplate">保存至模板库</el-button>
        </div>
      </el-form>
    </el-card>

    <el-dialog v-model="showPreview" title="模板实时渲染预览" width="850px" destroy-on-close top="5vh">
      <div class="preview-scroll-area">
        <component :is="'style'">{{ generatedPreview.css }}</component>
        <div class="preview-render-box" v-html="generatedPreview.html"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const showPreview = ref(false)
const generatedPreview = reactive({ html: '', css: '' })

// 初始表单数据
const form = ref({
  name: '',
  description: '',
  category: 'modern',
  layout: 'sidebar',
  module_style: 'line',
  font_family: 'sans',
  spacing: 'normal',
  font_size: 14,
  color_scheme: {
    primary: '#2C3E50',
    secondary: '#34495E',
    accent: '#3498DB',
    background: '#FFFFFF'
  }
})

const fontMap = {
  'sans': "'-apple-system', 'Helvetica Neue', Helvetica, Arial, sans-serif",
  'serif': "'Georgia', 'Times New Roman', serif",
  'mono': "'Courier New', Courier, monospace"
}

const spaceMap = {
  'compact': { margin: '15px', padding: '15px' },
  'normal': { margin: '25px', padding: '25px' },
  'spacious': { margin: '40px', padding: '35px' }
}

// 引擎核心：将用户配置转换成真实的 HTML & CSS
const generateTemplateData = () => {
  const cfg = form.value
  const c = cfg.color_scheme
  const space = spaceMap[cfg.spacing]

  let css = `
    .resume-container {
      background: ${c.background};
      font-family: ${fontMap[cfg.font_family]};
      font-size: ${cfg.font_size}px;
      color: #333;
      min-height: 1120px;
      box-sizing: border-box;
      line-height: 1.6;
    }
    .custom-section { margin-bottom: ${space.margin}; }
    .custom-section h2 {
      color: ${c.secondary};
      font-size: ${cfg.font_size + 4}px;
      margin-top: 0;
      margin-bottom: 15px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .item-header { display: flex; justify-content: space-between; align-items: baseline; font-weight: bold; }
    .item-title { color: #111; font-size: ${cfg.font_size + 2}px; }
    .item-date { color: ${c.accent}; font-size: ${cfg.font_size - 1}px; }
    .item-subtitle { color: #666; margin-bottom: 5px; font-style: italic; }
  `

  if (cfg.module_style === 'line') {
    css += `.custom-section h2 { border-bottom: 2px solid ${c.accent}; padding-bottom: 8px; }`
  } else if (cfg.module_style === 'left-border') {
    css += `.custom-section { border-left: 4px solid ${c.accent}; padding-left: 15px; }`
  } else if (cfg.module_style === 'card') {
    css += `
      .custom-section {
        background: #fff;
        padding: ${space.padding};
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
      }
      .resume-container { background: #F3F4F6; padding: 30px; }
    `
  }

  let html = ''
  const contentBlocks = `
    {{#if summary_html}}<div class="custom-section"><h2>个人简介</h2>{{summary_html}}</div>{{/if}}
    {{#if experience_html}}<div class="custom-section"><h2>工作经历</h2>{{experience_html}}</div>{{/if}}
    {{#if projects_html}}<div class="custom-section"><h2>项目经验</h2>{{projects_html}}</div>{{/if}}
    {{#if education_html}}<div class="custom-section"><h2>教育背景</h2>{{education_html}}</div>{{/if}}
  `
  const sidebarBlocks = `
    {{#if skills_html}}<div class="custom-section"><h2>专业技能</h2>{{skills_html}}</div>{{/if}}
  `

  if (cfg.layout === 'sidebar') {
    css += `
      .layout-sidebar { display: flex; width: 100%; min-height: 1120px; }
      .sidebar-left { width: 35%; background: ${c.primary}; color: #fff; padding: 40px ${space.padding}; }
      .sidebar-left h2 { color: #fff; border-color: rgba(255,255,255,0.3); }
      .sidebar-left .personal-info { color: #fff; margin-bottom: 40px; }
      .main-right { width: 65%; padding: 40px ${space.padding}; }
    `
    html = `
      <div class="resume-container layout-sidebar">
        <div class="sidebar-left">
          {{personal_info_html}}
          ${sidebarBlocks}
        </div>
        <div class="main-right">
          ${contentBlocks}
        </div>
      </div>
    `
  } else if (cfg.layout === 'double') {
    css += `
      .layout-double { padding: 40px ${space.padding}; }
      .top-header { border-bottom: 3px solid ${c.primary}; padding-bottom: 20px; margin-bottom: ${space.margin}; }
      .grid-50 { display: flex; gap: ${space.margin}; }
      .grid-col { flex: 1; }
    `
    html = `
      <div class="resume-container layout-double">
        <div class="top-header">{{personal_info_html}}</div>
        <div class="grid-50">
          <div class="grid-col">${contentBlocks}</div>
          <div class="grid-col">${sidebarBlocks}</div>
        </div>
      </div>
    `
  } else {
    css += `
      .layout-single { padding: 50px ${space.padding}; max-width: 900px; margin: 0 auto; }
      .top-header { text-align: center; margin-bottom: ${space.margin}; }
    `
    html = `
      <div class="resume-container layout-single">
        <div class="top-header">{{personal_info_html}}</div>
        ${contentBlocks}
        ${sidebarBlocks}
      </div>
    `
  }

  return { html, css }
}

const previewTemplate = () => {
  const result = generateTemplateData()

  let mockHtml = result.html
  mockHtml = mockHtml.replace('{{personal_info_html}}', `
    <div style="margin-bottom: 20px;">
      <h1 style="margin:0 0 10px 0; font-size:32px;">张三 (San Zhang)</h1>
      <p style="margin:0; opacity:0.8;">资深前端开发工程师 | 13800138000 | admin@example.com</p>
    </div>
  `)
  mockHtml = mockHtml.replace(/{{#if \w+}}|{{\/if}}/g, '')
  mockHtml = mockHtml.replace('{{summary_html}}', '<p>具备 5 年以上开发经验，热爱技术，追求极致的代码质量与排版美学。</p>')
  mockHtml = mockHtml.replace('{{experience_html}}', `
    <div style="margin-bottom:15px;">
      <div class="item-header"><span class="item-title">某某科技 (深圳) 有限公司</span><span class="item-date">2020.07 - 至今</span></div>
      <div class="item-subtitle">高级前端开发工程师</div>
      <p style="margin:5px 0 0 0;">负责核心业务模块的重构与性能优化，搭建微前端架构体系。</p>
    </div>
  `)
  mockHtml = mockHtml.replace('{{projects_html}}', '<p>暂无项目经验展示</p>')
  mockHtml = mockHtml.replace('{{education_html}}', `
    <div class="item-header"><span class="item-title">某某大学</span><span class="item-date">2016.09 - 2020.06</span></div>
    <div class="item-subtitle">计算机科学与技术 (本科)</div>
  `)
  mockHtml = mockHtml.replace('{{skills_html}}', '<ul style="padding-left: 20px; margin-top:5px;"><li>精通 Vue/React</li><li>熟练掌握工程化部署</li></ul>')

  generatedPreview.css = result.css
  generatedPreview.html = mockHtml
  showPreview.value = true
}

const saveTemplate = async () => {
  if (!form.value.name) {
    ElMessage.warning('请先为您的模板起个名字！')
    return
  }

  const { html, css } = generateTemplateData()

  try {
    const payload = { ...form.value, html_content: html, css_content: css }
    if (typeof payload.color_scheme === 'object') {
      payload.color_scheme = JSON.stringify(payload.color_scheme)
    }

    await api.post('/templates/', payload)
    ElMessage.success('专属模板保存成功！快去模板集市看看吧。')
    router.push('/templates')
  } catch (error) {
    ElMessage.error('保存失败，请检查网络')
  }
}
</script>

<style scoped>
.template-editor {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
}

.editor-card {
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
  border: none;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-area h2 {
  margin: 0 0 8px 0;
  color: #1f2937;
  font-size: 24px;
}

.subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.editor-form {
  padding: 10px 20px;
}

.form-section {
  background: #f9fafb;
  border: 1px solid #f3f4f6;
  border-radius: 12px;
  padding: 25px 30px 10px;
  margin-bottom: 30px;
  position: relative;
}

.section-title {
  position: absolute;
  top: -12px;
  left: 20px;
  background: #fff;
  padding: 0 15px;
  font-size: 13px;
  font-weight: 600;
  color: #4f46e5;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
}

.color-item {
  display: flex;
  flex-direction: column;
}

.color-tip {
  color: #9ca3af;
  font-size: 12px;
  line-height: 1.4;
  margin-top: 6px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e5e7eb;
}

/* 预览弹窗样式 */
.preview-scroll-area {
  max-height: 70vh;
  overflow-y: auto;
  background: #edf2f7;
  padding: 30px;
  border-radius: 8px;
}

.preview-render-box {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border-radius: 4px;
  overflow: hidden;
  margin: 0 auto;
  max-width: 800px;
}
</style>