<template>
  <div class="resume-editor-container">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
          <h2>{{ isEdit ? '编辑简历' : '创建简历' }}</h2>
        </div>
        <div class="header-right">
          <el-button @click="togglePreview">
            <el-icon><View v-if="!showPreview" /><Edit v-else /></el-icon>
            {{ showPreview ? '编辑' : '预览' }}
          </el-button>
          <el-button type="primary" :loading="saving" @click="saveResume">保存</el-button>
          <el-button type="warning" plain :disabled="!resumeId" @click="goCareerAdvice">AI职业建议</el-button>
          <el-button type="success" :loading="generating" @click="exportPdf">
            导出PDF
          </el-button>
        </div>
      </el-header>

      <el-main>
        <div v-if="!showPreview" class="editor-layout">
          <el-tabs v-model="activeTab" tab-position="left" class="resume-tabs">
            <el-tab-pane label="个人信息" name="personal">
              <div class="form-section">
                <el-form :model="resumeStore.resumeData.personal" label-width="100px">
                  <el-form-item label="姓名">
                    <el-input v-model="resumeStore.resumeData.personal.name" placeholder="请输入姓名" />
                  </el-form-item>
                  <el-form-item label="邮箱">
                    <el-input v-model="resumeStore.resumeData.personal.email" placeholder="请输入邮箱" />
                  </el-form-item>
                  <el-form-item label="手机">
                    <el-input v-model="resumeStore.resumeData.personal.phone" placeholder="请输入手机号" />
                  </el-form-item>
                  <el-form-item label="应聘职位">
                    <el-input v-model="resumeStore.resumeData.personal.position" placeholder="请输入应聘职位" />
                  </el-form-item>
                  <el-form-item label="个人照片">
                    <div class="photo-field">
                      <input type="file" accept="image/*" @change="handlePhotoChange" />
                      <img
                        v-if="resumeStore.resumeData.personal.photo"
                        :src="resumeStore.resumeData.personal.photo"
                        alt="photo preview"
                        class="photo-preview"
                      />
                      <el-button
                        v-if="resumeStore.resumeData.personal.photo"
                        type="danger"
                        plain
                        @click="removePhoto"
                      >
                        删除照片
                      </el-button>
                    </div>
                  </el-form-item>
                  <el-form-item label="个人简介">
                    <el-input v-model="resumeStore.resumeData.personal.summary" type="textarea" :rows="4" placeholder="请输入个人简介" />
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>

            <el-tab-pane label="教育经历" name="education">
              <div class="form-section">
                <div v-for="(edu, index) in resumeStore.resumeData.education" :key="index" class="item-card">
                  <el-card>
                    <el-form label-width="80px">
                      <el-form-item label="学校">
                        <el-input v-model="edu.school" placeholder="学校名称" />
                      </el-form-item>
                      <el-form-item label="学历">
                        <el-input v-model="edu.degree" placeholder="学历，如本科、硕士" />
                      </el-form-item>
                      <el-form-item label="专业">
                        <el-input v-model="edu.major" placeholder="专业" />
                      </el-form-item>
                      <el-form-item label="时间">
                        <el-input v-model="edu.period" placeholder="如 2019-2023" />
                      </el-form-item>
                    </el-form>
                    <div class="item-actions">
                      <el-button type="danger" size="small" @click="removeEducation(index)">删除</el-button>
                    </div>
                  </el-card>
                </div>
                <el-button type="primary" @click="addEducation">添加教育经历</el-button>
              </div>
            </el-tab-pane>

            <el-tab-pane label="工作经历" name="experience">
              <div class="form-section">
                <div v-for="(exp, index) in resumeStore.resumeData.experience" :key="index" class="item-card">
                  <el-card>
                    <el-form label-width="80px">
                      <el-form-item label="公司">
                        <el-input v-model="exp.company" placeholder="公司名称" />
                      </el-form-item>
                      <el-form-item label="职位">
                        <el-input v-model="exp.position" placeholder="职位" />
                      </el-form-item>
                      <el-form-item label="时间">
                        <el-input v-model="exp.period" placeholder="如 2020-至今" />
                      </el-form-item>
                      <el-form-item label="工作内容">
                        <el-input v-model="exp.description" type="textarea" :rows="4" placeholder="描述工作内容" />
                      </el-form-item>
                    </el-form>
                    <div class="item-actions">
                      <el-button type="danger" size="small" @click="removeExperience(index)">删除</el-button>
                    </div>
                  </el-card>
                </div>
                <el-button type="primary" @click="addExperience">添加工作经历</el-button>
              </div>
            </el-tab-pane>

            <el-tab-pane label="项目经历" name="projects">
              <div class="form-section">
                <div v-for="(proj, index) in resumeStore.resumeData.projects" :key="index" class="item-card">
                  <el-card>
                    <el-form label-width="80px">
                      <el-form-item label="项目名称">
                        <el-input v-model="proj.name" placeholder="项目名称" />
                      </el-form-item>
                      <el-form-item label="角色">
                        <el-input v-model="proj.role" placeholder="担任角色" />
                      </el-form-item>
                      <el-form-item label="时间">
                        <el-input v-model="proj.period" placeholder="如 2021-2022" />
                      </el-form-item>
                      <el-form-item label="项目描述">
                        <el-input v-model="proj.description" type="textarea" :rows="4" placeholder="描述项目内容" />
                      </el-form-item>
                    </el-form>
                    <div class="item-actions">
                      <el-button type="danger" size="small" @click="removeProject(index)">删除</el-button>
                    </div>
                  </el-card>
                </div>
                <el-button type="primary" @click="addProject">添加项目经历</el-button>
              </div>
            </el-tab-pane>

            <el-tab-pane label="技能证书" name="skills">
              <div class="form-section">
                <el-form label-width="100px">
                  <el-form-item label="技能证书">
                    <div class="skills-input">
                      <el-input v-model="skillInput" placeholder="输入技能名称后按回车添加" @keyup.enter="addSkill" />
                      <el-button @click="addSkill">添加</el-button>
                    </div>
                  </el-form-item>
                </el-form>
                <div class="skills-list">
                  <el-tag v-for="(skill, index) in resumeStore.resumeData.skills" :key="index" closable @close="removeSkill(index)">
                    {{ skill }}
                  </el-tag>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div v-else class="preview-layout">
          <div class="preview-container">
            <div ref="previewContainerRef" class="resume-preview" v-html="previewHtml"></div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useResumeStore } from '@/stores/resume'
