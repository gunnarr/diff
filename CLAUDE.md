# CLAUDE.md - AI Assistant Guide for Swedish NewsDiff Tracker

## Project Overview

Swedish NewsDiff Tracker is a full-stack web application that tracks changes in Swedish news articles over time. It automatically scrapes news articles from Swedish news sources (primarily SVT Nyheter), stores multiple versions, and displays diffs showing what changed between versions.

**Tech Stack:**
- Backend: FastAPI (Python 3.11+) with SQLAlchemy async ORM
- Frontend: React 18 + TypeScript + Vite + TailwindCSS
- Database: PostgreSQL (production) / SQLite (development)
- Deployment: Railway.app (backend) + Vercel (frontend)

## Repository Structure

```
/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── config.py        # Pydantic settings
│   │   ├── database.py      # SQLAlchemy async setup
│   │   ├── models/          # ORM models (Article, ArticleVersion, NewsSource)
│   │   ├── api/v1/          # API endpoints
│   │   ├── scrapers/        # Web scrapers (base.py, svt.py, generic.py)
│   │   ├── services/        # Business logic (scraper_service, diff_service)
│   │   ├── schemas/         # Pydantic response schemas
│   │   └── core/scheduler.py # APScheduler job scheduling
│   ├── tests/               # pytest test files
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React TypeScript frontend
│   ├── src/
│   │   ├── api/             # Axios HTTP client
│   │   ├── components/      # React components by feature
│   │   ├── pages/           # Route-level components
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript interfaces
│   ├── package.json         # npm dependencies
│   └── vite.config.ts       # Vite configuration
│
└── CLAUDE.md               # This file
```

## Quick Commands

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server (with hot reload)
uvicorn app.main:app --reload

# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v --tb=short

# Run tests with JSON report
pytest tests/ -v --tb=short --json-report --json-report-file=/tmp/test-report.json
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Architecture Patterns

### Backend Architecture

**Database Models (SQLAlchemy):**
- `NewsSource` - News sources to scrape (name, base_url, scraper_class, intervals)
- `Article` - Tracked articles (url, title, timestamps, version_count)
- `ArticleVersion` - Article snapshots (content, content_hash, captured_at)

**Scraping Pipeline:**
1. APScheduler triggers `scrape_source_job()` every 15 minutes
2. `ScraperService.scrape_source()` orchestrates the scrape
3. Scraper discovers articles via RSS feeds + sitemap parsing
4. 8 concurrent workers process articles with 1-second delays
5. New versions created only when content_hash (SHA256) differs

**Key Backend Files:**
- `app/main.py` - FastAPI app setup, startup events
- `app/scrapers/svt.py` - SVT Nyheter scraper implementation
- `app/services/scraper_service.py` - Main scraping orchestration
- `app/services/diff_service.py` - Word-level diff generation
- `app/core/scheduler.py` - APScheduler configuration

### Frontend Architecture

**State Management:**
- TanStack Query (React Query) for server state caching
- Local useState for UI state

**Key Routes:**
- `/` - Article list with search and filters
- `/articles/:id` - Article detail with diff viewer
- `/livelog` - Real-time backend logs

**Key Components:**
- `components/article/` - ArticleCard, ArticleMetadata, ArticleContent
- `components/diff/` - DiffViewer, SideBySideDiff, DiffStats
- `components/common/` - CountdownTimer, LoadingSkeleton

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/api/v1/sources` | List news sources |
| POST | `/api/v1/sources/{id}/scrape` | Manual scrape trigger |
| GET | `/api/v1/articles` | List articles (paginated) |
| GET | `/api/v1/articles/{id}` | Article with all versions |
| GET | `/api/v1/diff/{id}` | Diff between versions |
| GET | `/api/v1/stats` | System statistics |
| GET | `/api/v1/next-scrape` | Next scheduled scrape |
| GET | `/api/v1/logs` | Backend logs |
| POST | `/api/v1/run-tests` | Execute system tests |

## Code Conventions

### Python (Backend)

**Naming:**
- Models: PascalCase (`Article`, `ArticleVersion`)
- Functions: snake_case (`get_articles`, `_normalize_url`)
- Private functions: leading underscore (`_process_article`)
- Constants: UPPER_SNAKE_CASE

**Async Patterns:**
```python
# Always use async/await for database operations
async with async_session() as session:
    result = await session.execute(select(Article))
    articles = result.scalars().all()

