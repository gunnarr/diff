import type { ArticleListItem } from '../../types'
import { ArticleCard } from './ArticleCard'

interface ArticleListProps {
  articles: ArticleListItem[]
}

export const ArticleList = ({ articles }: ArticleListProps) => {
  if (articles.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Inga artiklar hittades</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  )
}
