import { Link } from 'react-router-dom'

interface ArticleMetadataProps {
  author?: string
  publishedDate?: string
  tags?: string[]
  metaDescription?: string
}

export const ArticleMetadata = ({
  author,
  publishedDate,
  tags = [],
  metaDescription
}: ArticleMetadataProps) => {
  return (
    <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-6 transition-colors">
      <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Artikelinfo</h3>

      <div className="space-y-3">
        {/* Author */}
        {author && (
          <div className="flex items-start">
            <svg className="w-5 h-5 text-gray-400 dark:text-gray-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <div>
              <div className="text-xs text-gray-500 dark:text-gray-400">Författare</div>
              <Link
                to={`/?author=${encodeURIComponent(author)}`}
                className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 hover:underline"
              >
                {author}
              </Link>
            </div>
          </div>
        )}

        {/* Published Date */}
        {publishedDate && (
          <div className="flex items-start">
            <svg className="w-5 h-5 text-gray-400 dark:text-gray-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <div>
              <div className="text-xs text-gray-500 dark:text-gray-400">Publicerad</div>
              <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                {new Date(publishedDate).toLocaleDateString('sv-SE', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
            </div>
          </div>
        )}

        {/* Description */}
        {metaDescription && (
          <div className="flex items-start">
            <svg className="w-5 h-5 text-gray-400 dark:text-gray-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Beskrivning</div>
              <div className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                {metaDescription}
              </div>
            </div>
          </div>
        )}

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex items-start">
            <svg className="w-5 h-5 text-gray-400 dark:text-gray-500 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <div className="flex-1">
              <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">Ämnen</div>
              <div className="flex flex-wrap gap-2">
                {tags.map((tag, index) => (
                  <Link
                    key={index}
                    to={`/?tag=${encodeURIComponent(tag)}`}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
                  >
                    {tag}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
