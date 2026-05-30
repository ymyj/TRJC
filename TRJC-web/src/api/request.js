import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: 'http://localhost:8000/trjcai', // 服务器地址：https://xx7x.star7.cn:8090/trjcai/
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      if (router.currentRoute.path !== '/login') {
        router.push('/login')
      }
    }
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api
