"""Diff generation service."""
import difflib
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Article, ArticleVersion
from app.schemas.diff import DiffResponse, DiffChange, DiffStats, VersionInfo


class DiffService:
    """Service for generating diffs between article versions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_diff(
        self,
        article_id: int,
        from_version: int,
        to_version: int
    ) -> DiffResponse:
        """Generate diff between two versions of an article."""
        # Get both versions
        result = await self.db.execute(
            select(ArticleVersion)
            .where(
                ArticleVersion.article_id == article_id,
                ArticleVersion.version_number.in_([from_version, to_version])
            )
        )
        versions = result.scalars().all()

        if len(versions) != 2:
            raise ValueError(f"Could not find both versions {from_version} and {to_version}")

        # Sort versions
        v1 = next(v for v in versions if v.version_number == from_version)
        v2 = next(v for v in versions if v.version_number == to_version)

        # Generate content diff
        content_diff = self._generate_word_diff(v1.content, v2.content)

        # Calculate stats
        stats = self._calculate_stats(content_diff, v1.title, v2.title)

        # Generate title diff if changed
        title_diff = {}
        if v1.title != v2.title:
            title_diff = {
                'old': v1.title,
                'new': v2.title
            }

        return DiffResponse(
            article_id=article_id,
            from_version=VersionInfo(
                id=v1.id,
                version_number=v1.version_number,
                title=v1.title or "",
                captured_at=v1.captured_at,
                word_count=v1.word_count or 0
            ),
            to_version=VersionInfo(
                id=v2.id,
                version_number=v2.version_number,
                title=v2.title or "",
                captured_at=v2.captured_at,
                word_count=v2.word_count or 0
            ),
            title_diff=title_diff,
            content_diff=content_diff,
            stats=stats
        )

    def _generate_word_diff(self, old_text: str, new_text: str) -> List[DiffChange]:
        """Generate word-level diff."""
        old_words = old_text.split()
        new_words = new_text.split()

        diff = difflib.SequenceMatcher(None, old_words, new_words)
        changes = []
        position = 0

        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag == 'equal':
                position += (i2 - i1)
            elif tag == 'delete':
                changes.append(DiffChange(
                    type='delete',
                    content=old_words[i1:i2],
                    position=position
                ))
            elif tag == 'insert':
                changes.append(DiffChange(
                    type='insert',
                    content=new_words[j1:j2],
                    position=position
                ))
                position += (j2 - j1)
            elif tag == 'replace':
                changes.append(DiffChange(
                    type='delete',
                    content=old_words[i1:i2],
                    position=position
                ))
                changes.append(DiffChange(
                    type='insert',
                    content=new_words[j1:j2],
                    position=position
                ))
                position += (j2 - j1)

        return changes

    def _calculate_stats(
        self,
        changes: List[DiffChange],
        old_title: str,
        new_title: str
    ) -> DiffStats:
        """Calculate diff statistics."""
        words_added = sum(
            len(change.content)
            for change in changes
            if change.type == 'insert'
        )

        words_removed = sum(
            len(change.content)
            for change in changes
            if change.type == 'delete'
        )

        return DiffStats(
            words_added=words_added,
            words_removed=words_removed,
            net_change=words_added - words_removed,
            title_changed=old_title != new_title
        )
