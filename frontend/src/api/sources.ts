import { apiClient } from './client'
import type { NewsSource } from '../types'

export const sourcesApi = {
  getSources: async (): Promise<NewsSource[]> => {
    const { data } = await apiClient.get('/sources')
    return data
  },
}
