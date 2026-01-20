import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../api/articles'

export const useArticles = (params?: {
  source?: string
  has_changes?: boolean
  limit?: number
  offset?: number
}) => {
  return useQuery({
    queryKey: ['articles', params],
    queryFn: () => articlesApi.getArticles(params),
  })
}

export const useArticle = (id: number | string) => {
  return useQuery({
    queryKey: ['article', id],
    queryFn: () => articlesApi.getArticle(id),
    enabled: !!id,
  })
}

export const useDiff = (
  articleId: number,
  fromVersion: number,
  toVersion: number
) => {
  return useQuery({
    queryKey: ['diff', articleId, fromVersion, toVersion],
    queryFn: () => articlesApi.getDiff(articleId, fromVersion, toVersion),
    enabled: !!articleId && !!fromVersion && !!toVersion,
  })
}
