"""Logs endpoints."""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

router = APIRouter()


class LogEntry(BaseModel):
    """Log entry."""
    timestamp: str
    level: str
    message: str


class LogsResponse(BaseModel):
    """Logs response."""
    logs: List[LogEntry]
    total_lines: int


def parse_log_line(line: str) -> Optional[LogEntry]:
    """Parse a log line into structured format."""
    try:
        # Format: 2026-01-21 11:49:31,733 - module - LEVEL - message
        if not line.strip():
            return None
            
        parts = line.split(' - ', 3)
        if len(parts) < 4:
            return None
            
        timestamp = parts[0].strip()
        # module = parts[1].strip()
        level = parts[2].strip()
        message = parts[3].strip()
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message
        )
    except Exception:
        return None


@router.get("/logs", response_model=LogsResponse)
async def get_logs(
    limit: int = Query(100, ge=1, le=1000, description="Number of log lines to return"),
    filter_scraping: bool = Query(True, description="Filter to only show scraping-related logs")
):
    """Get recent logs from the backend."""
    
    log_file = "backend.log"
    
    if not os.path.exists(log_file):
        return LogsResponse(logs=[], total_lines=0)
    
    try:
        # Read last N lines from log file
        with open(log_file, 'r', encoding='utf-8') as f:
            # Read all lines and get the last ones
            all_lines = f.readlines()
            recent_lines = all_lines[-limit*3:] if len(all_lines) > limit*3 else all_lines
        
        parsed_logs = []
        
        # Keywords to identify scraping-related logs
        scraping_keywords = [
            'scrape', 'scraper', 'discover', 'fetch', 'article',
            'scheduler', 'job', 'SVT', 'httpx', 'trafilatura'
        ]
        
        # Filter logs to exclude HTTP API requests
        exclude_keywords = [
            'GET /api', 'POST /api', 'PUT /api', 'DELETE /api',
            'HTTP/1.1', '127.0.0.1', 'localhost'
        ]
        
        for line in recent_lines:
            # Skip lines with exclude keywords
            if any(keyword in line for keyword in exclude_keywords):
                continue
                
            # If filtering, only include scraping-related logs
            if filter_scraping:
                if not any(keyword.lower() in line.lower() for keyword in scraping_keywords):
                    continue
            
            entry = parse_log_line(line)
            if entry:
                parsed_logs.append(entry)
        
        # Return most recent logs first
        parsed_logs = parsed_logs[-limit:]
        parsed_logs.reverse()
        
        return LogsResponse(
            logs=parsed_logs,
            total_lines=len(parsed_logs)
        )
        
    except Exception as e:
        return LogsResponse(
            logs=[LogEntry(
                timestamp=datetime.now().isoformat(),
                level="ERROR",
                message=f"Failed to read logs: {str(e)}"
            )],
            total_lines=1
        )
