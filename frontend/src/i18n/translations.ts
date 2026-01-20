export type Language = 'sv' | 'en'

export interface Translations {
  // Header
  appTitle: string
  appSubtitle: string
  home: string

  // HomePage
  latestChanges: string
  trackingSubtitle: string
  searchArticles: string
  searchPlaceholder: string
  fromDate: string
  toDate: string
  source: string
  allSources: string
  showOnlyChanges: string
  showing: string
  of: string
  articles: string
  filteredBy: string
  clearFilters: string
  noArticlesFound: string
  tryChangingFilters: string

  // Article stats
  firstSeen: string
  lastModified: string
  versions: string
  words: string

  // ArticlePage
  backToList: string
  openOriginal: string
  articleInfo: string
  author: string
  published: string
  description: string
  topics: string
  versionHistory: string
  latest: string
  compareVersions: string
  fromVersion: string
  toVersion: string
  articleTextWithChanges: string
  titleChange: string
  contentChanges: string
  noChangesYet: string

  // Footer stats
  totalArticles: string
  totalVersions: string
  withChanges: string
  activeSources: string
  totalSources: string
  footerSubtitle: string

  // Countries
  sweden: string
  norway: string
  denmark: string
  finland: string
  uk: string
  unknown: string
}

export const translations: Record<Language, Translations> = {
  sv: {
    // Header
    appTitle: 'NewsDiff',
    appSubtitle: 'Spåra nyhetsändringar',
    home: 'Hem',

    // HomePage
    latestChanges: 'Senaste nyhetsändringar',
    trackingSubtitle: 'Spåra hur svenska nyhetsartiklar ändras över tid',
    searchArticles: 'Sök artiklar',
    searchPlaceholder: 'Sök efter artikeltitel...',
    fromDate: 'Från datum',
    toDate: 'Till datum',
    source: 'Källa',
    allSources: 'Alla källor',
    showOnlyChanges: 'Visa endast artiklar med ändringar',
    showing: 'Visar',
    of: 'av',
    articles: 'artiklar',
    filteredBy: 'filtrerade efter',
    clearFilters: 'Rensa alla filter',
    noArticlesFound: 'Inga artiklar hittades',
    tryChangingFilters: 'Prova att ändra dina sökkriterier eller filter',

    // Article stats
    firstSeen: 'Först upptäckt',
    lastModified: 'Senast ändrad',
    versions: 'versioner',
    words: 'ord',

    // ArticlePage
    backToList: 'Tillbaka till listan',
    openOriginal: 'Öppna originalartikel',
    articleInfo: 'Artikelinfo',
    author: 'Författare',
    published: 'Publicerad',
    description: 'Beskrivning',
    topics: 'Ämnen',
    versionHistory: 'Versionshistorik',
    latest: 'Senaste',
    compareVersions: 'Jämför versioner',
    fromVersion: 'Från version',
    toVersion: 'Till version',
    articleTextWithChanges: 'Artikeltext med ändringar markerade',
    titleChange: 'Titeländring',
    contentChanges: 'Innehållsändringar',
    noChangesYet: 'Denna artikel har ännu inte ändrats sedan den först upptäcktes.',

    // Footer stats
    totalArticles: 'Artiklar',
    totalVersions: 'Versioner',
    withChanges: 'Med ändringar',
    activeSources: 'Aktiva källor',
    totalSources: 'Totalt källor',
    footerSubtitle: 'Nyhetsdiff-tracker · Automatisk scraping var 15:e minut',

    // Countries
    sweden: 'Sverige',
    norway: 'Norge',
    denmark: 'Danmark',
    finland: 'Finland',
    uk: 'Storbritannien',
    unknown: 'Okänt',
  },
  en: {
    // Header
    appTitle: 'NewsDiff',
    appSubtitle: 'Track news changes',
    home: 'Home',

    // HomePage
    latestChanges: 'Latest news changes',
    trackingSubtitle: 'Track how news articles change over time',
    searchArticles: 'Search articles',
    searchPlaceholder: 'Search by article title...',
    fromDate: 'From date',
    toDate: 'To date',
    source: 'Source',
    allSources: 'All sources',
    showOnlyChanges: 'Show only articles with changes',
    showing: 'Showing',
    of: 'of',
    articles: 'articles',
    filteredBy: 'filtered by',
    clearFilters: 'Clear all filters',
    noArticlesFound: 'No articles found',
    tryChangingFilters: 'Try changing your search criteria or filters',

    // Article stats
    firstSeen: 'First seen',
    lastModified: 'Last modified',
    versions: 'versions',
    words: 'words',

    // ArticlePage
    backToList: 'Back to list',
    openOriginal: 'Open original article',
    articleInfo: 'Article info',
    author: 'Author',
    published: 'Published',
    description: 'Description',
    topics: 'Topics',
    versionHistory: 'Version history',
    latest: 'Latest',
    compareVersions: 'Compare versions',
    fromVersion: 'From version',
    toVersion: 'To version',
    articleTextWithChanges: 'Article text with changes highlighted',
    titleChange: 'Title change',
    contentChanges: 'Content changes',
    noChangesYet: 'This article has not been modified since it was first discovered.',

    // Footer stats
    totalArticles: 'Articles',
    totalVersions: 'Versions',
    withChanges: 'With changes',
    activeSources: 'Active sources',
    totalSources: 'Total sources',
    footerSubtitle: 'News diff tracker · Automatic scraping every 15 minutes',

    // Countries
    sweden: 'Sweden',
    norway: 'Norway',
    denmark: 'Denmark',
    finland: 'Finland',
    uk: 'United Kingdom',
    unknown: 'Unknown',
  },
}
