"""
Tests for Cache Manager
"""

import pytest
import tempfile
import json
from pathlib import Path
from src.cache_manager import CacheManager


class TestCacheManager:
    """Test cache manager"""

    def test_cache_init(self, tmp_path):
        """Test cache manager initialization"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        assert manager.cache_dir == cache_dir
        assert manager.enabled is True

    def test_save_and_get_cache(self, tmp_path):
        """Test saving and retrieving cached data"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        # Save analysis
        test_hash = "abc123"
        test_analysis = {"title": "Test Paper", "problem": "Test problem"}

        manager.save_analysis(test_hash, test_analysis)

        # Retrieve cached analysis
        cached = manager.get_cached_analysis(test_hash)

        assert cached is not None
        assert cached == test_analysis

    def test_cache_not_found(self, tmp_path):
        """Test retrieving non-existent cache"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        cached = manager.get_cached_analysis("nonexistent")

        assert cached is None

    def test_cache_disable(self, tmp_path):
        """Test disabling cache"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        manager.disable()

        assert manager.enabled is False

        # Save should not work
        manager.save_analysis("test", {"data": "test"})

        cached = manager.get_cached_analysis("test")
        assert cached is None

    def test_clear_cache(self, tmp_path):
        """Test clearing cache"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        # Add some cached data
        manager.save_analysis("hash1", {"data": "1"})
        manager.save_analysis("hash2", {"data": "2"})

        # Clear cache
        count = manager.clear_cache()

        assert count == 2

        # Verify cleared
        assert manager.get_cached_analysis("hash1") is None
        assert manager.get_cached_analysis("hash2") is None

    def test_cache_stats(self, tmp_path):
        """Test cache statistics"""
        cache_dir = tmp_path / "cache"
        manager = CacheManager(cache_dir=str(cache_dir))

        # Add some cached data
        manager.save_analysis("hash1", {"data": "test"})

        stats = manager.get_cache_stats()

        assert 'total_files' in stats
        assert 'valid_files' in stats
        assert 'expired_files' in stats
        assert 'total_size_mb' in stats
        assert stats['total_files'] >= 1
