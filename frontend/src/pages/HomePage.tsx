import { useState } from 'react'
import { Layout } from '../components/layout/Layout'
import { ArticleList } from '../components/article/ArticleList'
import { ArticleListSkeleton } from '../components/common/LoadingSkeleton'
import { useArticles } from '../hooks/useArticles'
import { useSources } from '../hooks/useSources'

export const HomePage = () => {
  const [selectedSource, setSelectedSource] = useState<string>('')
  const [showOnlyChanges, setShowOnlyChanges] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')

  const { data: sources } = useSources()
  const { data: articlesData, isLoading, error } = useArticles({
    source: selectedSource || undefined,
    has_changes: showOnlyChanges || undefined,
    limit: 50,
  })

  // Filter articles based on search query and date range
  const filteredArticles = articlesData?.items.filter((article) => {
    // Search filter
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase())

    // Date range filter
    let matchesDateRange = true
    const articleDate = new Date(article.first_seen_at)

    if (dateFrom) {
      const fromDate = new Date(dateFrom)
      matchesDateRange = matchesDateRange && articleDate >= fromDate
    }

    if (dateTo) {
      const toDate = new Date(dateTo)
      toDate.setHours(23, 59, 59, 999) // Include the entire day
      matchesDateRange = matchesDateRange && articleDate <= toDate
    }

    return matchesSearch && matchesDateRange
  }) || []

  return (
    <Layout>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Senaste nyhetsändringar
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Spåra hur svenska nyhetsartiklar ändras över tid
        </p>

        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 transition-colors">
          <div className="space-y-4">
            {/* Search bar */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Sök artiklar
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Sök efter artikeltitel..."
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            {/* Date range filter */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Från datum
                </label>
                <div className="relative">
                  <input
                    type="date"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                    max={dateTo || undefined}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Till datum
                </label>
                <div className="relative">
                  <input
                    type="date"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                    min={dateFrom || undefined}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                  />
                </div>
              </div>
            </div>

            {/* Source filter and changes toggle */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Källa
                </label>
                <select
                  value={selectedSource}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                >
                  <option value="">Alla källor</option>
                  {sources && (() => {
                    // Group sources by country
                    const grouped = sources.reduce((acc, source) => {
                      const country = source.country || 'Okänt'
                      if (!acc[country]) acc[country] = []
                      acc[country].push(source)
                      return acc
                    }, {} as Record<string, typeof sources>)

                    // Sort countries: Sverige first, then alphabetically
                    const sortedCountries = Object.keys(grouped).sort((a, b) => {
                      if (a === 'Sverige') return -1
                      if (b === 'Sverige') return 1
                      return a.localeCompare(b, 'sv')
                    })

                    return sortedCountries.map(country => (
                      <optgroup key={country} label={country}>
                        {grouped[country]
                          .sort((a, b) => a.name.localeCompare(b.name, 'sv'))
                          .map(source => (
                            <option key={source.id} value={source.name}>
                              {source.name} ({source.article_count} artiklar)
                            </option>
                          ))
                        }
                      </optgroup>
                    ))
                  })()}
                </select>
              </div>
              <div className="flex items-end">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showOnlyChanges}
                    onChange={(e) => setShowOnlyChanges(e.target.checked)}
                    className="w-4 h-4 text-blue-600 dark:text-blue-400 rounded focus:ring-blue-500 dark:focus:ring-blue-400"
                  />
                  <span className="ml-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                    Visa endast artiklar med ändringar
                  </span>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Stats */}
        {articlesData && (
          <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 dark:border-blue-400 p-4 mb-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-blue-700 dark:text-blue-300">
                Visar <strong>{filteredArticles.length}</strong> av{' '}
                <strong>{articlesData.total}</strong> artiklar
                {searchQuery && (
                  <span className="ml-2">
                    (filtrerade efter "{searchQuery}")
                  </span>
                )}
              </p>
              {(searchQuery || selectedSource || !showOnlyChanges || dateFrom || dateTo) && (
                <button
                  onClick={() => {
                    setSearchQuery('')
                    setSelectedSource('')
                    setShowOnlyChanges(true)
                    setDateFrom('')
                    setDateTo('')
                  }}
                  className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200 font-medium"
                >
                  Rensa alla filter
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Loading state */}
      {isLoading && <ArticleListSkeleton count={5} />}

      {/* Error state */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-400 p-4">
          <p className="text-red-700 dark:text-red-300">
            Kunde inte ladda artiklar. Kontrollera att backend körs.
          </p>
        </div>
      )}

      {/* Articles */}
      {articlesData && filteredArticles.length > 0 && (
        <ArticleList articles={filteredArticles} />
      )}

      {/* No results */}
      {articlesData && filteredArticles.length === 0 && (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg shadow">
          <svg className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">Inga artiklar hittades</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Prova att ändra dina sökkriterier eller filter
          </p>
        </div>
      )}
    </Layout>
  )
}
