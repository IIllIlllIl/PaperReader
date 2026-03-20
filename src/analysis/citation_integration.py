"""
Citation analysis integration module.
Provides high-level interface for adding citation analysis to PaperReader pipeline.
"""

import logging
from typing import Dict, Optional
from pathlib import Path

from .citation_analyzer import CitationAnalyzer
from ..visualization.citation_charts import CitationChartGenerator
from ..config.citation_config import CitationConfig

logger = logging.getLogger(__name__)


class CitationIntegrator:
    """
    High-level interface for citation analysis integration.
    Handles analysis, visualization, and error handling.
    """

    def __init__(self, config: Optional[CitationConfig] = None):
        """
        Initialize citation integrator.

        Args:
            config: CitationConfig object (uses default if None)
        """
        self.config = config or CitationConfig.default()
        self.analyzer = CitationAnalyzer(
            cache_dir=self.config.cache_dir,
            cache_days=self.config.cache_days
        )
        self.chart_generator = CitationChartGenerator(
            output_dir="outputs/intermediates/images/citations"
        )

        # Initialize sources
        if self.config.enable_semantic_scholar:
            try:
                self.analyzer.setup_semantic_scholar()
                logger.info("Semantic Scholar initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Semantic Scholar: {e}")

    def analyze_paper_citations(self, paper_title: str,
                                 authors: str = None,
                                 year: int = None) -> Optional[Dict]:
        """
        Analyze paper citations with full pipeline.

        Args:
            paper_title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            Complete citation analysis result with charts, or None if failed
        """
        if not paper_title:
            logger.warning("No paper title provided for citation analysis")
            return None

        try:
            logger.info(f"Starting citation analysis for: {paper_title}")

            # Perform multi-source analysis
            result = self.analyzer.analyze_citations_multisource(
                paper_title=paper_title,
                authors=authors,
                year=year,
                min_sources=self.config.min_sources
            )

            # Check if we have meaningful results
            if result['total_citations'] == 0:
                logger.info("No verified citations found")
                return result

            # Add paper metadata to result
            result['paper_title'] = paper_title
            result['paper_year'] = year

            # Generate visualizations
            if self.config.generate_year_chart or self.config.generate_coverage_chart:
                charts = self.chart_generator.generate_summary_chart(result)
                result['charts'] = charts
                logger.info(f"Generated {len(charts)} visualization charts")

            # Log summary
            logger.info(f"Citation analysis complete: {result['total_citations']} verified citations")
            logger.info(f"Source coverage: {result['by_source_coverage']}")

            return result

        except Exception as e:
            logger.error(f"Citation analysis failed: {e}")
            return None

    def add_citation_to_analysis(self, analysis, paper_title: str,
                                  authors: str = None, year: int = None) -> bool:
        """
        Add citation data to PaperAnalysis object.

        Args:
            analysis: PaperAnalysis object to enhance
            paper_title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Perform analysis
            citation_data = self.analyze_paper_citations(
                paper_title=paper_title,
                authors=authors,
                year=year
            )

            if citation_data:
                analysis.citation_data = citation_data
                analysis.has_citation_data = citation_data['total_citations'] > 0
                logger.info(f"Added citation data to analysis: {citation_data['total_citations']} citations")
                return True
            else:
                analysis.citation_data = None
                analysis.has_citation_data = False
                return False

        except Exception as e:
            logger.error(f"Failed to add citation data to analysis: {e}")
            analysis.citation_data = None
            analysis.has_citation_data = False
            return False

    def get_citation_summary(self, citation_data: Dict) -> str:
        """
        Generate text summary of citation data.

        Args:
            citation_data: Citation analysis result

        Returns:
            Text summary
        """
        if not citation_data or citation_data['total_citations'] == 0:
            return "No verified citations found."

        summary_parts = [
            f"Total verified citations: {citation_data['total_citations']}",
            f"Data sources: {', '.join(citation_data['sources_used'])}",
            f"Verification threshold: ≥{citation_data['min_sources_required']} sources"
        ]

        if citation_data.get('by_year'):
            years = sorted(citation_data['by_year'].keys())
            if years:
                summary_parts.append(f"Year range: {years[0]}-{years[-1]}")

        return ". ".join(summary_parts)
