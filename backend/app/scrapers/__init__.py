"""Scrapers for different news sources."""
from app.scrapers.base import BaseScraper
from app.scrapers.svt import SVTNyheterScraper
from app.scrapers.sr import SverigesRadioScraper
from app.scrapers.svd import SvenskaDagbladetScraper
from app.scrapers.aftonbladet import AftonbladetScraper
from app.scrapers.nrk import NRKScraper
from app.scrapers.dr import DRScraper
from app.scrapers.generic import GenericRSSScraper

__all__ = [
    "BaseScraper",
    "SVTNyheterScraper",
    "SverigesRadioScraper",
    "SvenskaDagbladetScraper",
    "AftonbladetScraper",
    "NRKScraper",
    "DRScraper",
    "GenericRSSScraper"
]
