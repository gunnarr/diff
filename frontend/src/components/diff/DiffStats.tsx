import type { DiffStats as DiffStatsType } from '../../types'

interface DiffStatsProps {
  stats: DiffStatsType
}

export const DiffStats = ({ stats }: DiffStatsProps) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Statistik</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center">
          <div className="text-3xl font-bold text-green-600 dark:text-green-400">
            +{stats.words_added}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Ord tillagda</div>
        </div>
        <div className="text-center">
          <div className="text-3xl font-bold text-red-600 dark:text-red-400">
            -{stats.words_removed}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Ord borttagna</div>
        </div>
        <div className="text-center">
          <div className={`text-3xl font-bold ${
            stats.net_change > 0 ? 'text-green-600 dark:text-green-400' :
            stats.net_change < 0 ? 'text-red-600 dark:text-red-400' :
            'text-gray-600 dark:text-gray-400'
          }`}>
            {stats.net_change > 0 ? '+' : ''}{stats.net_change}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Nettoförändring</div>
        </div>
        <div className="text-center">
          <div className={`text-3xl font-bold ${
            stats.title_changed ? 'text-yellow-600 dark:text-yellow-400' : 'text-gray-400 dark:text-gray-500'
          }`}>
            {stats.title_changed ? '✓' : '✗'}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Titel ändrad</div>
        </div>
      </div>
    </div>
  )
}
