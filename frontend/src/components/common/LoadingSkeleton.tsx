export const ArticleCardSkeleton = () => {
  return (
    <div className="block bg-white rounded-lg shadow p-4 sm:p-6 animate-pulse">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 space-y-3">
          {/* Title skeleton */}
          <div className="h-5 bg-gray-200 rounded w-3/4"></div>

          {/* First line of metadata */}
          <div className="flex items-center space-x-4">
            <div className="h-4 bg-gray-200 rounded w-32"></div>
            <div className="h-4 bg-gray-200 rounded w-16"></div>
          </div>

          {/* Second line of metadata */}
          <div className="flex items-center space-x-4">
            <div className="h-4 bg-gray-200 rounded w-40"></div>
            <div className="h-4 bg-gray-200 rounded w-20"></div>
          </div>
        </div>

        {/* Icon skeleton */}
        <div className="flex-shrink-0">
          <div className="w-6 h-6 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  )
}

export const ArticleListSkeleton = ({ count = 5 }: { count?: number }) => {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, index) => (
        <ArticleCardSkeleton key={index} />
      ))}
    </div>
  )
}

export const ArticleDetailSkeleton = () => {
  return (
    <div className="animate-pulse">
      {/* Header skeleton */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
        <div className="h-4 bg-gray-200 rounded w-32 mt-4"></div>
      </div>

      {/* Version timeline skeleton */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="h-6 bg-gray-200 rounded w-40 mb-4"></div>
        <div className="space-y-3">
          {Array.from({ length: 2 }).map((_, index) => (
            <div key={index} className="flex items-start p-3 rounded-lg bg-gray-50">
              <div className="w-24 h-8 bg-gray-200 rounded"></div>
              <div className="flex-1 ml-4 space-y-2">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Version selector skeleton */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="h-6 bg-gray-200 rounded w-40 mb-4"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="h-10 bg-gray-200 rounded"></div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>

      {/* Diff skeleton */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
        <div className="space-y-2">
          {Array.from({ length: 5 }).map((_, index) => (
            <div key={index} className="h-16 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    </div>
  )
}
