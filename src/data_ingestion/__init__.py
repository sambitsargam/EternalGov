"""
Data Ingestion Layer for EternalGov
Collects governance data from public sources: Snapshot, forums, Twitter, blogs
"""

from .snapshot_scraper import SnapshotScraper
from .forum_scraper import ForumScraper
from .twitter_scraper import TwitterScraper
from .blog_scraper import BlogScraper
from .data_aggregator import DataAggregator

__all__ = [
    "SnapshotScraper",
    "ForumScraper",
    "TwitterScraper",
    "BlogScraper",
    "DataAggregator",
]
