import { formatDistanceToNow, format } from 'date-fns'
import { sv } from 'date-fns/locale'

export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString)
  return formatDistanceToNow(date, { addSuffix: true, locale: sv })
}

export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  return format(date, 'yyyy-MM-dd HH:mm', { locale: sv })
}
