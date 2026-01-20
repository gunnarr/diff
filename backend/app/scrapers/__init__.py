"""Scrapers for different news sources."""
from app.scrapers.base import BaseScraper
from app.scrapers.svt import SVTNyheterScraper
from app.scrapers.generic import GenericRSSScraper

__all__ = [
    "BaseScraper",
    "SVTNyheterScraper",
    "GenericRSSScraper"
]
