import api from './request'

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
