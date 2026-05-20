import api from './request'

export function getPersonnelList(params) {
  return api.get('/api/personnel', { params })
}

export function getPersonnelOptions() {
  return api.get('/api/personnel/options')
}

export function getPersonnelForAssignment(params) {
  return api.get('/api/personnel/for-assignment', { params })
}

export function createPersonnel(data) {
  return api.post('/api/personnel', data)
}

export function updatePersonnel(id, data) {
  return api.put(`/api/personnel/${id}`, data)
}

export function deletePersonnel(id) {
  return api.delete(`/api/personnel/${id}`)
}

export function getPersonnelDetail(id) {
  return api.get(`/api/personnel/${id}`)
}
