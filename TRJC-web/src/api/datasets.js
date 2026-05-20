import api from './request'

export function getDatasetList(params) {
  return api.get('/api/datasets', { params })
}

export function getDatasetDetail(id) {
  return api.get(`/api/datasets/${id}`)
}

export function createDataset(data) {
  return api.post('/api/datasets', data)
}
