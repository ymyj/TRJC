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

export function assignPlot(taskId, plotId, data) {
  return api.post(`/api/tasks/${taskId}/plots/${plotId}/assign`, data)
}

export function publishTask(id) {
  return api.post(`/api/tasks/${id}/publish`)
}

export function uploadAttachment(taskId, file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post(`/api/tasks/${taskId}/attachments`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function getAttachments(taskId) {
  return api.get(`/api/tasks/${taskId}/attachments`)
}

export function deleteAttachment(attachmentId) {
  return api.delete(`/api/attachments/${attachmentId}`)
}

export function downloadAttachment(attachmentId) {
  return `${import.meta.env.VITE_API_BASE_URL || 'https://xx7x.star7.cn:8090/trjcai/'}/api/attachments/${attachmentId}/download`
}
