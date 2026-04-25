<template>
  <div class="register-page">
    <div class="register-shell">
      <section class="register-panel">
        <div class="register-panel-head">
          <div class="head-badge">Create Account</div>
          <h2>创建你的账号</h2>
          <p>注册后即可开始选择模板、填写内容并保存历史简历。</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" label-width="0" class="register-form" @keyup.enter="handleRegister">
          <div class="form-grid">
            <el-form-item prop="username" class="full-row">
              <el-input v-model="form.username" size="large" placeholder="请输入用户名">
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="email" class="full-row">
              <el-input v-model="form.email" size="large" placeholder="请输入邮箱">
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="phone" class="full-row">
              <el-input v-model="form.phone" size="large" placeholder="请输入手机号">
                <template #prefix>
                  <el-icon><Phone /></el-icon>
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

            <el-form-item prop="password2">
              <el-input v-model="form.password2" type="password" size="large" placeholder="请确认密码" show-password>
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </div>

          <div class="register-actions">
            <el-button class="ghost-btn" @click="router.push('/login')">返回登录</el-button>
            <el-link type="primary" @click="router.push('/')">先回首页</el-link>
          </div>

          <el-button class="submit-btn" type="primary" size="large" :loading="loading" @click="handleRegister">
            注册账号
          </el-button>
        </el-form>
      </section>

      <section class="register-showcase">
        <div class="showcase-header">
          <div class="brand-mark">R</div>
          <div>
            <h1>简历在线生成</h1>
            <p>从模板出发，快速生成更适合投递的简历内容。</p>
          </div>
        </div>

        <div class="showcase-stack">
          <div class="stack-card stack-primary">
            <span>第一步</span>
            <strong>选择模板</strong>
          </div>
          <div class="stack-card">
            <span>第二步</span>
            <strong>填写简历</strong>
          </div>
          <div class="stack-card">
            <span>第三步</span>
            <strong>保存与导出</strong>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock, Message, Phone, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  password2: '',
  role: 'user'
})

const validatePass2 = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 位', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    await authStore.register({
      username: form.username,
      email: form.email,
      phone: form.phone,
      password: form.password,
      password2: form.password2,
      role: form.role
    })
    ElMessage.success('注册成功')
    router.push('/')
  } catch (error) {
    const msg = error.response?.data?.password?.[0] || error.response?.data?.username?.[0] || '注册失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  background:
    radial-gradient(circle at top left, rgba(250, 204, 21, 0.14), transparent 24%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.18), transparent 24%),
    linear-gradient(180deg, #f7f9fc 0%, #edf2f8 100%);
}

.register-shell {
  width: min(1160px, 100%);
  min-height: 720px;
  display: grid;
  grid-template-columns: 0.95fr 1.05fr;
  overflow: hidden;
  border-radius: 34px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.12);
}

.register-panel {
  padding: 44px 42px 38px;
  border-right: 1px solid rgba(226, 232, 240, 0.9);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.6), transparent 30%),
    linear-gradient(180deg, #fbfdff 0%, #f4f8fd 100%);
}

.head-badge {
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

.register-panel-head h2 {
  margin: 18px 0 0;
  font-size: 36px;
  line-height: 1.12;
  color: #0f172a;
}

.register-panel-head p {
  margin: 12px 0 0;
  color: #64748b;
  line-height: 1.8;
}

.register-form {
  margin-top: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 16px;
}

.full-row {
  grid-column: 1 / -1;
}

.register-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.register-form :deep(.el-input__wrapper) {
  min-height: 52px;
  border-radius: 16px;
  background: #f8fafc;
  box-shadow: inset 0 0 0 1px #dce5f1;
}

.register-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: inset 0 0 0 1px #93c5fd, 0 0 0 4px rgba(147, 197, 253, 0.18);
}

.register-form :deep(.el-input__inner) {
  font-size: 15px;
}

.register-actions {
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

.register-showcase {
  position: relative;
  padding: 44px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.4), transparent 24%),
    linear-gradient(160deg, #eef5ff 0%, #fff8ef 100%);
}

.showcase-header {
  display: flex;
  align-items: center;
  gap: 16px;
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

.showcase-header h1 {
  margin: 0;
  font-size: 38px;
  line-height: 1.12;
  color: #0f172a;
}

.showcase-header p {
  margin: 10px 0 0;
  max-width: 420px;
  color: #5b6b7f;
  font-size: 15px;
  line-height: 1.8;
}

.showcase-stack {
  display: grid;
  gap: 16px;
  margin-top: 52px;
}

.stack-card {
  padding: 22px 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: inset 0 0 0 1px rgba(226, 232, 240, 0.9);
}

.stack-card span {
  display: block;
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
}

.stack-card strong {
  font-size: 24px;
  color: #0f172a;
}

.stack-primary {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(59, 130, 246, 0.82));
  box-shadow: 0 22px 50px rgba(37, 99, 235, 0.16);
}

.stack-primary span,
.stack-primary strong {
  color: #f8fbff;
}

@media (max-width: 920px) {
  .register-shell {
    grid-template-columns: 1fr;
  }

  .register-panel {
    border-right: 0;
    border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  }

  .showcase-stack {
    margin-top: 30px;
  }
}

@media (max-width: 640px) {
  .register-page {
    padding: 14px;
  }

  .register-shell {
    min-height: auto;
    border-radius: 26px;
  }

  .register-panel,
  .register-showcase {
    padding: 26px 22px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .register-panel-head h2,
  .showcase-header h1 {
    font-size: 30px;
  }

  .register-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