# Use Semaphore for concurrency control
semaphore = asyncio.Semaphore(8)
async def process_with_limit(url):
    async with semaphore:
        # Do work
        pass
```

**Error Handling:**
- Use `HTTPException` for API errors with appropriate status codes
- Log errors with Python's `logging` module
- Provide fallback behavior where possible

### TypeScript/React (Frontend)

**Naming:**
- Components: PascalCase (`ArticleCard.tsx`)
- Hooks: useCamelCase (`useDarkMode`)
- Props interfaces: `ComponentNameProps`

**Component Pattern:**
```typescript
interface ArticleCardProps {
  article: Article;
  onClick?: () => void;
}

export function ArticleCard({ article, onClick }: ArticleCardProps) {
  // Component implementation
}
```

**API Calls:**
```typescript
// Use TanStack Query for data fetching
const { data, isLoading, error } = useQuery({
  queryKey: ['articles', filters],
  queryFn: () => articlesApi.getArticles(filters)
});
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db  # Required in production
CORS_ORIGINS=["https://frontend.vercel.app"]             # Frontend URLs
ENVIRONMENT=production                                    # or development
DEBUG=False
LOG_LEVEL=INFO
USER_AGENT=NewsDiffBot/1.0
```

### Frontend
```
VITE_API_URL=https://backend.railway.app/api/v1  # Backend URL
```

## Testing

**Backend tests are in `/backend/tests/`**

Test coverage includes:
- API health checks
- Database connectivity
- News source configuration
- Article existence
- Scraper configuration validation
- URL validation

Tests run automatically daily at 03:00 UTC via APScheduler.

## Important Implementation Details

### Content Extraction
- Primary: `trafilatura` library for intelligent extraction
- Fallback: Custom BeautifulSoup extraction if trafilatura fails
- Content validated: Minimum length, no live article indicators

### URL Handling
- URLs are normalized (remove fragments, standardize trailing slashes)
- Canonical URLs extracted from meta tags
- Articles matched by normalized URL to prevent duplicates

### Version Detection
- Content hashed with SHA256
- New version created only when hash differs from latest
- Word count tracked for change metrics

### Rate Limiting
- 1-second delay between article fetches
- 8 concurrent workers maximum
- Respects server resources

## Common Tasks

### Adding a New News Source
1. Create scraper class in `backend/app/scrapers/` extending `BaseScraper`
2. Implement `get_rss_urls()` and customize extraction if needed
3. Add source to database via API or `seed_sources.py`

### Modifying the Diff Algorithm
Edit `backend/app/services/diff_service.py` - uses `difflib.SequenceMatcher`

### Adding Frontend Features
1. Add types to `frontend/src/types/`
2. Add API methods to `frontend/src/api/`
3. Create components in `frontend/src/components/`
4. Add routes in `frontend/src/App.tsx`

### Database Migrations
Currently no migration tool - schema changes require manual database updates or recreation.

## Deployment

### Backend (Railway.app)
- Auto-deploys from GitHub on push
- Root directory: `/backend`
- Uses NIXPACKS builder
- Requires PostgreSQL addon

### Frontend (Vercel)
- Auto-deploys from GitHub on push
- Root directory: `/frontend`
- Set `VITE_API_URL` environment variable

## Troubleshooting

**No articles being scraped:**
- Check `/api/v1/sources` - ensure source is active
- Check `/api/v1/logs` for error messages
- Verify RSS feeds are accessible

**Database connection errors:**
- Verify `DATABASE_URL` format (must use `postgresql+asyncpg://`)
- Check network connectivity to database

**CORS errors:**
- Update `CORS_ORIGINS` in backend config
- Ensure frontend URL is in the allowed list

**Tests failing:**
- Run `pytest tests/ -v` for detailed output
- Check database connectivity
- Ensure sources are seeded
