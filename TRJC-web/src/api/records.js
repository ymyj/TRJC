import api from './request'

export function getSurveyRecords(taskId) {
  return api.get(`/api/tasks/${taskId}/survey`)
}

export function createSurveyRecord(taskId, data) {
  return api.post(`/api/tasks/${taskId}/survey`, data)
}

export function updateSurveyRecord(taskId, recordId, data) {
  return api.put(`/api/tasks/${taskId}/survey/${recordId}`, data)
}

export function getSampleRecords(taskId) {
  return api.get(`/api/tasks/${taskId}/samples`)
}

export function createSampleRecord(taskId, data) {
  return api.post(`/api/tasks/${taskId}/samples`, data)
}

export function updateSampleRecord(taskId, recordId, data) {
  return api.put(`/api/tasks/${taskId}/samples/${recordId}`, data)
}