import { ElMessage } from 'element-plus'
import { ArrowLeft, View, Edit } from '@element-plus/icons-vue'
import html2pdf from 'html2pdf.js'
import api from '@/api'

const router = useRouter()
const route = useRoute()
const resumeStore = useResumeStore()

const activeTab = ref('personal')
const showPreview = ref(false)
const saving = ref(false)
const generating = ref(false)
const skillInput = ref('')
const isEdit = ref(false)
const resumeId = ref(null)
const previewContainerRef = ref(null)

const addEducation = () => {
  resumeStore.addEducation({ school: '', degree: '', major: '', period: '' })
}

const removeEducation = (index) => {
  resumeStore.removeEducation(index)
}

const addExperience = () => {
  resumeStore.addExperience({ company: '', position: '', period: '', description: '' })
}

const removeExperience = (index) => {
  resumeStore.removeExperience(index)
}

const addProject = () => {
  resumeStore.addProject({ name: '', role: '', period: '', description: '' })
}

const removeProject = (index) => {
  resumeStore.removeProject(index)
}

const addSkill = () => {
  if (skillInput.value.trim()) {
    resumeStore.addSkill(skillInput.value.trim())
    skillInput.value = ''
  }
}

const removeSkill = (index) => {
  resumeStore.removeSkill(index)
}

const handlePhotoChange = (event) => {
  const file = event.target.files?.[0]
  event.target.value = ''

  if (!file) {
    return
  }

  if (!file.type.startsWith('image/')) {
    ElMessage.error('璇烽€夋嫨鍥剧墖鏂囦欢')
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    resumeStore.updatePersonal({ photo: reader.result })
  }
  reader.onerror = () => {
    ElMessage.error('鐓х墖璇诲彇澶辫触')
  }
  reader.readAsDataURL(file)
}

const removePhoto = () => {
  resumeStore.updatePersonal({ photo: '' })
}

