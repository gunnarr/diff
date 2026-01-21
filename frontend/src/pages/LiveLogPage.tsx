import { useState, useEffect } from 'react'
import { Layout } from '../components/layout/Layout'

interface LogEntry {
  timestamp: string
  level: string
  message: string
}

interface LogsResponse {
  logs: LogEntry[]
  total_lines: number
}

interface TestStatus {
  last_run: string | null
  status: string | null
  summary: string | null
}

export const LiveLogPage = () => {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isLive, setIsLive] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [isScraping, setIsScraping] = useState(false)
  const [isRunningTests, setIsRunningTests] = useState(false)
  const [testStatus, setTestStatus] = useState<TestStatus | null>(null)

  const fetchLogs = async () => {
    try {
      const response = await fetch('/api/v1/logs?limit=200&filter_scraping=true')
      const data: LogsResponse = await response.json()
      setLogs(data.logs)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    }
  }

  const fetchTestStatus = async () => {
    try {
      const response = await fetch('/api/v1/test-status')
      const data: TestStatus = await response.json()
      setTestStatus(data)
    } catch (error) {
      console.error('Failed to fetch test status:', error)
    }
  }

  const runTests = async () => {
    setIsRunningTests(true)
    try {
      const response = await fetch('/api/v1/run-tests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        // Refresh test status after tests complete
        await fetchTestStatus()
        setTimeout(() => {
          fetchLogs()
        }, 1000)
      } else {
        console.error('Failed to run tests:', await response.text())
      }
    } catch (error) {
      console.error('Failed to run tests:', error)
    } finally {
      setIsRunningTests(false)
    }
  }

  const triggerScrape = async () => {
    setIsScraping(true)
    try {
      const response = await fetch('/api/v1/sources/1/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        // Wait a moment then refresh logs
        setTimeout(() => {
          fetchLogs()
        }, 1000)
      } else {
        console.error('Failed to trigger scrape:', await response.text())
      }
    } catch (error) {
      console.error('Failed to trigger scrape:', error)
    } finally {
      setIsScraping(false)
    }
  }

  // Initial fetch
  useEffect(() => {
    fetchLogs()
    fetchTestStatus()
  }, [])

  // Auto-refresh every 2 seconds when live
  useEffect(() => {
    if (!isLive) return

    const interval = setInterval(() => {
      fetchLogs()
    }, 2000)

    return () => clearInterval(interval)
  }, [isLive])

  const getLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case 'ERROR':
        return 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20'
      case 'WARNING':
        return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20'
      case 'INFO':
        return 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20'
      default:
        return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800'
    }
  }

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Live Backend Logs
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Visar scraping-aktivitet i realtid
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={runTests}
              disabled={isRunningTests}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                isRunningTests
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-purple-600 text-white hover:bg-purple-700'
              }`}
            >
              {isRunningTests ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Kör tester...
                </span>
              ) : (
                'Kör tester'
              )}
            </button>
            <button
              onClick={triggerScrape}
              disabled={isScraping}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                isScraping
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-red-600 text-white hover:bg-red-700'
              }`}
            >
              {isScraping ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Hämtar...
                </span>
              ) : (
                'Hämta artiklar'
              )}
            </button>
            <button
              onClick={() => setIsLive(!isLive)}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                isLive
                  ? 'bg-green-600 text-white hover:bg-green-700'
                  : 'bg-gray-300 text-gray-700 hover:bg-gray-400 dark:bg-gray-600 dark:text-gray-200'
              }`}
            >
              <span className="flex items-center">
                {isLive ? (
                  <>
                    <span className="w-2 h-2 bg-white rounded-full mr-2 animate-pulse"></span>
                    Live
                  </>
                ) : (
                  <>Pausad</>
                )}
              </span>
            </button>
            <button
              onClick={fetchLogs}
              className="px-4 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors"
            >
              Uppdatera nu
            </button>
          </div>
        </div>

        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600 dark:text-gray-400">
              Totalt antal loggrader: <span className="font-medium text-gray-900 dark:text-white">{logs.length}</span>
            </span>
            <span className="text-gray-600 dark:text-gray-400">
              Senast uppdaterad: <span className="font-medium text-gray-900 dark:text-white">{lastUpdate.toLocaleTimeString('sv-SE')}</span>
            </span>
          </div>
        </div>

        {testStatus && (
          <div className={`rounded-lg p-4 mb-4 border-l-4 ${
            testStatus.status === 'success'
              ? 'bg-green-50 dark:bg-green-900/20 border-green-500'
              : testStatus.status === 'failed'
              ? 'bg-red-50 dark:bg-red-900/20 border-red-500'
              : 'bg-gray-50 dark:bg-gray-800 border-gray-400'
          }`}>
            <div className="flex items-start">
              <svg
                className={`w-5 h-5 mr-3 flex-shrink-0 mt-0.5 ${
                  testStatus.status === 'success'
                    ? 'text-green-600 dark:text-green-400'
                    : testStatus.status === 'failed'
                    ? 'text-red-600 dark:text-red-400'
                    : 'text-gray-600 dark:text-gray-400'
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                {testStatus.status === 'success' ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                ) : testStatus.status === 'failed' ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                )}
              </svg>
              <div className="flex-1">
                <p className={`font-medium ${
                  testStatus.status === 'success'
                    ? 'text-green-800 dark:text-green-300'
                    : testStatus.status === 'failed'
                    ? 'text-red-800 dark:text-red-300'
                    : 'text-gray-800 dark:text-gray-300'
                }`}>
                  Systemtester
                </p>
                <p className={`text-sm mt-1 ${
                  testStatus.status === 'success'
                    ? 'text-green-700 dark:text-green-400'
                    : testStatus.status === 'failed'
                    ? 'text-red-700 dark:text-red-400'
                    : 'text-gray-700 dark:text-gray-400'
                }`}>
                  {testStatus.summary}
                </p>
                {testStatus.last_run && (
                  <p className="text-xs text-gray-600 dark:text-gray-500 mt-1">
                    Senast körda: {new Date(testStatus.last_run).toLocaleString('sv-SE')}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {logs.length === 0 ? (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 dark:border-yellow-600 p-4 rounded">
          <div className="flex items-start">
            <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <p className="text-yellow-800 dark:text-yellow-300 font-medium">
                Inga scraping-loggar ännu
              </p>
              <p className="text-yellow-700 dark:text-yellow-400 text-sm mt-1">
                Loggarna kommer att börja dyka upp när nästa scrape körs. Sidan uppdateras automatiskt var 2:a sekund när "Live" är aktivt.
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-gray-900 rounded-lg overflow-hidden shadow-lg font-mono text-sm">
          <div className="overflow-y-auto" style={{ maxHeight: 'calc(100vh - 320px)' }}>
            {logs.map((log, index) => (
              <div
                key={index}
                className="border-b border-gray-800 hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-start p-3 space-x-3">
                  <span className="text-gray-500 dark:text-gray-400 text-xs whitespace-nowrap flex-shrink-0">
                    {log.timestamp}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold uppercase flex-shrink-0 ${getLevelColor(log.level)}`}>
                    {log.level}
                  </span>
                  <span className="text-gray-300 dark:text-gray-200 flex-1 break-words">
                    {log.message}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </Layout>
  )
}
