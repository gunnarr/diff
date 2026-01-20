import { useEffect } from 'react'

export const useDarkMode = () => {
  useEffect(() => {
    // Check system preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

    const applyTheme = (isDark: boolean) => {
      if (isDark) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    // Apply initial theme
    applyTheme(mediaQuery.matches)

    // Listen for changes
    const listener = (e: MediaQueryListEvent) => {
      applyTheme(e.matches)
    }

    mediaQuery.addEventListener('change', listener)

    return () => {
      mediaQuery.removeEventListener('change', listener)
    }
  }, [])
}
