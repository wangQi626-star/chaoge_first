<template>
  <div class="statistics-container">
    <el-card class="stats-card">
      <template #header>
        <div class="header-row">
          <h2>数据统计</h2>
          <el-button @click="$router.push('/')">返回</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-box">
            <div class="stat-value">{{ resumeStats.total }}</div>
            <div class="stat-label">我的简历</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-box">
            <div class="stat-value">{{ templateStats.total }}</div>
            <div class="stat-label">可用模板</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-box">
            <div class="stat-value">{{ templateStats.total_usage }}</div>
            <div class="stat-label">总使用次数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-box">
            <div class="stat-value">{{ resumeStats.by_status?.generated || 0 }}</div>
            <div class="stat-label">已生成</div>
          </div>
        </el-col>
      </el-row>

      <el-divider />

      <h3>热门模板 TOP 5</h3>
      <el-table :data="templateStats.top_templates" style="width: 100%">
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="usage_count" label="使用次数" width="120" />
      </el-table>
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
// 【修改点 1】把原生 axios 换成封装好的 api
import api from '@/api'

const resumeStats = ref({ total: 0, by_status: {}, top_templates: [] })
const templateStats = ref({ total: 0, total_usage: 0, by_category: [], top_templates: [] })

const fetchStats = async () => {
  try {
    // 【修改点 2】使用 api.get 替代 axios.get，如果你封装的 api 不需要写 /api 前缀，可以把 /api 去掉，具体看你封装的逻辑。
    // 通常封装的 api baseURL 已经包含了 '/api'，所以这里我假设直接写具体的路由即可。
    // 如果你之前的页面都是写的完整 /api/...，那就保留 /api/resumes/statistics/
    const [resumeRes, templateRes] = await Promise.all([
      api.get('/resumes/statistics/'),
      api.get('/templates/statistics/')
    ])

    // 【修改点 3】注意：封装的 api 返回结构可能已经是 data 了，你需要根据实际情况调整。
    // 大多数项目封装 api 后，可以直接拿到数据，如果拿不到，就依然保留 .data
    resumeStats.value = resumeRes.data || resumeRes
    templateStats.value = templateRes.data || templateRes

  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-row h2 {
  margin: 0;
}

.stat-box {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  margin-top: 8px;
  color: #606266;
}
</style>
