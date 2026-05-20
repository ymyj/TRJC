import api from './request'

export function getPlotList(params) {
  return api.get('/api/plots', { params })
}

export function getPlotOptions() {
  return api.get('/api/plots/options')
}

export function createPlot(data) {
  return api.post('/api/plots', data)
}

export function updatePlot(id, data) {
  return api.put(`/api/plots/${id}`, data)
}

export function deletePlot(id) {
  return api.delete(`/api/plots/${id}`)
}

export function getPlotDetail(id) {
  return api.get(`/api/plots/${id}`)
}
