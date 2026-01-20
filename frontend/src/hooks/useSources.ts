import { useQuery } from '@tanstack/react-query'
import { sourcesApi } from '../api/sources'

export const useSources = () => {
  return useQuery({
    queryKey: ['sources'],
    queryFn: () => sourcesApi.getSources(),
  })
}
