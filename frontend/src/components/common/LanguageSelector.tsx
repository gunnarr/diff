import { useLanguage } from '../../contexts/LanguageContext'

export const LanguageSelector = () => {
  const { language, setLanguage } = useLanguage()

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={() => setLanguage('sv')}
        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
          language === 'sv'
            ? 'bg-blue-600 text-white'
            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
        }`}
      >
        SV
      </button>
      <button
        onClick={() => setLanguage('en')}
        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
          language === 'en'
            ? 'bg-blue-600 text-white'
            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
        }`}
      >
        EN
      </button>
    </div>
  )
}
