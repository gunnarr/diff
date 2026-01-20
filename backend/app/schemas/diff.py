"""Diff schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal, Dict, Any


class DiffChange(BaseModel):
    """Single diff change."""
    type: Literal['delete', 'insert', 'equal']
    content: List[str]
    position: int


class DiffStats(BaseModel):
    """Diff statistics."""
    words_added: int
    words_removed: int
    net_change: int
    title_changed: bool


class VersionInfo(BaseModel):
    """Version information for diff."""
    id: int
    version_number: int
    title: str
    captured_at: datetime
    word_count: int


class DiffResponse(BaseModel):
    """Diff response between two versions."""
    article_id: int
    from_version: VersionInfo
    to_version: VersionInfo
    title_diff: Dict[str, Any]
    content_diff: List[DiffChange]
    stats: DiffStats
