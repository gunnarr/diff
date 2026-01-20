const rtf = new Intl.RelativeTimeFormat('sv', { numeric: 'auto' })

export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  const intervals = [
    { seconds: 31536000, unit: 'year' as Intl.RelativeTimeFormatUnit },
    { seconds: 2592000, unit: 'month' as Intl.RelativeTimeFormatUnit },
    { seconds: 86400, unit: 'day' as Intl.RelativeTimeFormatUnit },
    { seconds: 3600, unit: 'hour' as Intl.RelativeTimeFormatUnit },
    { seconds: 60, unit: 'minute' as Intl.RelativeTimeFormatUnit },
  ]

  for (const { seconds, unit } of intervals) {
    const value = Math.floor(diffInSeconds / seconds)
    if (value >= 1) {
      return rtf.format(-value, unit)
    }
  }

  return 'just nu'
}

export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('sv-SE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date).replace(',', '')
}
