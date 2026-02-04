import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// Portfolio API
export const portfolioAPI = {
  getAll: () => api.get('/portfolios'),
  create: (data) => api.post('/portfolios', data),
  getById: (id) => api.get(`/portfolios/${id}`),
  update: (id, data) => api.put(`/portfolios/${id}`, data),
  delete: (id) => api.delete(`/portfolios/${id}`),
  getRealtimeStats: (id) => api.get(`/portfolios/${id}/realtime`),
  getHistoryStats: (id, days = 30) => api.get(`/portfolios/${id}/history`, { params: { days } })
}

// Holding API
export const holdingAPI = {
  getByPortfolio: (portfolioId) => api.get(`/portfolios/${portfolioId}/holdings`),
  create: (portfolioId, data) => api.post(`/portfolios/${portfolioId}/holdings`, data),
  batchCreate: (portfolioId, holdings) => api.post(`/portfolios/${portfolioId}/holdings/batch`, { holdings }),
  update: (id, data) => api.put(`/holdings/${id}`, data),
  delete: (id) => api.delete(`/holdings/${id}`)
}

// OCR API
export const ocrAPI = {
  uploadFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/ocr/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 300000  // OCR识别需要更长时间，设置5分钟超时
    })
  },
  uploadBase64: (image) => api.post('/ocr/upload-base64', { image }, { timeout: 300000 })
}

export default api
