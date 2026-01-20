import { useState } from 'react'
import type { DiffChange } from '../../types'

interface ArticleContentHighlightedProps {
  versionNumber: number
  title: string
  content: string
  wordCount: number
  capturedAt: string
  isOlder?: boolean
  diffChanges?: DiffChange[]
  showAsOldVersion?: boolean
}

export const ArticleContentHighlighted = ({
  versionNumber,
  title,
  content,
  wordCount,
  capturedAt,
  isOlder = false,
  diffChanges = [],
  showAsOldVersion = false
}: ArticleContentHighlightedProps) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const [showHighlights, setShowHighlights] = useState(true)

  // Color scheme based on version age
  const colorScheme = isOlder ? {
    bg: 'bg-red-50 dark:bg-red-900/10',
    border: 'border-red-200 dark:border-red-800',
    headerBg: 'bg-red-100 dark:bg-red-900/30',
    headerText: 'text-red-900 dark:text-red-300',
    badge: 'bg-red-500',
    label: 'Äldre version'
  } : {
    bg: 'bg-green-50 dark:bg-green-900/10',
    border: 'border-green-200 dark:border-green-800',
    headerBg: 'bg-green-100 dark:bg-green-900/30',
    headerText: 'text-green-900 dark:text-green-300',
    badge: 'bg-green-500',
    label: 'Nyare version'
  }

  // Build highlighted content using simple string matching
  const buildHighlightedContent = () => {
    if (!showHighlights || diffChanges.length === 0) {
      return content
    }

    let result = content
    const highlights: Array<{text: string, type: 'delete' | 'insert', index: number}> = []

    // Find all occurrences of changed text
    diffChanges.forEach(change => {
      if (change.type === 'equal') return

      const changeText = change.content.join(' ')

      // For old version, only highlight deletions
      // For new version, only highlight insertions
      if ((showAsOldVersion && change.type === 'delete') ||
          (!showAsOldVersion && change.type === 'insert')) {

        let index = result.indexOf(changeText)
        while (index !== -1) {
          highlights.push({
            text: changeText,
            type: change.type,
            index: index
          })
          // Look for next occurrence
          index = result.indexOf(changeText, index + changeText.length)
        }
      }
    })

    // Sort highlights by index (reverse order to replace from end to start)
    highlights.sort((a, b) => b.index - a.index)

    // Apply highlights
    highlights.forEach(highlight => {
      const before = result.substring(0, highlight.index)
      const after = result.substring(highlight.index + highlight.text.length)

      const highlightClass = highlight.type === 'delete'
        ? 'bg-red-300 dark:bg-red-900/40 text-red-900 dark:text-red-300 px-1 rounded font-medium'
        : 'bg-green-300 dark:bg-green-900/40 text-green-900 dark:text-green-300 px-1 rounded font-medium'

      result = before + `<mark class="${highlightClass}">${highlight.text}</mark>` + after
    })

    return result
  }

  const displayHTML = buildHighlightedContent()
  const shouldTruncate = content.length > 300
  const truncatedHTML = shouldTruncate && !isExpanded
    ? displayHTML.substring(0, 300) + '...'
    : displayHTML

  return (
    <div className={`${colorScheme.bg} rounded-lg shadow-md border-2 ${colorScheme.border} overflow-hidden`}>
      {/* Header with color coding */}
      <div className={`${colorScheme.headerBg} px-4 py-3 border-b-2 ${colorScheme.border}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${colorScheme.badge}`}></div>
            <h3 className={`text-lg font-semibold ${colorScheme.headerText}`}>
              Version {versionNumber}
            </h3>
            <span className={`text-xs font-medium px-2 py-1 rounded ${colorScheme.headerText} bg-white dark:bg-gray-700 whitespace-nowrap`}>
              {colorScheme.label}
            </span>
          </div>
          <div className="flex items-center gap-3">
            {diffChanges.length > 0 && (
              <button
                onClick={() => setShowHighlights(!showHighlights)}
                className={`text-xs px-3 py-1 rounded font-medium whitespace-nowrap ${
                  showHighlights
                    ? 'bg-blue-500 text-white'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600'
                }`}
              >
                {showHighlights ? '🔍 Dölj ändringar' : 'Visa ändringar'}
              </button>
            )}
            <span className="text-sm text-gray-600 dark:text-gray-400 whitespace-nowrap">{wordCount} ord</span>
          </div>
        </div>
        <p className="text-xs text-gray-600 dark:text-gray-400">{capturedAt}</p>
      </div>

      {/* Content area */}
      <div className="p-6 bg-white dark:bg-gray-800">
        <h4 className="text-xl font-medium text-gray-800 dark:text-gray-200 mb-4 break-words">{title}</h4>

        <div className="prose prose-sm max-w-none">
          <div
            className="leading-relaxed whitespace-pre-wrap text-gray-700 dark:text-gray-300"
            dangerouslySetInnerHTML={{ __html: truncatedHTML }}
          />
        </div>

        {shouldTruncate && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="mt-4 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium text-sm flex items-center"
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
