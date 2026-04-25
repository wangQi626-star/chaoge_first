<template>
  <div class="login-page">
    <div class="login-shell">
      <section class="login-showcase">
        <div class="showcase-badge">Resume Builder</div>
        <div class="showcase-brand">
          <div class="brand-mark">R</div>
          <div>
            <h1>简历在线生成</h1>
            <p>登录后继续创建简历、查看历史记录和导出内容。</p>
          </div>
        </div>

        <div class="showcase-panel">
          <div class="panel-card panel-main">
            <span>快速进入</span>
            <strong>创建简历</strong>
          </div>
          <div class="panel-card">
            <span>已保存内容</span>
            <strong>历史记录</strong>
          </div>
          <div class="panel-card">
            <span>多种版式</span>
            <strong>模板任选</strong>
          </div>
        </div>
      </section>

      <section class="login-panel">
        <div class="login-panel-head">
          <h2>欢迎回来</h2>
          <p>输入账号和密码，继续编辑你的简历内容。</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" label-width="0" class="login-form" @keyup.enter="handleLogin">
          <el-form-item prop="username">
            <el-input v-model="form.username" size="large" placeholder="请输入用户名">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" size="large" placeholder="请输入密码" show-password>
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <div class="login-actions">
            <el-button class="ghost-btn" @click="router.push('/')">返回首页</el-button>
            <el-link type="primary" @click="router.push('/register')">没有账号？立即注册</el-link>
          </div>

          <el-button class="submit-btn" type="primary" size="large" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    await authStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  background:
    radial-gradient(circle at top left, rgba(250, 204, 21, 0.16), transparent 26%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.16), transparent 24%),
    linear-gradient(180deg, #f7f9fc 0%, #edf2f8 100%);
}

.login-shell {
  width: min(1120px, 100%);
  min-height: 680px;
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  overflow: hidden;
  border-radius: 34px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.12);
}

.login-showcase {
  position: relative;
  padding: 42px 40px 34px;
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.42), transparent 30%),
    linear-gradient(160deg, #f7fbff 0%, #ebf3ff 52%, #fff7ed 100%);
  border-right: 1px solid rgba(226, 232, 240, 0.9);
}

.showcase-badge {
  display: inline-flex;
  align-items: center;
  padding: 7px 14px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.08);
  color: #3154b6;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.showcase-brand {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-top: 30px;
}

.brand-mark {
  width: 62px;
  height: 62px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2563eb, #f59e0b);
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  box-shadow: 0 20px 36px rgba(37, 99, 235, 0.18);
}

.showcase-brand h1 {
  margin: 0;
  font-size: 38px;
  line-height: 1.12;
  color: #0f172a;
}

.showcase-brand p {
  margin: 10px 0 0;
  max-width: 460px;
  color: #5b6b7f;
  font-size: 15px;
  line-height: 1.8;
}

.showcase-panel {
  margin-top: 64px;
  display: grid;
  gap: 16px;
}

.panel-card {
  padding: 22px 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: inset 0 0 0 1px rgba(226, 232, 240, 0.9);
  backdrop-filter: blur(8px);
}

.panel-card span {
  display: block;
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
}

.panel-card strong {
  font-size: 24px;
  color: #0f172a;
}

.panel-main {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(59, 130, 246, 0.82));
  box-shadow: 0 22px 50px rgba(37, 99, 235, 0.16);
}

.panel-main span,
.panel-main strong {
  color: #f8fbff;
}

.login-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 48px 48px 42px;
}

.login-panel-head h2 {
  margin: 0;
  font-size: 36px;
  line-height: 1.12;
  color: #0f172a;
}

.login-panel-head p {
  margin: 12px 0 0;
  color: #64748b;
  line-height: 1.8;
}

.login-form {
  margin-top: 34px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.login-form :deep(.el-input__wrapper) {
  min-height: 52px;
  border-radius: 16px;
  background: #f8fafc;
  box-shadow: inset 0 0 0 1px #dce5f1;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: inset 0 0 0 1px #93c5fd, 0 0 0 4px rgba(147, 197, 253, 0.18);
}

.login-form :deep(.el-input__inner) {
  font-size: 15px;
}

.login-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin: 8px 0 20px;
}

.ghost-btn {
  border-radius: 999px;
}

.submit-btn {
  width: 100%;
  min-height: 54px;
  border: 0;
  border-radius: 18px;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  box-shadow: 0 22px 44px rgba(37, 99, 235, 0.2);
}

@media (max-width: 920px) {
  .login-shell {
    grid-template-columns: 1fr;
  }

  .login-showcase {
    border-right: 0;
    border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  }

  .showcase-panel {
    margin-top: 30px;
  }
}

@media (max-width: 640px) {
  .login-page {
    padding: 14px;
  }

  .login-shell {
    min-height: auto;
    border-radius: 26px;
  }

  .login-showcase,
  .login-panel {
    padding: 26px 22px;
  }

  .showcase-brand {
    align-items: flex-start;
  }

  .showcase-brand h1,
  .login-panel-head h2 {
    font-size: 30px;
  }

  .login-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
