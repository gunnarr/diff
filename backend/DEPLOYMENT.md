# Deployment Guide - Swedish NewsDiff Tracker

## Railway Deployment (Backend + Database)

### Prerequisites
- Railway account (https://railway.app/)
- GitHub repository with your code

### Step 1: Create Railway Project

1. Go to https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select your repository
5. Choose the `backend` directory as root (if needed)

### Step 2: Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically added

### Step 3: Configure Environment Variables

In Railway project settings → Variables, add:

```
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
LOG_LEVEL=INFO
USER_AGENT=NewsDiffBot/1.0 (your-email@example.com)
```

**Note:** `DATABASE_URL` is automatically set by Railway's PostgreSQL plugin.

### Step 4: Deploy

1. Railway will automatically detect the `Procfile` and deploy
2. Wait for deployment to complete
3. Copy your Railway app URL (e.g., `https://your-app.up.railway.app`)

### Step 5: Verify Deployment

Test these endpoints:
- `https://your-app.up.railway.app/` - Should return app info
- `https://your-app.up.railway.app/health` - Should return healthy status
- `https://your-app.up.railway.app/api/v1/sources` - Should return news sources

---

## Vercel Deployment (Frontend)

### Prerequisites
- Vercel account (https://vercel.com/)
- Railway backend URL from previous steps

### Step 1: Prepare Frontend

1. Update frontend environment variable
2. The backend URL will be configured in Vercel

### Step 2: Deploy to Vercel

1. Go to https://vercel.com/
2. Click "Add New" → "Project"
3. Import your Git repository
4. Select the `frontend` directory as root
5. Vercel auto-detects Vite configuration

### Step 3: Configure Environment Variables

In Vercel project settings → Environment Variables, add:

```
VITE_API_URL=https://your-app.up.railway.app/api/v1
```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Copy your Vercel URL (e.g., `https://your-app.vercel.app`)

### Step 5: Update CORS in Railway

1. Go back to Railway project
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ```
3. Railway will automatically redeploy

---

## Post-Deployment

### Monitor Scraping

Check Railway logs to ensure scrapers are running:
```
Scheduler setup complete
Starting scraper for source: SVT Nyheter
```

### Verify Functionality

1. Visit your Vercel frontend URL
2. Check that articles are loading
3. Toggle dark mode
4. Switch language (SV/EN)
5. Click on an article to see versions

### Database Backup

Railway provides automatic daily backups for PostgreSQL.
To manually backup:
1. Go to Railway → PostgreSQL service
2. Click "Backups" tab
3. Click "Create Backup"

---

## Troubleshooting

### Backend Issues

**503 Service Unavailable**
- Check Railway logs for errors
- Verify `DATABASE_URL` is set correctly
- Check if PostgreSQL service is running

**CORS Errors**
- Verify `CORS_ORIGINS` includes your Vercel URL
- Ensure URL format is correct (no trailing slash)

**Scraper Not Running**
- Check Railway logs for scheduler errors
- Verify all dependencies are installed

### Frontend Issues

**API Errors**
- Verify `VITE_API_URL` is set correctly in Vercel
- Check Railway backend is running
- Test backend endpoints directly

**Build Failures**
- Check Vercel build logs
- Verify all npm dependencies are in package.json

---

## Cost Estimate

- **Railway Hobby**: ~$5-10/month (backend + PostgreSQL)
- **Vercel Free Tier**: $0/month (sufficient for this app)

**Total**: ~$5-10/month
