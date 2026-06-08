<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-circle bg-circle-1"></div>
      <div class="bg-circle bg-circle-2"></div>
      <div class="bg-lines bg-lines-1"></div>
      <div class="bg-lines bg-lines-2"></div>
    </div>

    <div class="login-card">
      <!-- Logo -->
      <div class="logo-wrapper">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="14" width="4" height="6" rx="1" fill="#409eff"/>
          <rect x="10" y="10" width="4" height="10" rx="1" fill="#409eff"/>
          <rect x="16" y="6" width="4" height="14" rx="1" fill="#409eff"/>
        </svg>
      </div>

      <h1 class="login-title">耕地质量监测管理系统</h1>
      <p class="login-subtitle">用户登录</p>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">公司</label>
          <div class="input-wrapper">
            <select
              class="form-select"
              v-model="form.gs"
              required
            >
              <option value="">请选择公司</option>
              <option v-for="gs in companyList" :key="gs" :value="gs">{{ gs }}</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">用户名</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#b4c0d4" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </span>
            <input
              type="text"
              class="form-input"
              v-model="form.username"
              placeholder="请输入用户名"
              required
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#b4c0d4" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <input
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              v-model="form.password"
              placeholder="请输入密码"
              required
            >
            <span class="toggle-password" @click="showPassword = !showPassword">
              <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="#b4c0d4" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="#b4c0d4" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </span>
          </div>
        </div>

        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { login, getCompanies } from '../api/auth'

const router = useRouter()

const form = reactive({
  gs: '',
  username: '',
  password: ''
})

const loading = ref(false)
const errorMsg = ref('')
const companyList = ref([])
const showPassword = ref(false)

// 加载公司列表
const fetchCompanies = async () => {
  try {
    const res = await getCompanies()
    if (res.data.code === 200) {
      companyList.value = res.data.data || []
    }
  } catch (err) {
    console.error('获取公司列表失败:', err)
  }
}

const handleLogin = async () => {
  if (!form.gs) {
    errorMsg.value = '请选择公司'
    return
  }
  if (!form.username || !form.password) {
    errorMsg.value = '请填写用户名和密码'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const res = await login(form)
    console.log('登录响应:', res.data)
    if (res.data.code === 200) {
      const { token, user } = res.data.data
      console.log('登录获取的用户信息:', user)
      localStorage.setItem('token', token)
      localStorage.setItem('userInfo', JSON.stringify(user))
      router.push('/')
    } else {
      errorMsg.value = res.data.msg || '登录失败'
    }
  } catch (err) {
    if (err.response && err.response.status === 401) {
      errorMsg.value = '用户名或密码错误'
    } else if (err.response && err.response.status === 403) {
      errorMsg.value = err.response.data.detail || '无权限登录'
    } else {
      errorMsg.value = '登录失败，请检查网络连接'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCompanies()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f5ff 0%, #e8edff 100%);
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}

/* ===== 背景装饰 ===== */
.bg-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
}

.bg-circle-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.08) 0%, transparent 70%);
  right: -200px;
  bottom: -200px;
}

.bg-circle-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.06) 0%, transparent 70%);
  left: -100px;
  top: -100px;
}

/* 线条装饰 */
.bg-lines {
  position: absolute;
  background: linear-gradient(
    135deg,
    transparent 0%,
    rgba(64, 158, 255, 0.04) 50%,
    transparent 100%
  );
}

.bg-lines-1 {
  width: 500px;
  height: 500px;
  top: -100px;
  right: -100px;
  border-radius: 50%;
}

.bg-lines-2 {
  width: 400px;
  height: 400px;
  bottom: -80px;
  left: -80px;
  border-radius: 50%;
}

/* ===== 登录卡片 ===== */
.login-card {
  position: relative;
  z-index: 1;
  width: 360px;
  padding: 36px 28px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}

/* ===== Logo ===== */
.logo-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.logo-icon {
  width: 40px;
  height: 40px;
}

/* ===== 标题 ===== */
.login-title {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #1d2129;
  margin: 0 0 6px;
}

.login-subtitle {
  text-align: center;
  font-size: 13px;
  color: #86909c;
  margin: 0 0 28px;
}

/* ===== 表单 ===== */
.login-form {
  width: 100%;
}

.form-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 6px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.input-icon svg {
  width: 16px;
  height: 16px;
}

.form-input {
  width: 100%;
  height: 40px;
  padding: 0 14px 0 38px;
  border: 1px solid #e5e6eb;
  border-radius: 6px;
  font-size: 13px;
  color: #1d2129;
  outline: none;
  transition: all 0.2s;
  background: #fff;
}

.form-input::placeholder {
  color: #c9cdd4;
}

.form-input:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.form-select {
  width: 100%;
  height: 40px;
  padding: 0 32px 0 12px;
  border: 1px solid #e5e6eb;
  border-radius: 6px;
  font-size: 13px;
  color: #1d2129;
  outline: none;
  transition: all 0.2s;
  background-color: #fff;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23c9cdd4' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

.form-select:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

/* 密码显示/隐藏按钮 */
.toggle-password {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px;
}

.toggle-password svg {
  width: 16px;
  height: 16px;
}

/* ===== 错误消息 ===== */
.error-msg {
  padding: 8px 12px;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 6px;
  color: #ff4d4f;
  font-size: 12px;
  margin-bottom: 16px;
}

/* ===== 登录按钮 ===== */
.login-btn {
  width: 100%;
  height: 40px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
}

.login-btn:hover {
  background: #66b1ff;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-btn:disabled:hover {
  background: #409eff;
}
</style>
