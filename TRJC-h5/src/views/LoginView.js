const LoginView = {
  name: 'LoginView',
  template: `
    <div class="login-page">
      <div class="login-top-decoration"></div>
      <div class="login-content">
        <div class="login-header">
          <div class="logo-icon">
            <van-icon name="bar-chart-o" size="36" color="#fff" />
          </div>
          <div class="logo-title">耕地质量监测</div>
          <div class="subtitle">移动端数据采集系统</div>
        </div>

        <div class="login-form">
          <div class="form-title">欢迎登录</div>
          
          <div class="input-group">
            <van-field
              v-model="form.username"
              placeholder="请输入用户名"
              type="text"
              class="form-input"
            />
          </div>

          <div class="input-group">
            <van-field
              v-model="form.password"
              placeholder="请输入密码"
              type="password"
              class="form-input"
            />
          </div>

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

        </div>
      </div>
    </div>
  `,
  setup() {
    const router = VueRouter.useRouter()
    const loading = Vue.ref(false)
    const errorMsg = Vue.ref('')

    const form = Vue.reactive({
      username: '',
      password: ''
    })

    const handleLogin = async () => {
      if (!form.username || !form.password) {
        errorMsg.value = '请填写用户名和密码'
        return
      }

      loading.value = true
      errorMsg.value = ''

      try {
        const res = await TRJC.api.login(form)
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

    return {
      form,
      loading,
      errorMsg,
      handleLogin
    }
  }
}

const LoginViewStyle = `
.login-page {
  min-height: 100vh;
  background: #F5F8FF;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.login-top-decoration {
  width: 100%;
  height: 220px;
  background: linear-gradient(135deg, #4A90E2 0%, #5BA3F5 50%, #7AB8F7 100%);
  border-radius: 0 0 32px 32px;
  position: relative;
}

.login-top-decoration::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 20px;
  background: #F5F8FF;
  border-radius: 20px 20px 0 0;
}

.login-content {
  width: 100%;
  max-width: 400px;
  padding: 0 20px;
  margin-top: -100px;
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.logo-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 16px rgba(74, 144, 226, 0.3);
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  color: #1A1A1A;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 13px;
  color: #999;
}

.login-form {
  width: 100%;
  background: #fff;
  border-radius: 20px;
  padding: 28px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.form-title {
  font-size: 18px;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 20px;
  text-align: center;
}

.input-group {
  margin-bottom: 12px;
}

.form-input {
  background: #F5F8FF;
  border-radius: 12px;
}

.login-btn {
  margin-top: 20px;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 24px;
  background: linear-gradient(135deg, #4A90E2 0%, #5BA3F5 100%);
  border: none;
}

.login-tip {
  text-align: center;
  margin-top: 16px;
  font-size: 12px;
  color: #999;
}
`;

export { LoginView, LoginViewStyle };