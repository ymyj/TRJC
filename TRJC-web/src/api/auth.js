import api from './request'

export function login(data) {
  return api.post('/api/auth/login', data, {
    headers: {
      'X-Login-Source': 'web'
    }
  })
}

export function logout() {
  return api.post('/api/auth/logout')
}

export function refreshToken() {
  return api.post('/api/auth/refresh')
}
