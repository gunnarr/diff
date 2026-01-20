#!/bin/bash
# Smart auto-push script med intelligenta commit-meddelanden

cd /Users/gunnar/diff

# Lägg till alla ändringar
git add .

# Kolla om det finns något att committa
if git diff --staged --quiet; then
  echo "✓ Inga ändringar att pusha"
  exit 0
fi

# Analysera vilka filer som ändrats
CHANGED_FILES=$(git diff --staged --name-only)
BACKEND_CHANGES=$(echo "$CHANGED_FILES" | grep "^backend/" | wc -l)
FRONTEND_CHANGES=$(echo "$CHANGED_FILES" | grep "^frontend/" | wc -l)

# Skapa intelligent commit-meddelande
COMMIT_MSG=""

# Backend-ändringar
if [ $BACKEND_CHANGES -gt 0 ]; then
  if echo "$CHANGED_FILES" | grep -q "scrapers/"; then
    COMMIT_MSG="Improve news scrapers"
  elif echo "$CHANGED_FILES" | grep -q "models/"; then
    COMMIT_MSG="Update database models"
  elif echo "$CHANGED_FILES" | grep -q "api/"; then
    COMMIT_MSG="Update API endpoints"
  elif echo "$CHANGED_FILES" | grep -q "config.py"; then
    COMMIT_MSG="Update backend configuration"
  elif echo "$CHANGED_FILES" | grep -q "requirements.txt"; then
    COMMIT_MSG="Update backend dependencies"
  else
    COMMIT_MSG="Update backend code"
  fi
fi

# Frontend-ändringar
if [ $FRONTEND_CHANGES -gt 0 ]; then
  if echo "$CHANGED_FILES" | grep -q "components/"; then
    if [ -n "$COMMIT_MSG" ]; then
      COMMIT_MSG="$COMMIT_MSG and UI components"
    else
      COMMIT_MSG="Update UI components"
    fi
  elif echo "$CHANGED_FILES" | grep -q "pages/"; then
    if [ -n "$COMMIT_MSG" ]; then
      COMMIT_MSG="$COMMIT_MSG and pages"
    else
      COMMIT_MSG="Update pages"
    fi
  elif echo "$CHANGED_FILES" | grep -q "styles\|\.css"; then
    if [ -n "$COMMIT_MSG" ]; then
      COMMIT_MSG="$COMMIT_MSG and styling"
    else
      COMMIT_MSG="Update styling"
    fi
  elif echo "$CHANGED_FILES" | grep -q "package.json"; then
    if [ -n "$COMMIT_MSG" ]; then
      COMMIT_MSG="$COMMIT_MSG and frontend dependencies"
    else
      COMMIT_MSG="Update frontend dependencies"
    fi
  else
    if [ -n "$COMMIT_MSG" ]; then
      COMMIT_MSG="$COMMIT_MSG and frontend code"
    else
      COMMIT_MSG="Update frontend code"
    fi
  fi
fi

# Om både backend och frontend ändrats
if [ $BACKEND_CHANGES -gt 0 ] && [ $FRONTEND_CHANGES -gt 0 ]; then
  COMMIT_MSG="Update backend and frontend"
fi

# Fallback om inget matchade
if [ -z "$COMMIT_MSG" ]; then
  COMMIT_MSG="Update project files"
fi

# Lista ändrade filer för detaljer
FILE_LIST=$(echo "$CHANGED_FILES" | head -5 | sed 's/^/- /')
if [ $(echo "$CHANGED_FILES" | wc -l) -gt 5 ]; then
  FILE_LIST="$FILE_LIST
- ... and $(( $(echo "$CHANGED_FILES" | wc -l) - 5 )) more files"
fi

# Skapa full commit-meddelande
FULL_MSG="$COMMIT_MSG

$FILE_LIST

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Commit
git commit -m "$FULL_MSG"

# Pusha till GitHub
git push

echo ""
echo "✅ Pushade till GitHub med meddelande:"
echo "   $COMMIT_MSG"
echo ""
