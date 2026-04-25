<template>
  <div class="templates-container">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <div class="brand-mark">R</div>
          <div class="header-copy">
            <div class="header-inline">
              <div class="step-chip">Step 1 / Template</div>
              <h2>创建简历</h2>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button class="header-btn" :icon="ArrowLeft" @click="$router.push('/')">返回首页</el-button>
        </div>
      </el-header>

      <el-main class="templates-main">
        <div class="main-layout">
<aside class="sidebar">
  <PopularSidebar @select="handleSidebarSelect" />
</aside>
          <section v-loading="loading" class="gallery-section">
          <div v-if="pagedTemplates.length > 0" class="templates-grid">
            <article
              v-for="template in pagedTemplates"
              :key="template.id"
              class="template-card"
              :class="{ selected: selectedTemplate?.id === template.id }"
              @click="selectTemplate(template)"
            >
              <div class="template-card-head">
                <span class="template-order">#{{ template.id }}</span>
                <span class="template-usage">已使用 {{ template.usage_count }} 次</span>
              </div>

            <div class="template-thumbnail">
            <iframe class="template-preview" :srcdoc="template.html_content" frameborder="0" scrolling="no" tabindex="-1"></iframe>
          </div>

              <div class="template-info">
                <div class="template-title-row">
                  <h3>{{ template.name }}</h3>
                  <span v-if="selectedTemplate?.id === template.id" class="selected-text">已选中</span>
                </div>
                <p>{{ template.description || '暂无描述' }}</p>
              </div>

              <div class="template-card-foot">
                <el-button
                  size="small"
                  type="primary"
                  :plain="selectedTemplate?.id !== template.id"
                  @click.stop="selectTemplate(template)"
                >
                  {{ selectedTemplate?.id === template.id ? '当前选择' : '选择模板' }}
                </el-button>
              </div>

              <div v-if="selectedTemplate?.id === template.id" class="selected-badge">
                <el-icon><Check /></el-icon>
              </div>
            </article>
          </div>

          <div v-if="!loading && templates.length === 0" class="empty-state">
            <el-empty description="暂无可用模板">
              <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
            </el-empty>
          </div>

          <div v-if="templates.length > pageSize" class="pagination-panel">
            <el-pagination
              :current-page="currentPage"
              :page-size="pageSize"
              :total="templates.length"
              layout="prev, pager, next"
              @current-change="handlePageChange"
            />
          </div>
        </section>
        </div>

        <div v-if="selectedTemplate" class="action-bar">
          <div class="action-bar-inner">
            <div class="action-summary">
              <span>已选择模板</span>
              <strong>{{ selectedTemplate.name }}</strong>
            </div>
            <el-button type="primary" size="large" @click="useTemplate">
              下一步，填写简历内容
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '@/stores/resume'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Check } from '@element-plus/icons-vue'
import api from '@/api'
import PopularSidebar from '@/components/PopularSidebar.vue'

const router = useRouter()
const resumeStore = useResumeStore()

const templates = ref([])
const loading = ref(false)
const selectedTemplate = ref(resumeStore.selectedTemplate || null)
const currentPage = ref(1)
const pageSize = 6

const pagedTemplates = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return templates.value.slice(start, start + pageSize)
})
// 👇 新增：处理侧边栏传过来的点击事件
const handleSidebarSelect = (id) => {
  // 1. 在全部模板列表里找到对应的那个模板
  const matched = templates.value.find(t => t.id === id)

  if (matched) {
    // 2. 选中它（底部会弹出下一步的确认条）
    selectTemplate(matched)

    // 3. 自动计算它在第几页，并翻页过去
    const selectedIndex = templates.value.findIndex(t => t.id === id)
    currentPage.value = Math.floor(selectedIndex / pageSize) + 1

    // 4. 平滑滚动到页面顶部
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } else {
    ElMessage.warning('模板加载中，请稍候...')
  }
}
const fetchTemplates = async () => {
  loading.value = true
  try {
    const response = await api.get('/templates/')
    templates.value = response.data.results || response.data

    if (selectedTemplate.value) {
      const matched = templates.value.find(item => item.id === selectedTemplate.value.id)
      if (matched) {
        selectedTemplate.value = matched
        const selectedIndex = templates.value.findIndex(item => item.id === matched.id)
        currentPage.value = Math.floor(selectedIndex / pageSize) + 1
      }
    }
  } catch (error) {
    ElMessage.error('获取模板列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const selectTemplate = (template) => {
  selectedTemplate.value = template
  resumeStore.setTemplate(template)
}

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const useTemplate = () => {
  if (!selectedTemplate.value) {
    return
  }
  router.push('/resume')
}

onMounted(() => {
  fetchTemplates()
})
</script>

<style scoped>
.templates-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.12), transparent 26%),
    radial-gradient(circle at top right, rgba(245, 158, 11, 0.14), transparent 22%),
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-right {
  display: flex;
  align-items: center;
}

.brand-mark {
  width: 46px;
  height: 46px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2563eb, #f59e0b);
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 16px 30px rgba(37, 99, 235, 0.2);
}

.header-copy {
  display: flex;
  align-items: center;
}

.header-inline {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-copy h2 {
  margin: 0;
  font-size: 26px;
  color: #0f172a;
  line-height: 1;
}

.step-chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: #e7efff;
  color: #3154b6;
  font-size: 12px;
  letter-spacing: 1px;
  line-height: 1;
}

.header-btn {
  border-radius: 999px;
}

.templates-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 24px 120px;
}

.main-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
}

.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.gallery-section {
  margin-top: 0;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}

.template-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.07);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  cursor: pointer;
}

.template-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 22px 44px rgba(15, 23, 42, 0.12);
}

.template-card.selected {
  border-color: #2563eb;
  box-shadow: 0 22px 48px rgba(37, 99, 235, 0.16);
}

.template-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 18px 0;
  color: #94a3b8;
  font-size: 12px;
}

.template-thumbnail {
  height: 190px;
  margin: 14px 18px 0;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid #edf2f7;
  background: #ffffff;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.8);
}

.template-preview {
  width: 1000px;
  height: 720px;
  transform: scale(0.19);
  transform-origin: top left;
  pointer-events: none;
  background: #ffffff;
}

.template-info {
  padding: 14px 18px 10px;
}

.template-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.template-info h3 {
  margin: 0;
  font-size: 19px;
  color: #111827;
}

.selected-text {
  color: #2563eb;
  font-size: 12px;
  white-space: nowrap;
}

.template-info p {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 13px;
  line-height: 1.55;
  min-height: 40px;
}

.template-card-foot {
  display: flex;
  justify-content: flex-end;
  padding: 0 18px 14px;
}

.selected-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: #2563eb;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.24);
}

.pagination-panel {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 26px;
  padding: 14px 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.06);
}

.empty-state {
  padding: 80px 20px;
  text-align: center;
}

.action-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 14px 24px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 -16px 34px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
}

.action-bar-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  padding: 10px 16px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.86), rgba(255, 247, 237, 0.86));
  border: 1px solid rgba(226, 232, 240, 0.9);
}

.action-summary {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #64748b;
}

.action-summary strong {
  color: #0f172a;
  font-size: 18px;
}

@media (max-width: 1100px) {
  .main-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .templates-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .header {
    padding: 0 14px;
  }

  .header-right {
    display: none;
  }

  .header-inline {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .templates-main {
    padding: 18px 14px 120px;
  }

  .templates-grid {
    grid-template-columns: 1fr;
  }

  .pagination-panel {
    justify-content: center;
  }

  .action-bar-inner {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
