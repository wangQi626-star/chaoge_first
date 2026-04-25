<template>
  <div class="home-container">
    <el-container>
      <el-header class="header">
        <div class="brand-block">
          <div class="brand-mark">R</div>
          <div>
            <h1>简历在线生成</h1>
            <p>从模板开始，完成一份更好看的简历</p>
          </div>
        </div>

        <div class="header-actions">
          <el-button class="ghost-btn" @click="$router.push('/history')">历史记录</el-button>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ authStore.user?.username || '用户' }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <section class="hero-panel">
          <div class="hero-copy">
            <div class="hero-badge">Resume Builder</div>
            <h2>创建简历，从选择模板开始。</h2>
            <p>
              先挑一个适合你的版式，再进入内容编辑。模板、配色、布局、头像形式都已经准备好，
              你只需要专注填写信息。
            </p>
            <div class="hero-actions">
              <el-button type="primary" size="large" @click="$router.push('/templates')">创建简历</el-button>
              <el-button size="large" @click="$router.push('/history')">查看历史记录</el-button>
            </div>
          </div>

          <div class="hero-preview">
            <div class="preview-stack preview-a">
              <div class="preview-tag">左侧栏</div>
              <div class="preview-title">湖蓝侧栏</div>
            </div>
            <div class="preview-stack preview-b">
              <div class="preview-tag">双栏布局</div>
              <div class="preview-title">靛青双栏</div>
            </div>
            <div class="preview-stack preview-c">
              <div class="preview-tag">圆形头像</div>
              <div class="preview-title">晴空圆卡</div>
            </div>
          </div>
        </section>

        <section class="feature-grid">
          <el-card class="feature-card feature-primary" @click="$router.push('/templates')">
            <div class="feature-icon"><el-icon :size="28"><Document /></el-icon></div>
            <h3>创建简历</h3>
            <p>第一步先选模板，再进入编辑页填写内容。</p>
          </el-card>

          <el-card class="feature-card" @click="$router.push('/history')">
            <div class="feature-icon"><el-icon :size="28"><Files /></el-icon></div>
            <h3>历史记录</h3>
            <p>查看、编辑、删除你已保存的简历内容。</p>
          </el-card>

          <el-card class="feature-card" @click="$router.push('/statistics')">
            <div class="feature-icon"><el-icon :size="28"><DataAnalysis /></el-icon></div>
            <h3>数据统计</h3>
            <p>查看简历使用情况和热门模板统计。</p>
          </el-card>

          <el-card class="feature-card" @click="$router.push('/template-editor')">
            <div class="feature-icon"><el-icon :size="28"><Edit /></el-icon></div>
            <h3>自定义模板</h3>
            <p>创建属于你自己的个性化简历模板。</p>
          </el-card>


        </section>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { User, Document, Files, MagicStick, DataAnalysis, Edit } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const handleCommand = (command) => {
  if (command === 'logout') {
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(250, 204, 21, 0.14), transparent 28%),
    radial-gradient(circle at top right, rgba(37, 99, 235, 0.12), transparent 24%),
    linear-gradient(180deg, #f7f9fc 0%, #eef2f7 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 28px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 12px 36px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2563eb, #f59e0b);
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.2);
}

.brand-block h1 {
  margin: 0;
  font-size: 24px;
  color: #0f172a;
}

.brand-block p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ghost-btn {
  border-radius: 999px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  background: #ffffff;
  cursor: pointer;
  color: #334155;
  box-shadow: inset 0 0 0 1px #e2e8f0;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 36px 24px 48px;
}

.hero-panel {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 28px;
  padding: 40px;
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 26px 60px rgba(15, 23, 42, 0.1);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: #e8eefc;
  color: #3154b6;
  font-size: 12px;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.hero-copy h2 {
  margin: 0;
  font-size: 44px;
  line-height: 1.15;
  color: #0f172a;
}

.hero-copy p {
  margin: 18px 0 0;
  font-size: 16px;
  line-height: 1.8;
  color: #475569;
  max-width: 620px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.hero-preview {
  position: relative;
  min-height: 360px;
}

.preview-stack {
  position: absolute;
  width: 220px;
  height: 220px;
  padding: 24px;
  border-radius: 28px;
  color: #ffffff;
  box-shadow: 0 22px 40px rgba(15, 23, 42, 0.14);
}

.preview-a {
  top: 0;
  left: 16px;
  background: linear-gradient(160deg, #22638c, #64a5c6);
}

.preview-b {
  top: 82px;
  right: 8px;
  background: linear-gradient(160deg, #4858a8, #8897ea);
}

.preview-c {
  left: 72px;
  bottom: 0;
  background: linear-gradient(160deg, #f59e0b, #f7c971);
}

.preview-tag {
  font-size: 12px;
  letter-spacing: 2px;
  opacity: 0.82;
  margin-bottom: 12px;
}

.preview-title {
  font-size: 28px;
  line-height: 1.2;
  font-weight: 700;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  margin-top: 28px;
}

.feature-card {
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.1);
}

.feature-primary {
  background: linear-gradient(180deg, #f8fbff 0%, #eef5ff 100%);
}

.static-card {
  cursor: default;
}

.static-card:hover {
  transform: none;
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eff6ff;
  color: #2563eb;
  margin-bottom: 18px;
}

.feature-card h3 {
  margin: 0 0 10px;
  color: #111827;
}

.feature-card p {
  margin: 0;
  color: #64748b;
  line-height: 1.7;
}

@media (max-width: 980px) {
  .hero-panel {
    grid-template-columns: 1fr;
  }

  .hero-preview {
    min-height: 300px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .header {
    padding: 0 14px;
  }

  .main-content {
    padding: 20px 14px 40px;
  }

  .hero-panel {
    padding: 26px 20px;
    border-radius: 24px;
  }

  .hero-copy h2 {
    font-size: 32px;
  }

  .preview-stack {
    width: 180px;
    height: 180px;
  }
}
</style>
