import { useState } from 'react'
import type { DiffChange } from '../../types'

interface SideBySideDiffProps {
  changes: DiffChange[]
  oldTitle: string
  newTitle: string
}

export const SideBySideDiff = ({ changes, oldTitle, newTitle }: SideBySideDiffProps) => {
  // Reconstruct text segments with context
  const segments: Array<{ old: string[], new: string[], type: 'equal' | 'change' }> = []

  let currentOld: string[] = []
  let currentNew: string[] = []
  let lastPosition = 0

  changes.forEach((change, idx) => {
    if (change.type === 'equal') {
      // Add equal segments as context
      if (currentOld.length > 0 || currentNew.length > 0) {
        segments.push({ old: currentOld, new: currentNew, type: 'change' })
        currentOld = []
        currentNew = []
      }
      segments.push({ old: change.content, new: change.content, type: 'equal' })
    } else if (change.type === 'delete') {
      currentOld.push(...change.content)
    } else if (change.type === 'insert') {
      currentNew.push(...change.content)
    }

    // If this is the last change or next change is equal, flush current changes
    if (idx === changes.length - 1 || (idx < changes.length - 1 && changes[idx + 1].type === 'equal')) {
      if (currentOld.length > 0 || currentNew.length > 0) {
        segments.push({ old: currentOld, new: currentNew, type: 'change' })
        currentOld = []
        currentNew = []
      }
    }
  })

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <div className="grid grid-cols-1 lg:grid-cols-2 lg:divide-x divide-gray-200 dark:divide-gray-600">
        {/* Old version (left) */}
        <div className="bg-red-50 dark:bg-red-900/10">
          <div className="bg-red-100 dark:bg-red-900/30 border-b border-red-200 dark:border-red-800 px-4 py-3 font-semibold text-red-900 dark:text-red-300 flex items-center">
            <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="truncate text-sm lg:text-base">{oldTitle}</span>
          </div>
          <div className="p-4 space-y-2 text-sm max-h-96 lg:max-h-none overflow-y-auto">
            {segments.map((segment, idx) => (
              <div key={`old-${idx}`} className="break-words">
                {segment.type === 'equal' ? (
                  <span className="text-gray-600 dark:text-gray-400">{segment.old.join(' ')}</span>
                ) : (
                  segment.old.length > 0 && (
                    <span className="bg-red-200 dark:bg-red-900/40 text-red-900 dark:text-red-300 px-1 rounded line-through">
                      {segment.old.join(' ')}
                    </span>
                  )
                )}
              </div>
            ))}
          </div>
        </div>

        {/* New version (right) */}
        <div className="bg-green-50 dark:bg-green-900/10 border-t lg:border-t-0 border-gray-200 dark:border-gray-600">
          <div className="bg-green-100 dark:bg-green-900/30 border-b border-green-200 dark:border-green-800 px-4 py-3 font-semibold text-green-900 dark:text-green-300 flex items-center">
            <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="truncate text-sm lg:text-base">{newTitle}</span>
          </div>
          <div className="p-4 space-y-2 text-sm max-h-96 lg:max-h-none overflow-y-auto">
            {segments.map((segment, idx) => (
              <div key={`new-${idx}`} className="break-words">
                {segment.type === 'equal' ? (
                  <span className="text-gray-600 dark:text-gray-400">{segment.new.join(' ')}</span>
                ) : (
                  segment.new.length > 0 && (
                    <span className="bg-green-200 dark:bg-green-900/40 text-green-900 dark:text-green-300 px-1 rounded font-medium">
                      {segment.new.join(' ')}
                    </span>
                  )
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
