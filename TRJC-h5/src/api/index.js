import api from './request'

export function login(data) {
  return api.post('/api/auth/login', data)
}

export function logout() {
  return api.post('/api/auth/logout')
}

export function getTaskList(params) {
  return api.get('/api/tasks', { params })
}

export function getTaskStats() {
  return api.get('/api/tasks/stats')
}

export function getTaskDetail(id) {
  return api.get(`/api/tasks/${id}`)
}

export function getSurveyRecords(taskId) {
  return api.get(`/api/tasks/${taskId}/survey`)
}

export function createSurveyRecord(taskId, data) {
  return api.post(`/api/tasks/${taskId}/survey`, data)
}

export function getSampleRecords(taskId) {
  return api.get(`/api/tasks/${taskId}/samples`)
}

export function createSampleRecord(taskId, data) {
  return api.post(`/api/tasks/${taskId}/samples`, data)
}

export function getTaskPlots(taskId, ryid) {
  const params = ryid ? { ryid } : {};
  return api.get(`/api/tasks/${taskId}/plots`, { params });
}
