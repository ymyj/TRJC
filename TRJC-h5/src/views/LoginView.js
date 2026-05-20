import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

export default {
  name: 'LoginView',
  setup() {
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

    return { form, loading, errorMsg, handleLogin }
  },
  render() {
    return (
      <div class="login-page">
        <div class="login-header">
          <div class="logo">耕地质量监测</div>
          <div class="subtitle">移动端数据采集系统</div>
        </div>

        <div class="login-form">
          <div class="form-item">
            <input
              type="text"
              v-model={this.form.username}
              placeholder="请输入手机号"
              class="form-input"
            />
          </div>

          <div class="form-item">
            <input
              type="password"
              v-model={this.form.password}
              placeholder="请输入密码"
              class="form-input"
            />
          </div>

          {this.errorMsg && (
            <div class="error-msg">{this.errorMsg}</div>
          )}

          <button
            class="login-btn"
            onClick={this.handleLogin}
            disabled={this.loading}
          >
            {this.loading ? '登录中...' : '登 录'}
          </button>

          <div class="login-tip">默认密码: 123456</div>
        </div>
      </div>
    )
  }
}
