"""
Citation data visualization module.
Generates charts for citation analysis slides.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Headless mode
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CitationChartGenerator:
    """Generate charts for citation analysis."""

    def __init__(self, output_dir: str = "outputs/images/citations"):
        """
        Initialize chart generator.

        Args:
            output_dir: Directory to save generated charts
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set style
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            plt.style.use('seaborn-whitegrid')

        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A4C93']

    def generate_year_trend_chart(self, by_year: Dict[int, int],
                                   paper_year: int = None) -> Optional[str]:
        """
        Generate year trend bar chart.

        Args:
            by_year: Year -> citation count mapping
            paper_year: Paper publication year (for annotation)

        Returns:
            Chart file path or None if failed
        """
        if not by_year:
            logger.warning("No year data for chart generation")
            return None

        try:
            years = sorted(by_year.keys())
            counts = [by_year[y] for y in years]

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(years, counts, color=self.colors[0], alpha=0.8, width=0.8)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom', fontsize=10)

            # Add vertical line for paper publication year
            if paper_year and paper_year in years:
                ax.axvline(x=paper_year, color='red', linestyle='--', alpha=0.5,
                          label=f'Paper published ({paper_year})')
                ax.legend()

            ax.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Citations', fontsize=12, fontweight='bold')
            ax.set_title('Citation Trend by Year', fontsize=14, fontweight='bold')

            # Set x-axis ticks to show all years
            ax.set_xticks(years)
            ax.set_xticklabels(years, rotation=45, ha='right')

            # Save chart
            filename = self.output_dir / f"citation_trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.tight_layout()
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Generated year trend chart: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"Failed to generate year trend chart: {e}")
            return None

    def generate_source_coverage_chart(self, coverage: Dict[str, int]) -> Optional[str]:
        """
        Generate source coverage pie chart.

        Args:
            coverage: Source name -> verified citation count mapping

        Returns:
            Chart file path or None if failed
        """
        if not coverage:
            logger.warning("No coverage data for chart generation")
            return None

        try:
            sources = list(coverage.keys())
            counts = list(coverage.values())

            # Filter out zero counts
            non_zero = [(s, c) for s, c in zip(sources, counts) if c > 0]
            if not non_zero:
                return None

            sources, counts = zip(*non_zero)

            fig, ax = plt.subplots(figsize=(8, 6))
            wedges, texts, autotexts = ax.pie(
                counts,
                labels=sources,
                autopct='%1.1f%%',
                colors=self.colors[:len(sources)],
                startangle=90
            )

            # Beautify
            for text in texts:
                text.set_fontsize(11)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            ax.set_title('Citation Source Coverage', fontsize=14, fontweight='bold')

            # Save chart
            filename = self.output_dir / f"source_coverage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.tight_layout()
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Generated source coverage chart: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"Failed to generate source coverage chart: {e}")
            return None

    def generate_citation_network(self, citations: List[Dict],
                                   paper_title: str, max_nodes: int = 20) -> Optional[str]:
        """
        Generate simplified citation network diagram.

        Args:
            citations: Citation list
            paper_title: Original paper title
            max_nodes: Maximum number of nodes to display

        Returns:
            Chart file path or None if failed
        """
        if not citations:
            logger.warning("No citation data for network generation")
            return None

        try:
            import networkx as nx

            # Limit nodes
            top_citations = citations[:max_nodes]

            G = nx.DiGraph()

            # Add center node (original paper)
            center = "This Paper"
            G.add_node(center, size=3000)

            # Add citation nodes
            for i, cit in enumerate(top_citations):
                node_id = f"cit_{i}"
                title = cit.get('title', 'Unknown')
                title_short = title[:30] + '...' if len(title) > 30 else title
                G.add_node(node_id, label=title_short, size=1000)
                G.add_edge(center, node_id)

            # Draw
            fig, ax = plt.subplots(figsize=(12, 8))
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

            # Node sizes
            node_sizes = [G.nodes[n].get('size', 1000) for n in G.nodes]

            # Draw
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                                  node_color=self.colors[:len(G.nodes)], alpha=0.9, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=ax)

            # Labels
            labels = {n: G.nodes[n].get('label', n) for n in G.nodes}
            nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)

            ax.set_title('Citation Network (Top Cited Works)', fontsize=14, fontweight='bold')
            ax.axis('off')

            # Save
            filename = self.output_dir / f"citation_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.tight_layout()
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Generated citation network: {filename}")
            return str(filename)

        except ImportError:
            logger.warning("networkx not installed, skipping network visualization")
            return None
        except Exception as e:
            logger.error(f"Failed to generate citation network: {e}")
            return None

    def generate_summary_chart(self, citation_data: Dict) -> Dict[str, str]:
        """
        Generate all charts for citation analysis.

        Args:
            citation_data: Complete citation analysis result

        Returns:
            Dictionary mapping chart type to file path
        """
        charts = {}

        # Year trend chart
        if citation_data.get('by_year'):
            year_chart = self.generate_year_trend_chart(
                citation_data['by_year'],
                paper_year=citation_data.get('paper_year')
            )
            if year_chart:
                charts['year_trend'] = year_chart

        # Source coverage chart
        if citation_data.get('by_source_coverage'):
            coverage_chart = self.generate_source_coverage_chart(
                citation_data['by_source_coverage']
            )
            if coverage_chart:
                charts['source_coverage'] = coverage_chart

        # Citation network (optional)
        if citation_data.get('citations') and len(citation_data['citations']) > 0:
            network_chart = self.generate_citation_network(
                citation_data['citations'][:10],
                citation_data.get('paper_title', '')
            )
            if network_chart:
                charts['citation_network'] = network_chart

        logger.info(f"Generated {len(charts)} charts for citation analysis")
        return charts
