import { Link } from 'react-router-dom'
import type { ArticleListItem } from '../../types'
import { formatRelativeTime } from '../../utils/date'
import { generateArticleUrl } from '../../utils/slug'

interface ArticleCardProps {
  article: ArticleListItem
}

export const ArticleCard = ({ article }: ArticleCardProps) => {
  const hasChanges = article.version_count > 1

  // Generate SEO-friendly URL with date and slug
  const articleUrl = generateArticleUrl(article.first_seen_at, article.title)

  return (
    <Link
      to={articleUrl}
      className="block bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow p-4 sm:p-6"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-white mb-2 break-words">
            {article.title}
          </h3>
          <div className="space-y-1 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
              <span className="flex items-center">
                <svg className="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="break-words">Först upptäckt {formatRelativeTime(article.first_seen_at)}</span>
              </span>
              {article.latest_version && (
                <span className="whitespace-nowrap">
                  {article.latest_version.word_count} ord
                </span>
              )}
            </div>
            {hasChanges && article.last_modified_at && (
              <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                <span className="flex items-center text-yellow-700 dark:text-yellow-400">
                  <svg className="w-4 h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span className="break-words">Senast ändrad {formatRelativeTime(article.last_modified_at)}</span>
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 whitespace-nowrap">
                  {article.version_count} versioner
                </span>
              </div>
            )}
          </div>
        </div>
        {hasChanges && (
          <div className="flex-shrink-0">
            <svg
              className="w-5 h-5 sm:w-6 sm:h-6 text-yellow-500 dark:text-yellow-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
        )}
      </div>
    </Link>
  )
}
