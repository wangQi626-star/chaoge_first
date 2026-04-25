<template>
  <div class="career-page">
    <div class="career-shell">
      <section class="hero-card">
        <div class="hero-copy">
          <div class="hero-kicker">AI Career Advisor</div>
          <h1>职业发展建议</h1>
          <p>
            基于你的简历内容，生成更聚焦的职业规划、技能提升方向和岗位推荐。
          </p>

          <div class="meta-list">
            <span>{{ resume.title || '未命名简历' }}</span>
            <span v-if="resume.name">{{ resume.name }}</span>
            <span v-if="resume.position">{{ resume.position }}</span>
            <span v-if="resume.template_name">{{ resume.template_name }}</span>
          </div>

          <div v-if="resume.skills?.length" class="skill-tags">
            <span v-for="skill in resume.skills" :key="skill">{{ skill }}</span>
          </div>
        </div>

        <div class="hero-actions">
          <el-button :icon="ArrowLeft" @click="router.push('/history')">返回历史</el-button>
          <el-button @click="router.push(`/resume/${route.params.id}`)">继续编辑</el-button>
          <el-button type="primary" :loading="loading" @click="fetchAdvice(true)">重新生成</el-button>
        </div>
      </section>

      <el-alert
        v-if="error"
        :title="error"
        type="error"
        show-icon
        :closable="false"
        class="error-alert"
      />

      <section class="advice-section">
        <div v-if="loading && !hasAdvice" class="advice-grid loading-grid">
          <div v-for="index in 3" :key="index" class="advice-card skeleton-card" />
        </div>

        <div v-else-if="hasAdvice" class="advice-grid">
          <article v-for="card in adviceCards" :key="card.key" class="advice-card">
            <div class="card-label">{{ card.label }}</div>
            <h2>{{ card.data.title }}</h2>
            <p>{{ card.data.description }}</p>
            <ul>
              <li v-for="action in card.data.actions" :key="action">{{ action }}</li>
            </ul>
          </article>
        </div>

        <el-empty v-else description="暂未生成职业建议，可点击重新生成" />
      </section>

      <section class="jobs-panel">
        <div class="jobs-head">
          <div>
            <div class="jobs-kicker">Recommended Roles</div>
            <h2>推荐工作</h2>
          </div>
          <span v-if="advice.analyzed_at" class="analyzed-at">生成时间：{{ formatDate(advice.analyzed_at) }}</span>
        </div>

        <div v-if="loading && !jobRecommendations.length" class="jobs-grid">
          <div v-for="index in 4" :key="index" class="job-card skeleton-card" />
        </div>

        <div v-else-if="jobRecommendations.length" class="jobs-grid">
          <article v-for="job in jobRecommendations" :key="`${job.title}-${job.match_score}`" class="job-card">
            <div class="job-top">
              <div>
                <div class="job-title">{{ job.title }}</div>
                <div class="job-reason">{{ job.reason }}</div>
              </div>
              <div class="score-badge">{{ job.match_score }}%</div>
            </div>

            <div class="job-preparation">
              <span>建议准备</span>
              <p>{{ job.preparation }}</p>
            </div>

            <div v-if="job.keywords?.length" class="job-tags">
              <span v-for="keyword in job.keywords" :key="keyword">{{ keyword }}</span>
            </div>
          </article>
        </div>

        <el-empty v-else description="暂未生成岗位推荐，可点击重新生成" />
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const resume = ref({
  title: '',
  name: '',
  position: '',
  template_name: '',
  skills: []
})
const advice = ref({
  short_term_goal: { title: '', description: '', actions: [] },
  skill_suggestions: { title: '', description: '', actions: [] },
  long_term_plan: { title: '', description: '', actions: [] },
  job_recommendations: [],
  analyzed_at: ''
})

const hasAdvice = computed(() => {
  return advice.value.short_term_goal?.title || advice.value.skill_suggestions?.title || advice.value.long_term_plan?.title
})

const adviceCards = computed(() => [
  {
    key: 'short',
    label: '短期目标（1年内）',
    data: advice.value.short_term_goal || { title: '', description: '', actions: [] }
  },
  {
    key: 'skill',
    label: '技能提升建议',
    data: advice.value.skill_suggestions || { title: '', description: '', actions: [] }
  },
  {
    key: 'long',
    label: '长期职业规划（3-5年）',
    data: advice.value.long_term_plan || { title: '', description: '', actions: [] }
  }
])

const jobRecommendations = computed(() => advice.value.job_recommendations || [])

const formatError = (err) => {
  if (err?.code === 'ECONNABORTED' || String(err?.message || '').includes('timeout')) {
    return 'AI 分析耗时较长，请稍后重试'
  }
  const data = err?.response?.data
  if (data?.error) return data.error
  if (data?.detail) return data.detail
  return err.message || '生成职业建议失败'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchResume = async () => {
  const response = await api.get(`/resumes/${route.params.id}/`)
  const data = response.data || {}
  const personal = data.resume_data?.personal || {}
  resume.value = {
    title: data.title || '',
    name: personal.name || '',
    position: personal.position || '',
    template_name: data.template_name || data.template_detail?.name || '',
    skills: data.resume_data?.skills || []
  }
}

const fetchAdvice = async (showSuccess = false) => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.post(`/resumes/${route.params.id}/career_advice/`, null, {
      timeout: 90000
    })
    advice.value = response.data
    resume.value = response.data.resume || resume.value
    if (showSuccess) {
      ElMessage.success('职业建议已更新')
    }
  } catch (err) {
    error.value = formatError(err)
    if (showSuccess) {
      ElMessage.error(error.value)
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    await fetchResume()
  } catch (err) {
    error.value = formatError(err)
  }
  await fetchAdvice()
})
</script>