const togglePreview = () => {
  showPreview.value = !showPreview.value
}

const previewHtml = computed(() => {
  const data = resumeStore.resumeData
  const template = resumeStore.selectedTemplate
  if (!template?.html_content) {
    return renderDefaultTemplate(data)
  }
  return renderTemplate(template.html_content, data)
})

const renderDefaultTemplate = (data) => {
  const p = data.personal
  return `
    <div style="font-family: SimSun; padding: 40px; max-width: 800px; margin: 0 auto;">
      ${renderPersonalInfo(p)}
      ${renderEducation(data.education)}
      ${renderExperience(data.experience)}
      ${renderProjects(data.projects)}
      ${renderSkills(data.skills)}
      ${renderSummary(data.personal.summary)}
    </div>
  `
}

const renderTemplate = (html, data) => {
  if (!html) {
    return renderDefaultTemplate(data)
  }

  let result = normalizeTemplate(html)
  const p = data.personal
  const replacements = {
    name: p.name || '',
    email: p.email || '',
    phone: p.phone || '',
    position: p.position || '',
    summary: p.summary || '',
    personal_info_html: renderPersonalInfo(p),
    education_html: renderEducation(data.education),
    experience_html: renderExperience(data.experience),
    projects_html: renderProjects(data.projects),
    skills_html: renderSkills(data.skills),
    summary_html: renderSummary(p.summary)
  }

  result = result.replace(/{{#if\s+(\w+)}}([\s\S]*?){{\/if}}/g, (_, key, content) => {
    return replacements[key] ? content : ''
  })

  Object.entries(replacements).forEach(([key, value]) => {
    result = result.replace(new RegExp(`{{${key}}}`, 'g'), value)
  })

  return result
}

const normalizeTemplate = (html) => {
  let result = html

  result = result.replace(
    /<h1>\s*{{name}}\s*<\/h1>\s*<div class="contact">\s*{{email}}\s*\|\s*{{phone}}\s*\|\s*{{position}}\s*<\/div>/,
    '{{personal_info_html}}'
  )

  result = result.replace(/{{#if\s+summary}}[\s\S]*?{{\/if}}/g, '')

  if (result.includes('{{skills_html}}') && !result.includes('{{summary_html}}')) {
    result = result.replace(/{{skills_html}}/g, '{{skills_html}}{{summary_html}}')
  }

  if (!result.includes('{{personal_info_html}}')) {
    result = result.replace(/<body([^>]*)>/i, '<body$1>{{personal_info_html}}')
  }

  if (!result.includes('{{summary_html}}')) {
    result = result.replace(/<\/body>/i, '{{summary_html}}</body>')
  }

  return result
}

const renderPersonalInfo = (personal) => {
  const photoHtml = personal.photo
    ? `
      <td class="personal-photo-wrap">
        <img src="${personal.photo}" alt="photo" class="personal-photo" />
      </td>
    `
    : ''

  return `
    <table class="personal-info">
      <tr>
        <td class="personal-meta">
          <div class="personal-row"><span class="personal-label">姓名：</span><span class="personal-value">${personal.name || ''}</span></div>
          <div class="personal-row"><span class="personal-label">邮箱：</span><span class="personal-value">${personal.email || ''}</span></div>
          <div class="personal-row"><span class="personal-label">手机：</span><span class="personal-value">${personal.phone || ''}</span></div>
          <div class="personal-row"><span class="personal-label">应聘职位：</span><span class="personal-value">${personal.position || ''}</span></div>
        </td>
        ${photoHtml}
      </tr>
    </table>
  `
}

const renderSummary = (summary) => {
  if (!summary) {
    return ''
  }

  return `
    <div class="section">
      <h2>个人简介</h2>
      <div class="item-content">${summary}</div>
    </div>
  `
}

const renderEducation = (list) => {
  if (!list || list.length === 0) return ''
  let html = '<div class="section"><h2>教育经历</h2>'
  for (const edu of list) {
    html += `
      <div class="item">
        <div class="item-header">
          <span class="item-title">${edu.school || ''}</span>
          <span class="item-date">${edu.period || ''}</span>
        </div>
        <div class="item-subtitle">${edu.degree || ''} - ${edu.major || ''}</div>
      </div>
    `
  }
  html += '</div>'
  return html
}

const renderExperience = (list) => {
  if (!list || list.length === 0) return ''
  let html = '<div class="section"><h2>工作经历</h2>'
  for (const exp of list) {
    html += `
      <div class="item">
        <div class="item-header">
          <span class="item-title">${exp.company || ''}</span>
          <span class="item-date">${exp.period || ''}</span>
        </div>
        <div class="item-subtitle">${exp.position || ''}</div>
        <div class="item-content">${exp.description || ''}</div>
      </div>
    `
  }
  html += '</div>'
  return html
}

const renderProjects = (list) => {
  if (!list || list.length === 0) return ''
  let html = '<div class="section"><h2>项目经历</h2>'
  for (const proj of list) {
    html += `
      <div class="item">
        <div class="item-header">
          <span class="item-title">${proj.name || ''}</span>
          <span class="item-date">${proj.period || ''}</span>
        </div>
        <div class="item-subtitle">${proj.role || ''}</div>
        <div class="item-content">${proj.description || ''}</div>
      </div>
    `
  }
  html += '</div>'
  return html
}

const renderSkills = (list) => {
  if (!list || list.length === 0) return ''
  return `<div class="section"><h2>技能证书</h2><div class="skills">${list.join(', ')}</div></div>`
}

const formatApiError = (error) => {
  const data = error?.response?.data

  if (!data) {
    return error.message
  }

  if (typeof data === 'string') {
    return data
  }

  if (data.detail) {
    return data.detail
  }

  if (data.error) {
    return data.error
  }

  return Object.entries(data)
    .map(([key, value]) => {
      if (Array.isArray(value)) {
        return `${key}: ${value.join(', ')}`
      }
      return `${key}: ${value}`
    })
    .join('; ')
}

const saveResume = async () => {
  if (!resumeStore.selectedTemplate) {
    ElMessage.warning('请先选择模板')
    router.push('/templates')
    return
  }

  const title = resumeStore.resumeData.personal.name
    ? `${resumeStore.resumeData.personal.name}的简历`
    : '我的简历'

  saving.value = true
  try {
    if (isEdit.value && resumeId.value) {
      await resumeStore.updateResume(resumeId.value)
      ElMessage.success('简历更新成功')
    } else {
      const result = await resumeStore.saveResume(title, resumeStore.selectedTemplate.id)
      resumeId.value = result.id
      isEdit.value = true
      ElMessage.success('简历保存成功')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + formatApiError(error))
  } finally {
    saving.value = false
  }
}

const createExportContainer = (sourceNode) => {
  const container = document.createElement('div')
  const clone = sourceNode.cloneNode(true)
  const sourceWidth = Math.ceil(sourceNode.getBoundingClientRect().width) || 800

  container.style.position = 'fixed'
  container.style.left = '0'
  container.style.top = '0'
  container.style.width = `${sourceWidth}px`
  container.style.background = '#ffffff'
  container.style.opacity = '0'
  container.style.pointerEvents = 'none'
  container.style.zIndex = '-1'
  container.style.overflow = 'visible'
  container.innerHTML = `<div class="export-root"></div>`
  clone.style.width = `${sourceWidth}px`
  clone.style.maxWidth = 'none'
  clone.style.margin = '0'
  clone.querySelectorAll('.section h2').forEach((node) => {
    node.style.display = 'block'
    node.style.lineHeight = '1.1'
    node.style.paddingTop = '0'
    node.style.paddingBottom = '2px'
    node.style.marginTop = '0'
    node.style.marginBottom = '10px'
    node.style.position = 'relative'
    node.style.top = '0'
  })
  clone.querySelectorAll('.item-date').forEach((node) => {
    node.style.display = 'inline-block'
    node.style.lineHeight = '1'
    node.style.paddingTop = '0'
    node.style.paddingBottom = '2px'
    node.style.verticalAlign = 'top'
    node.style.position = 'relative'
    node.style.top = '-6px'
  })
  const exportRoot = container.querySelector('.export-root')
  exportRoot.appendChild(clone)

  return container
}

const waitForImages = async (root) => {
  const images = Array.from(root.querySelectorAll('img'))
  if (!images.length) {
    return
  }

  await Promise.all(images.map((img) => new Promise((resolve) => {
    if (img.complete) {
      resolve()
      return
    }
    img.onload = () => resolve()
    img.onerror = () => resolve()
  })))
}

const exportPdf = async () => {
  generating.value = true
  const wasPreviewVisible = showPreview.value
  try {
    if (!showPreview.value) {
      showPreview.value = true
      await nextTick()
    }

    const sourceNode = previewContainerRef.value
    if (!sourceNode) {
      throw new Error('未找到预览内容，请切换到预览后重试')
    }

    const container = createExportContainer(sourceNode)
    document.body.appendChild(container)
    await nextTick()
    await waitForImages(container)
    await new Promise(resolve => window.setTimeout(resolve, 300))

    const title = resumeStore.resumeData.personal.name
      ? `${resumeStore.resumeData.personal.name}的简历`
      : '我的简历'

    await html2pdf()
      .set({
        margin: [0, 0, 0, 0],
        filename: `${title}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
          scale: 2,
          useCORS: true,
          backgroundColor: '#ffffff',
          logging: false,
          scrollX: 0,
          scrollY: 0,
          width: Math.ceil(sourceNode.getBoundingClientRect().width) || 800,
          windowWidth: Math.ceil(sourceNode.getBoundingClientRect().width) || 800
        },
        jsPDF: {
          unit: 'mm',
          format: 'a4',
          orientation: 'portrait'
        },
        pagebreak: {
          mode: ['css', 'legacy']
        }
      })
      .from(container.querySelector('.export-root'))
      .save()

    container.remove()
  } catch (error) {
    ElMessage.error('导出PDF失败: ' + formatApiError(error))
  } finally {
    if (!wasPreviewVisible) {
      showPreview.value = false
    }
    document.querySelectorAll('.export-root').forEach(node => {
      const host = node.parentElement
      if (host && host.style.opacity === '0') {
        host.remove()
      }
    })
    generating.value = false
  }
}

const goBack = () => {
  router.push('/')
}

const goCareerAdvice = () => {
  if (!resumeId.value) {
    ElMessage.warning('请先保存简历')
    return
  }

  router.push(`/career-advice/${resumeId.value}`)
}

const loadResume = async (id) => {
  try {
    const response = await api.get(`/resumes/${id}/`)
    const data = response.data
    resumeStore.setResumeData(data.resume_data)
    if (data.template_detail) {
      resumeStore.setTemplate(data.template_detail)
    }
    resumeStore.currentResume = data
    resumeId.value = data.id
    isEdit.value = true
  } catch (error) {
    console.error('加载简历失败', error)
  }
}

onMounted(async () => {
  if (route.params.id) {
    await loadResume(route.params.id)
  } else if (!resumeStore.selectedTemplate) {
    router.push('/templates')
  }
})
</script>

<style scoped>
.resume-editor-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
}

.header-right {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.editor-layout {
  height: calc(100vh - 140px);
}

.resume-tabs {
  height: 100%;
}

.resume-tabs :deep(.el-tabs__content) {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.form-section {
  max-width: 800px;
  margin: 0 auto;
}

.item-card {
  margin-bottom: 16px;
}

.item-actions {
  margin-top: 16px;
  text-align: right;
}

.skills-input {
  display: flex;
  gap: 12px;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.photo-field {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.photo-preview {
  width: 110px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
}

.preview-layout {
  padding: 20px;
}

.preview-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.resume-preview {
  padding: 40px;
}

.resume-preview :deep(.section) {
  margin-bottom: 24px;
}

.resume-preview :deep(.section h2) {
  font-size: 18px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
  margin-bottom: 12px;
}

.resume-preview :deep(.item) {
  margin-bottom: 16px;
}

.resume-preview :deep(.item-header) {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.resume-preview :deep(.item-title) {
  font-weight: bold;
  color: #333;
}

.resume-preview :deep(.item-date) {
  color: #999;
  font-size: 14px;
}

.resume-preview :deep(.item-subtitle) {
  color: #666;
  font-size: 14px;
  margin-bottom: 4px;
}

.resume-preview :deep(.item-content) {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.resume-preview :deep(.skills) {
  color: #666;
}
</style>
