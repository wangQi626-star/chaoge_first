<template>
  <div class="history-container">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button :icon="ArrowLeft" @click="$router.push('/')">返回</el-button>
          <div>
            <h2>历史记录</h2>
            <p>查看你保存过的简历，并继续编辑、下载或生成 AI 职业建议。</p>
          </div>
        </div>

        <el-button type="primary" @click="$router.push('/templates')">创建简历</el-button>
      </el-header>

      <el-main class="history-main">
        <section class="history-summary">
          <div class="summary-card">
            <span>总简历数</span>
            <strong>{{ total }}</strong>
          </div>
          <div class="summary-card">
            <span>本页展示</span>
            <strong>{{ resumes.length }}</strong>
          </div>
          <div class="summary-card summary-action" @click="$router.push('/templates')">
            <span>下一步</span>
            <strong>继续创建新简历</strong>
          </div>
        </section>

        <div v-loading="loading" class="history-card">
          <el-table :data="resumes" style="width: 100%" @row-click="editResume">
            <el-table-column prop="title" label="简历标题" min-width="220">
              <template #default="{ row }">
                <div class="resume-title">
                  <span>{{ row.title }}</span>
                  <el-tag v-if="row.status === 'generated'" type="success" size="small">已生成</el-tag>
                  <el-tag v-else-if="row.status === 'failed'" type="danger" size="small">失败</el-tag>
                  <el-tag v-else type="info" size="small">草稿</el-tag>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="template_name" label="模板" min-width="140" />

            <el-table-column label="创建时间" width="190">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>

            <el-table-column label="更新时间" width="190">
              <template #default="{ row }">
                {{ formatDate(row.updated_at) }}
              </template>
            </el-table-column>

            <el-table-column label="操作" width="380" fixed="right">
              <template #default="{ row }">
                <div class="action-group">
                  <el-button type="primary" size="small" @click.stop="editResume(row)">编辑</el-button>
                  <el-button type="warning" size="small" plain @click.stop="analyzeCareer(row)">AI建议</el-button>
                  <el-button
                    v-if="row.status === 'generated'"
                    type="success"
                    size="small"
                    @click.stop="downloadPdf(row)"
                  >
                    下载
                  </el-button>
                  <el-button type="success" size="small" plain @click.stop="shareResume(row)">分享</el-button>
                  <el-button type="danger" size="small" @click.stop="deleteResume(row)">删除</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="!loading && resumes.length === 0" class="empty-state">
            <el-empty description="还没有简历记录">
              <el-button type="primary" @click="$router.push('/templates')">立即创建简历</el-button>
            </el-empty>
          </div>

          <div v-if="resumes.length > 0" class="pagination">
            <el-pagination
              v-model:current-page="currentPage"
              :page-size="pageSize"
              :total="total"
              layout="total, prev, pager, next"
              @current-change="fetchResumes"
            />
          </div>
        </div>
      </el-main>
    </el-container>

    <ShareDialog v-model="showShareDialog" :share-url="shareUrl" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'
import ShareDialog from '@/components/ShareDialog.vue'

const router = useRouter()

const resumes = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showShareDialog = ref(false)
const shareUrl = ref('')

const fetchResumes = async (page = 1) => {
  loading.value = true
  try {
    const response = await api.get(`/resumes/?page=${page}`)
    resumes.value = response.data.results || response.data
    total.value = response.data.count || resumes.value.length
  } catch (error) {
    ElMessage.error('获取历史记录失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const editResume = (row) => {
  router.push(`/resume/${row.id}`)
}

const analyzeCareer = (row) => {
  router.push(`/career-advice/${row.id}`)
}

const downloadPdf = async (row) => {
  try {
    const response = await api.get(`/resumes/${row.id}/download/`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${row.title}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载失败: ' + (error.response?.data?.error || error.message))
  }
}

const deleteResume = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这份简历吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await api.delete(`/resumes/${row.id}/`)
    ElMessage.success('删除成功')
    fetchResumes(currentPage.value)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const shareResume = async (row) => {
  try {
    const response = await api.post(`/resumes/${row.id}/share/`)
    shareUrl.value = response.data.share_url
    showShareDialog.value = true
  } catch (error) {
    ElMessage.error('生成分享链接失败')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchResumes()
})
</script>

<style scoped>
.history-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 28%),
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h2 {
  margin: 0;
  font-size: 24px;
  color: #111827;
}

.header-left p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
}

.history-main {
  max-width: 1240px;
  margin: 0 auto;
  padding: 28px 24px 40px;
}

.history-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 22px;
}

.summary-card {
  padding: 22px 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 34px rgba(15, 23, 42, 0.08);
}

.summary-card span {
  display: block;
  color: #64748b;
  font-size: 13px;
  margin-bottom: 10px;
}

.summary-card strong {
  font-size: 28px;
  color: #0f172a;
}

.summary-action {
  cursor: pointer;
  background: linear-gradient(135deg, #eff6ff, #f8fbff);
}

.history-card {
  padding: 18px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.08);
}

.resume-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.empty-state {
  padding: 70px 20px;
  text-align: center;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 22px;
}

.el-table {
  cursor: pointer;
}

.el-table :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.el-table :deep(th.el-table__cell) {
  background: #f8fafc;
  color: #475569;
}

.el-table :deep(.el-table__row) {
  cursor: pointer;
}

@media (max-width: 900px) {
  .history-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .header {
    padding: 0 14px;
  }

  .history-main {
    padding: 18px 14px 32px;
  }
}
</style>