<style scoped>
.career-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(245, 158, 11, 0.16), transparent 28%),
    radial-gradient(circle at top right, rgba(14, 165, 233, 0.12), transparent 26%),
    linear-gradient(180deg, #fffdf8 0%, #f6f8fc 100%);
}

.career-shell {
  max-width: 1240px;
  margin: 0 auto;
  padding: 32px 24px 40px;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 28px;
  padding: 30px 32px;
  border-radius: 30px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 248, 235, 0.96));
  box-shadow: 0 24px 60px rgba(148, 163, 184, 0.18);
  border: 1px solid rgba(251, 191, 36, 0.16);
  margin-bottom: 24px;
}

.hero-copy {
  flex: 1;
}

.hero-kicker,
.jobs-kicker,
.card-label {
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #b45309;
}

.hero-copy h1 {
  margin: 12px 0 10px;
  font-size: 36px;
  line-height: 1.1;
  color: #0f172a;
}

.hero-copy p {
  max-width: 720px;
  margin: 0;
  font-size: 15px;
  line-height: 1.75;
  color: #64748b;
}

.meta-list,
.skill-tags,
.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.meta-list {
  margin-top: 18px;
}

.meta-list span,
.skill-tags span,
.job-tags span {
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 13px;
}

.meta-list span {
  background: rgba(255, 255, 255, 0.92);
  color: #334155;
  border: 1px solid rgba(226, 232, 240, 0.95);
}

.skill-tags {
  margin-top: 14px;
}

.skill-tags span {
  background: rgba(14, 165, 233, 0.08);
  color: #0f766e;
}

.hero-actions {
  width: 180px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-self: flex-start;
}

.hero-actions :deep(.el-button) {
  margin-left: 0;
}

.error-alert {
  margin-bottom: 24px;
  border-radius: 20px;
}

.advice-section {
  margin-bottom: 24px;
}

.advice-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.advice-card,
.job-card {
  position: relative;
  overflow: hidden;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 20px 45px rgba(148, 163, 184, 0.16);
}

.advice-card {
  padding: 24px;
}

.advice-card::before,
.job-card::before {
  content: '';
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #f59e0b, #0ea5e9);
}

.advice-card h2,
.jobs-head h2 {
  margin: 12px 0 10px;
  color: #0f172a;
}

.advice-card h2 {
  font-size: 22px;
  line-height: 1.35;
}

.advice-card p {
  margin: 0 0 16px;
  color: #64748b;
  line-height: 1.75;
}

.advice-card ul {
  margin: 0;
  padding-left: 18px;
  color: #334155;
  line-height: 1.8;
}

.jobs-panel {
  padding: 28px;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 24px 52px rgba(148, 163, 184, 0.16);
}

.jobs-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 22px;
}

.jobs-head h2 {
  font-size: 28px;
}

.analyzed-at {
  color: #94a3b8;
  font-size: 13px;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.job-card {
  padding: 24px;
}

.job-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
}

.job-title {
  font-size: 22px;
  font-weight: 600;
  color: #111827;
}

.job-reason {
  margin-top: 8px;
  color: #64748b;
  line-height: 1.75;
}

.score-badge {
  flex-shrink: 0;
  min-width: 72px;
  padding: 10px 12px;
  border-radius: 18px;
  background: linear-gradient(135deg, #fff7ed, #fef3c7);
  color: #b45309;
  text-align: center;
  font-weight: 700;
}

.job-preparation {
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #eef2f7;
}

.job-preparation span {
  display: inline-block;
  margin-bottom: 8px;
  font-size: 13px;
  color: #94a3b8;
}

.job-preparation p {
  margin: 0;
  line-height: 1.75;
  color: #334155;
}

.job-tags {
  margin-top: 18px;
}

.job-tags span {
  background: #f8fafc;
  color: #475569;
}

.skeleton-card {
  min-height: 230px;
  background:
    linear-gradient(90deg, rgba(241, 245, 249, 0.92) 25%, rgba(226, 232, 240, 0.8) 37%, rgba(241, 245, 249, 0.92) 63%);
  background-size: 400% 100%;
  animation: shimmer 1.4s ease infinite;
}

@keyframes shimmer {
  0% {
    background-position: 100% 0;
  }
  100% {
    background-position: 0 0;
  }
}

@media (max-width: 960px) {
  .hero-card {
    flex-direction: column;
  }

  .hero-actions {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
  }

  .advice-grid,
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .career-shell {
    padding: 20px 14px 28px;
  }

  .hero-card,
  .jobs-panel {
    padding: 22px 18px;
    border-radius: 24px;
  }

  .hero-copy h1 {
    font-size: 28px;
  }

  .jobs-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
