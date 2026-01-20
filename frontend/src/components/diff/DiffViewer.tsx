import { useState } from 'react'
import type { DiffChange } from '../../types'
import { SideBySideDiff } from './SideBySideDiff'

interface DiffViewerProps {
  changes: DiffChange[]
  fromTitle?: string
  toTitle?: string
}

type ViewMode = 'inline' | 'side-by-side'

export const DiffViewer = ({ changes, fromTitle = 'Gammal version', toTitle = 'Ny version' }: DiffViewerProps) => {
  const [viewMode, setViewMode] = useState<ViewMode>('inline')

  if (changes.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500 dark:text-gray-400">Ingen skillnad upptäckt</p>
      </div>
    )
  }

  return (
    <div>
      {/* View mode toggle */}
      <div className="mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between bg-gray-50 dark:bg-gray-700 p-3 rounded-lg gap-3">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Visningsläge:</span>
        <div className="inline-flex rounded-lg shadow-sm" role="group">
          <button
            type="button"
            onClick={() => setViewMode('inline')}
            className={`flex-1 sm:flex-initial px-4 py-2 text-sm font-medium rounded-l-lg border ${
              viewMode === 'inline'
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white dark:bg-gray-600 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-500'
            }`}
          >
            <div className="flex items-center justify-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <span className="hidden sm:inline">Inline</span>
            </div>
          </button>
          <button
            type="button"
            onClick={() => setViewMode('side-by-side')}
            className={`flex-1 sm:flex-initial px-4 py-2 text-sm font-medium rounded-r-lg border-t border-r border-b ${
              viewMode === 'side-by-side'
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white dark:bg-gray-600 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-500'
            }`}
          >
            <div className="flex items-center justify-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 4v16m6-16v16" />
              </svg>
              <span className="hidden sm:inline">Jämför</span>
              <span className="sm:hidden">Sida vid sida</span>
            </div>
          </button>
        </div>
      </div>

      {/* Render based on view mode */}
      {viewMode === 'inline' ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="space-y-2">
            {changes.map((change, index) => {
              if (change.type === 'equal') return null

              return (
                <div key={index} className="flex items-start">
                  {change.type === 'delete' && (
                    <div className="flex-1 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-600 p-3 rounded">
                      <span className="inline-block px-2 py-1 text-xs font-semibold text-red-800 dark:text-red-300 bg-red-200 dark:bg-red-900/40 rounded mr-2">
                        Borttaget
                      </span>
                      <span className="text-red-900 dark:text-red-300 line-through">
                        {change.content.join(' ')}
                      </span>
                    </div>
                  )}
                  {change.type === 'insert' && (
                    <div className="flex-1 bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 dark:border-green-600 p-3 rounded">
                      <span className="inline-block px-2 py-1 text-xs font-semibold text-green-800 dark:text-green-300 bg-green-200 dark:bg-green-900/40 rounded mr-2">
                        Tillagt
                      </span>
                      <span className="text-green-900 dark:text-green-300 font-medium">
                        {change.content.join(' ')}
                      </span>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      ) : (
        <SideBySideDiff changes={changes} oldTitle={fromTitle} newTitle={toTitle} />
      )}
    </div>
  )
}
