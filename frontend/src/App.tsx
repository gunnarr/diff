import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { HomePage } from './pages/HomePage'
import { ArticlePage } from './pages/ArticlePage'
import { useDarkMode } from './hooks/useDarkMode'
import { LanguageProvider } from './contexts/LanguageContext'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  // Apply dark mode based on system preference
  useDarkMode()

  return (
    <LanguageProvider>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/articles/:date/:slug" element={<ArticlePage />} />
            <Route path="/articles/:id" element={<ArticlePage />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </LanguageProvider>
  )
}

export default App
