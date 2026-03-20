"""Citation analysis configuration."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CitationConfig:
    """Configuration for citation analysis."""

    # API settings
    enable_openalex: bool = True
    enable_semantic_scholar: bool = True
    enable_opencitations: bool = True

    # Verification settings
    min_sources: int = 2  # Minimum sources for verification
    max_citations: int = 200  # Max citations to fetch per source
    display_citations: int = 10  # Citations to display in slides

    # Cache settings
    cache_dir: str = "outputs/citations"
    cache_days: int = 7

    # Chart settings
    generate_year_chart: bool = True
    generate_coverage_chart: bool = True
    generate_network_chart: bool = False  # Disabled by default (requires networkx)

    # Performance settings
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

    @classmethod
    def from_dict(cls, config_dict: dict):
        """Create config from dictionary"""
        return cls(**{k: v for k, v in config_dict.items()
                      if k in cls.__dataclass_fields__})

    @classmethod
    def default(cls):
        """Create default config"""
        return cls()
