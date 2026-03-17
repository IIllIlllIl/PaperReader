"""
Cache Manager for PaperReader

Caches AI analysis results to avoid redundant API calls
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching of AI analysis results"""

    def __init__(self, cache_dir: str = "./runtime/cache", ttl: int = 604800):
        """
        Initialize cache manager

        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live in seconds (default: 7 days)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self.enabled = True

    def get_cached_analysis(self, pdf_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached analysis if it exists and is not expired

        Args:
            pdf_hash: MD5 hash of the PDF file

        Returns:
            Cached analysis data or None if not found/expired
        """
        if not self.enabled:
            return None

        cache_file = self._get_cache_path(pdf_hash)

        if not cache_file.exists():
            logger.debug(f"No cache found for hash: {pdf_hash}")
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            # Check if cache is expired
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time > timedelta(seconds=self.ttl):
                logger.debug(f"Cache expired for hash: {pdf_hash}")
                cache_file.unlink()  # Delete expired cache
                return None

            logger.info(f"Cache hit for hash: {pdf_hash}")
            return cached_data['analysis']

        except Exception as e:
            logger.warning(f"Failed to read cache: {e}")
            return None

    def save_analysis(self, pdf_hash: str, analysis: Dict[str, Any],
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Save analysis result to cache

        Args:
            pdf_hash: MD5 hash of the PDF file
            analysis: Analysis result to cache
            metadata: Optional metadata (e.g., model used, tokens)
        """
        if not self.enabled:
            return

        cache_file = self._get_cache_path(pdf_hash)

        try:
            cache_data = {
                'hash': pdf_hash,
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis,
                'metadata': metadata or {}
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved analysis to cache: {pdf_hash}")

        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")

    def clear_cache(self) -> int:
        """
        Clear all cached files

        Returns:
            Number of cache files deleted
        """
        count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1

            logger.info(f"Cleared {count} cache files")
            return count

        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return count

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        try:
            cache_files = list(self.cache_dir.glob("*.json"))

            total_size = sum(f.stat().st_size for f in cache_files)

            valid_files = 0
            expired_files = 0

            for cache_file in cache_files:
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)

                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    if datetime.now() - cached_time > timedelta(seconds=self.ttl):
                        expired_files += 1
                    else:
                        valid_files += 1

                except:
                    expired_files += 1

            return {
                'total_files': len(cache_files),
                'valid_files': valid_files,
                'expired_files': expired_files,
                'total_size_mb': total_size / (1024 * 1024),
            }

        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {
                'total_files': 0,
                'valid_files': 0,
                'expired_files': 0,
                'total_size_mb': 0,
            }

    def cleanup_expired(self) -> int:
        """
        Remove expired cache files

        Returns:
            Number of files removed
        """
        count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)

                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    if datetime.now() - cached_time > timedelta(seconds=self.ttl):
                        cache_file.unlink()
                        count += 1

                except:
                    # If we can't read it, delete it
                    cache_file.unlink()
                    count += 1

            logger.info(f"Cleaned up {count} expired cache files")
            return count

        except Exception as e:
            logger.error(f"Failed to cleanup expired cache: {e}")
            return count

    def _get_cache_path(self, pdf_hash: str) -> Path:
        """Get cache file path for a given hash"""
        return self.cache_dir / f"{pdf_hash}.json"

    def enable(self):
        """Enable caching"""
        self.enabled = True
        logger.info("Cache enabled")

    def disable(self):
        """Disable caching"""
        self.enabled = False
        logger.info("Cache disabled")
