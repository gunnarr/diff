export interface NewsSource {
  id: number
  name: string
  base_url: string
  scraper_class: string
  is_active: boolean
  scrape_interval_active: number
  scrape_interval_archive: number
  max_articles_per_scrape: number
  created_at: string
  article_count: number
  country?: string
}

export interface ArticleVersionSummary {
  id: number
  version_number: number
  title: string
  content: string
  captured_at: string
  word_count: number
  byline?: string
  published_date?: string
  meta_description?: string
  meta_keywords?: string
}

export interface ArticleListItem {
  id: number
  source_id: number
  url: string
  title: string
  is_active: boolean
  first_seen_at: string
  last_modified_at: string | null
  version_count: number
  latest_version: ArticleVersionSummary | null
}

export interface ArticleDetail extends ArticleListItem {
  canonical_url: string | null
  last_checked_at: string | null
  check_count: number
  source: NewsSource | null
  versions: ArticleVersionSummary[]
}

export interface PaginatedArticles {
  total: number
  items: ArticleListItem[]
  limit: number
  offset: number
}

export interface DiffChange {
  type: 'delete' | 'insert' | 'equal'
  content: string[]
  position: number
}

export interface DiffStats {
  words_added: number
  words_removed: number
  net_change: number
  title_changed: boolean
}

export interface VersionInfo {
  id: number
  version_number: number
  title: string
  captured_at: string
  word_count: number
}

export interface DiffResponse {
  article_id: number
  from_version: VersionInfo
  to_version: VersionInfo
  title_diff: { old: string; new: string } | null
  content_diff: DiffChange[]
  stats: DiffStats
}
