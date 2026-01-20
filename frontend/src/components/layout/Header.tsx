import { Link } from 'react-router-dom'

export const Header = () => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Nyhetsdiff
            </h1>
            <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
              Spåra ändringar i svenska nyhetsartiklar
            </span>
          </Link>
          <nav className="flex items-center space-x-4">
            <Link
              to="/"
              className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Hem
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
