<template>
  <div class="login-page">
    <div class="login-header">
      <div class="logo">耕地质量监测</div>
      <div class="subtitle">移动端数据采集系统</div>
    </div>

    <div class="login-form">
      <van-field
        v-model="form.username"
        placeholder="请输入手机号"
        type="text"
        class="form-input"
      />

      <van-field
        v-model="form.password"
        placeholder="请输入密码"
        type="password"
        class="form-input"
      />

      <van-button
        type="primary"
        block
        class="login-btn"
        :loading="loading"
        loading-text="登录中..."
        @click="handleLogin"
      >
        登 录
      </van-button>

      <div class="login-tip">默认密码: 123456</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

const router = useRouter()
const loading = ref(false)
const errorMsg = ref('')

const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    errorMsg.value = '请填写手机号和密码'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const res = await login(form)
    if (res.data.code === 200) {
      const { token, user } = res.data.data
      localStorage.setItem('token', token)
      localStorage.setItem('userInfo', JSON.stringify(user))
      localStorage.setItem('currentUserId', user.ID)
      router.push('/')
    } else {
      errorMsg.value = res.data.msg || '登录失败'
    }
  } catch (err) {
    if (err.response && err.response.status === 401) {
      errorMsg.value = '用户名或密码错误'
    } else {
      errorMsg.value = '登录失败，请检查网络连接'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px 20px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.login-form {
  width: 100%;
  max-width: 360px;
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.form-input {
  margin-bottom: 16px;
}

.login-btn {
  margin-top: 24px;
  height: 48px;
  font-size: 16px;
  border-radius: 24px;
}

.login-tip {
  text-align: center;
  margin-top: 20px;
  font-size: 12px;
  color: #999;
}
</style>
