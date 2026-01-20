import { apiClient } from './client'
import type { PaginatedArticles, ArticleDetail, DiffResponse } from '../types'

export const articlesApi = {
  getArticles: async (params?: {
    source?: string
    has_changes?: boolean
    limit?: number
    offset?: number
  }): Promise<PaginatedArticles> => {
    const { data } = await apiClient.get('/articles', { params })
    return data
  },

  getArticle: async (id: number | string): Promise<ArticleDetail> => {
    const { data} = await apiClient.get(`/articles/${id}`)
    return data
  },

  getDiff: async (
    articleId: number,
    fromVersion: number,
    toVersion: number
  ): Promise<DiffResponse> => {
    const { data } = await apiClient.get(`/articles/${articleId}/diff`, {
      params: { from_version: fromVersion, to_version: toVersion },
    })
    return data
  },
}
