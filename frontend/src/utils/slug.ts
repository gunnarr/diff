/**
 * Convert text to URL-friendly slug.
 */
export function slugify(text: string): string {
  if (!text) return ''

  let slug = text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove diacritics
    .replace(/å/g, 'a')
    .replace(/ä/g, 'a')
    .replace(/ö/g, 'o')
    .replace(/[^a-z0-9\s-]/g, '') // Remove non-alphanumeric except spaces and hyphens
    .replace(/[\s-]+/g, '-') // Replace spaces and multiple hyphens with single hyphen
    .replace(/^-+|-+$/g, '') // Remove leading/trailing hyphens

  // Only truncate and remove incomplete word if text is too long
  if (slug.length > 100) {
    slug = slug.substring(0, 100)
    const lastDash = slug.lastIndexOf('-')
    if (lastDash > 0) {
      slug = slug.substring(0, lastDash)
    }
  }

  return slug
}

/**
 * Generate article URL from date and title.
 */
export function generateArticleUrl(date: string, title: string): string {
  const dateObj = new Date(date)
  const dateStr = dateObj.toISOString().split('T')[0] // YYYY-MM-DD
  const slug = slugify(title)

  return `/articles/${dateStr}/${slug}`
}
