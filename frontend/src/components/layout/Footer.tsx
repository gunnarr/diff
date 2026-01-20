import { useQuery } from '@tanstack/react-query'
import { api } from '../../api/client'

interface Stats {
  total_articles: number
  total_versions: number
  articles_with_changes: number
  total_sources: number
  active_sources: number
}

export const Footer = () => {
  const { data: stats } = useQuery<Stats>({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await api.get('/stats')
      return response.data
    },
    refetchInterval: 30000,
  })

  if (!stats) return null

  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {stats.total_articles}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Totalt artiklar</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {stats.total_versions}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Totalt versioner</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
              {stats.articles_with_changes}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Med ändringar</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {stats.active_sources}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Aktiva källor</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">
              {stats.total_sources}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Totalt källor</div>
          </div>
        </div>
        <div className="text-center mt-4 text-xs text-gray-500 dark:text-gray-400">
          Spårar ändringar i svenska nyhetsartiklar
        </div>
      </div>
    </footer>
  )
}
