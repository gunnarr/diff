import axios from 'axios'

// Use relative URL so Vite proxy can handle it (works on all devices)
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Export as 'api' for convenience
export const api = apiClient
