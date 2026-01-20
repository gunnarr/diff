import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { DiffViewer } from '../components/diff/DiffViewer'
import { DiffStats } from '../components/diff/DiffStats'
import { ArticleContentHighlighted } from '../components/article/ArticleContentHighlighted'
import { ArticleMetadata } from '../components/article/ArticleMetadata'
import { ArticleDetailSkeleton } from '../components/common/LoadingSkeleton'
import { useArticle, useDiff } from '../hooks/useArticles'
import { formatDateTime, formatRelativeTime } from '../utils/date'

export const ArticlePage = () => {
  const { id, date, slug } = useParams<{ id?: string, date?: string, slug?: string }>()

  // Support both URL formats: /articles/:id and /articles/:date/:slug
  const urlPath = date && slug ? `${date}/${slug}` : id
  const articleId = id ? Number(id) : null

  const { data: article, isLoading, error } = useArticle(urlPath || '')

  const [fromVersion, setFromVersion] = useState<number | null>(null)
  const [toVersion, setToVersion] = useState<number | null>(null)

  const { data: diff } = useDiff(
    article?.id || 0,
    fromVersion || 0,
    toVersion || 0
  )

  // Auto-select first two versions when article loads
  if (article && !fromVersion && article.versions.length >= 2) {
    setFromVersion(article.versions[article.versions.length - 1].version_number)
    setToVersion(article.versions[0].version_number)
  }

  if (isLoading) {
    return (
      <Layout>
        <ArticleDetailSkeleton />
      </Layout>
    )
  }

  if (error || !article) {
    return (
      <Layout>
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <p className="text-red-700">Kunde inte ladda artikel</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      {/* Back button */}
      <Link
        to="/"
        className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-6"
      >
        <svg
          className="w-5 h-5 mr-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        Tillbaka till listan
      </Link>

      {/* Article header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          {article.title}
        </h1>
        <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
          <div className="flex items-center space-x-4">
            <span className="font-medium">{article.source?.name}</span>
            <span>•</span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Först upptäckt {formatRelativeTime(article.first_seen_at)}
            </span>
            <span>•</span>
            <span className="font-medium text-blue-600 dark:text-blue-400">
              {article.version_count} versioner
            </span>
          </div>
          {article.last_modified_at && (
            <div className="flex items-center text-yellow-700 dark:text-yellow-400">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Senast ändrad {formatRelativeTime(article.last_modified_at)} ({formatDateTime(article.last_modified_at)})
            </div>
          )}
        </div>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center mt-4 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
        >
          Öppna originalartikel
          <svg
            className="w-4 h-4 ml-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      </div>

      {/* Article Metadata */}
      {article.versions.length > 0 && (
        <ArticleMetadata
          author={article.versions[0].byline}
          publishedDate={article.versions[0].published_date}
          tags={article.versions[0].meta_keywords?.split(',').map(t => t.trim()).filter(Boolean)}
          metaDescription={article.versions[0].meta_description}
        />
      )}

      {/* Version history timeline */}
      {article.version_count > 1 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Versionshistorik</h2>
          <div className="space-y-3">
            {article.versions.map((version, index) => (
              <div
                key={version.id}
                className={`flex items-start p-3 rounded-lg border-2 ${
                  index === 0
                    ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-600'
                    : 'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600'
                }`}
              >
                <div className="flex-shrink-0 w-24 text-center">
                  <div className={`inline-flex items-center justify-center px-3 py-1 rounded-full text-sm font-medium ${
                    index === 0 ? 'bg-blue-600 text-white' : 'bg-gray-600 dark:bg-gray-500 text-white'
                  }`}>
                    V{version.version_number}
                  </div>
                  {index === 0 && (
                    <div className="text-xs text-blue-600 dark:text-blue-400 font-medium mt-1">Senaste</div>
                  )}
                </div>
                <div className="flex-1 ml-4">
                  <div className="font-medium text-gray-900 dark:text-white">{version.title}</div>
                  <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600 dark:text-gray-400">
                    <span className="flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {formatDateTime(version.captured_at)}
                    </span>
                    <span>•</span>
                    <span>{formatRelativeTime(version.captured_at)}</span>
                    <span>•</span>
                    <span>{version.word_count} ord</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Version selector */}
      {article.version_count > 1 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Jämför versioner</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Från version
              </label>
              <select
                value={fromVersion || ''}
                onChange={(e) => setFromVersion(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {article.versions.slice().reverse().map((v) => (
                  <option key={v.id} value={v.version_number}>
                    Version {v.version_number} - {formatDateTime(v.captured_at)} ({v.word_count} ord)
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Till version
              </label>
              <select
                value={toVersion || ''}
                onChange={(e) => setToVersion(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {article.versions.slice().reverse().map((v) => (
                  <option key={v.id} value={v.version_number}>
                    Version {v.version_number} - {formatDateTime(v.captured_at)} ({v.word_count} ord)
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Full article content for selected versions */}
      {fromVersion && toVersion && article && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Artikeltext med ändringar markerade</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* From version content (older) */}
            {article.versions.find(v => v.version_number === fromVersion) && (
              <ArticleContentHighlighted
                versionNumber={fromVersion}
                title={article.versions.find(v => v.version_number === fromVersion)!.title}
                content={article.versions.find(v => v.version_number === fromVersion)!.content}
                wordCount={article.versions.find(v => v.version_number === fromVersion)!.word_count}
                capturedAt={formatDateTime(article.versions.find(v => v.version_number === fromVersion)!.captured_at)}
                isOlder={fromVersion < toVersion}
                diffChanges={diff?.content_diff || []}
                showAsOldVersion={true}
              />
            )}

            {/* To version content (newer) */}
            {article.versions.find(v => v.version_number === toVersion) && (
              <ArticleContentHighlighted
                versionNumber={toVersion}
                title={article.versions.find(v => v.version_number === toVersion)!.title}
                content={article.versions.find(v => v.version_number === toVersion)!.content}
                wordCount={article.versions.find(v => v.version_number === toVersion)!.word_count}
                capturedAt={formatDateTime(article.versions.find(v => v.version_number === toVersion)!.captured_at)}
                isOlder={toVersion < fromVersion}
                diffChanges={diff?.content_diff || []}
                showAsOldVersion={false}
              />
            )}
          </div>
        </div>
      )}

      {/* Diff display */}
      {diff && (
        <>
          <div className="mb-6">
            <DiffStats stats={diff.stats} />
          </div>

          {diff.title_diff && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Titeländring</h3>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 space-y-3">
                <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-600 p-3 rounded">
                  <span className="text-red-900 dark:text-red-300 line-through">
                    {diff.title_diff.old}
                  </span>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 dark:border-green-600 p-3 rounded">
                  <span className="text-green-900 dark:text-green-300 font-medium">
                    {diff.title_diff.new}
                  </span>
                </div>
              </div>
            </div>
          )}

          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Innehållsändringar</h3>
            <DiffViewer
              changes={diff.content_diff}
              fromTitle={`Version ${diff.from_version.version_number} (${formatDateTime(diff.from_version.captured_at)})`}
              toTitle={`Version ${diff.to_version.version_number} (${formatDateTime(diff.to_version.captured_at)})`}
            />
          </div>
        </>
      )}

      {/* No changes message */}
      {article.version_count === 1 && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 dark:border-blue-600 p-4">
          <p className="text-blue-700 dark:text-blue-300">
            Denna artikel har ännu inte ändrats sedan den först upptäcktes.
          </p>
        </div>
      )}
    </Layout>
  )
}
