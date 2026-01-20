"""Create a test version to demonstrate diff functionality."""
import asyncio
from datetime import datetime
from app.database import async_session
from app.models import Article, ArticleVersion
from app.utils.hash import content_hash
from app.core.text_utils import count_words
from sqlalchemy import select


async def create_test_version():
    """Create a modified version of article 1 for testing."""
    async with async_session() as db:
        # Get article 1
        result = await db.execute(
            select(Article).where(Article.id == 1)
        )
        article = result.scalar_one()

        # Get current version
        result = await db.execute(
            select(ArticleVersion)
            .where(ArticleVersion.article_id == 1)
            .order_by(ArticleVersion.version_number.desc())
            .limit(1)
        )
        current_version = result.scalar_one()

        # Create modified content
        modified_content = current_version.content.replace(
            "Emil Jonsson",
            "den svenske resenären Emil Jonsson"
        )
        modified_content = modified_content + " Han är nu tillbaka i sitt hem och återhämtar sig."

        modified_title = current_version.title.replace("Emil", "Svenska Emil")

        # Create new version
        new_version = ArticleVersion(
            article_id=article.id,
            version_number=2,
            title=modified_title,
            byline=current_version.byline,
            content=modified_content,
            content_hash=content_hash(modified_content),
            captured_at=datetime.utcnow(),
            word_count=count_words(modified_content),
            meta_description=current_version.meta_description,
            meta_keywords=current_version.meta_keywords,
            published_date=current_version.published_date,
            modified_date=datetime.utcnow()
        )

        db.add(new_version)

        # Update article
        article.version_count = 2
        article.last_modified_at = datetime.utcnow()
        article.title = modified_title

        await db.commit()

        print("✅ Created test version 2 for article 1")
        print(f"Title changed: {current_version.title} -> {modified_title}")
        print(f"Word count: {current_version.word_count} -> {new_version.word_count}")


if __name__ == "__main__":
    asyncio.run(create_test_version())
