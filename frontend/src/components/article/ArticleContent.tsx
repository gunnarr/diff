import { useState } from 'react'

interface ArticleContentProps {
  versionNumber: number
  title: string
  content: string
  wordCount: number
  capturedAt: string
  isOlder?: boolean
}

export const ArticleContent = ({ versionNumber, title, content, wordCount, capturedAt, isOlder = false }: ArticleContentProps) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const previewLength = 300

  const shouldTruncate = content.length > previewLength
  const displayContent = isExpanded || !shouldTruncate
    ? content
    : content.slice(0, previewLength) + '...'

  // Color scheme based on version age
  const colorScheme = isOlder ? {
    bg: 'bg-red-50',
    border: 'border-red-200',
    headerBg: 'bg-red-100',
    headerText: 'text-red-900',
    badge: 'bg-red-500',
    icon: 'text-red-600',
    label: 'Äldre version'
  } : {
    bg: 'bg-green-50',
    border: 'border-green-200',
    headerBg: 'bg-green-100',
    headerText: 'text-green-900',
    badge: 'bg-green-500',
    icon: 'text-green-600',
    label: 'Nyare version'
  }

  return (
    <div className={`${colorScheme.bg} rounded-lg shadow-md border-2 ${colorScheme.border} overflow-hidden`}>
      {/* Header with color coding */}
      <div className={`${colorScheme.headerBg} px-4 py-3 border-b-2 ${colorScheme.border}`}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${colorScheme.badge}`}></div>
            <h3 className={`text-lg font-semibold ${colorScheme.headerText}`}>
              Version {versionNumber}
            </h3>
            <span className={`text-xs font-medium px-2 py-1 rounded ${colorScheme.headerText} bg-white`}>
              {colorScheme.label}
            </span>
          </div>
          <span className="text-sm text-gray-600">{wordCount} ord</span>
        </div>
        <p className="text-xs text-gray-600">{capturedAt}</p>
      </div>

      {/* Content area */}
      <div className="p-6 bg-white">
        <h4 className="text-xl font-medium text-gray-800 mb-4">{title}</h4>

        <div className="prose prose-sm max-w-none">
          <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {displayContent}
          </p>
        </div>

        {shouldTruncate && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="mt-4 text-blue-600 hover:text-blue-800 font-medium text-sm flex items-center"
          >
            {isExpanded ? (
              <>
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
                Visa mindre
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
                Läs hela artikeln
              </>
            )}
          </button>
        )}
      </div>
    </div>
  )
}
