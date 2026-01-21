import { useState, useEffect } from 'react'

interface NextScrapeData {
  next_scrape_at: string | null
  seconds_until_scrape: number | null
  source_name: string | null
  is_paused?: boolean
}

export const NextScrapeCountdown = () => {
  const [countdown, setCountdown] = useState<number | null>(null)
  const [sourceName, setSourceName] = useState<string | null>(null)
  const [isPaused, setIsPaused] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Fetch next scrape time
  const fetchNextScrape = async () => {
    try {
      const response = await fetch('/api/v1/next-scrape')
      const data: NextScrapeData = await response.json()

      setIsPaused(data.is_paused || false)

      if (data.seconds_until_scrape !== null) {
        setCountdown(data.seconds_until_scrape)
        setSourceName(data.source_name)
      } else {
        setCountdown(null)
      }
      setIsLoading(false)
    } catch (error) {
      console.error('Failed to fetch next scrape time:', error)
      setIsLoading(false)
    }
  }

  // Initial fetch
  useEffect(() => {
    fetchNextScrape()
  }, [])

  // Countdown timer
  useEffect(() => {
    if (countdown === null || countdown <= 0) return

    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev === null || prev <= 1) {
          // Refetch when countdown reaches 0
          fetchNextScrape()
          return null
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [countdown])

  if (isLoading) {
    return (
      <span className="text-sm text-gray-500 dark:text-gray-400">
        Laddar...
      </span>
    )
  }

  if (isPaused) {
    return (
      <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
        <svg
          className="w-4 h-4 mr-1.5 text-gray-400 dark:text-gray-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Pausad
      </span>
    )
  }

  if (countdown === null) {
    return (
      <span className="text-sm text-gray-500 dark:text-gray-400">
        Uppdaterar snart...
      </span>
    )
  }

  const minutes = Math.floor(countdown / 60)
  const seconds = countdown % 60

  return (
    <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
      <svg 
        className="w-4 h-4 mr-1.5 text-blue-500 dark:text-blue-400 animate-pulse" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
        />
      </svg>
      Uppdateras om <span className="font-medium text-gray-700 dark:text-gray-300 mx-1">
        {minutes}:{seconds.toString().padStart(2, '0')}
      </span>
    </span>
  )
}
