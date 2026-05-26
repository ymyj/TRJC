import api from './request'

export function getTaskList(params) {
  return api.get('/api/tasks', { params })
}

export function getTaskStats() {
  return api.get('/api/tasks/stats')
}

export function createTask(data) {
  return api.post('/api/tasks', data)
}

export function updateTask(id, data) {
  return api.put(`/api/tasks/${id}`, data)
}

export function deleteTask(id) {
  return api.delete(`/api/tasks/${id}`)
}

export function getTaskDetail(id) {
  return api.get(`/api/tasks/${id}`)
}

export function assignTask(id, data) {
  return api.post(`/api/tasks/${id}/assign`, data)
}

export function publishTask(id) {
  return api.post(`/api/tasks/${id}/publish`)
}
