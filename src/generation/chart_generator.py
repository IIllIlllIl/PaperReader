"""
Chart Generator

Generates charts from extracted numeric results.
"""

import logging
from pathlib import Path
from typing import List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.result_analyzer import ComparisonResult, NumericResult

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generates charts for research presentation"""

    def __init__(self, output_dir: str = "outputs/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Chart style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = [
            '#3498db',  # Blue
            '#e74c3c',  # Red
            '#2ecc71',  # Green
            '#f39c12',  # Orange
            '#9b59b6',  # Purple
        ]

    def generate_comparison_chart(
        self,
        comparison: ComparisonResult,
        chart_name: str = "comparison"
    ) -> Optional[str]:
        """
        Generate comparison bar chart

        Args:
            comparison: ComparisonResult object
            chart_name: Name for the output file

        Returns:
            Path to generated chart image, or None if failed
        """
        logger.info(f"Generating comparison chart: {comparison.metric}")

        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Create bar chart
            x = np.arange(len(comparison.methods))
            bars = ax.bar(x, comparison.values, color=self.colors[:len(comparison.methods)])

            # Customize chart
            ax.set_xlabel('Method / Context', fontsize=12, fontweight='bold')
            ax.set_ylabel(comparison.metric, fontsize=12, fontweight='bold')
            ax.set_title(f'{comparison.metric} Comparison', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(x)
            ax.set_xticklabels(comparison.methods, rotation=0, ha='center')

            # Add value labels on bars
            for bar, value in zip(bars, comparison.values):
                height = bar.get_height()
                label = f'{value:.1f}%' if comparison.is_percentage else f'{value:.1f}'
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height,
                    label,
                    ha='center',
                    va='bottom',
                    fontsize=11,
                    fontweight='bold'
                )

            # Set y-axis limits
            if comparison.is_percentage:
                ax.set_ylim(0, 100)
            else:
                ax.set_ylim(0, max(comparison.values) * 1.2)

            # Grid
            ax.yaxis.grid(True, linestyle='--', alpha=0.7)
            ax.set_axisbelow(True)

            # Tight layout
            plt.tight_layout()

            # Save
            output_path = self.output_dir / f"{chart_name}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

            logger.info(f"✓ Chart saved: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to generate chart: {e}")
            return None

    def generate_multi_metric_chart(
        self,
        results: List[NumericResult],
        chart_name: str = "results"
    ) -> Optional[str]:
        """
        Generate multi-metric comparison chart

        Args:
            results: List of NumericResult objects
            chart_name: Name for output file

        Returns:
            Path to generated chart
        """
        logger.info(f"Generating multi-metric chart with {len(results)} metrics")

        if not results:
            logger.warning("No results to plot")
            return None

        try:
            fig, ax = plt.subplots(figsize=(12, 6))

            # Group by metric
            metrics = [r.metric for r in results]
            values = [r.value for r in results]
            contexts = [r.context for r in results]

            # Create bar chart
            x = np.arange(len(metrics))
            bars = ax.bar(x, values, color=self.colors[:len(metrics)])

            # Customize
            ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
            ax.set_ylabel('Value (%)', fontsize=12, fontweight='bold')
            ax.set_title('Key Results', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(x)

            # Rotate labels if too long
            if any(len(m) > 15 for m in metrics):
                ax.set_xticklabels(metrics, rotation=45, ha='right')
            else:
                ax.set_xticklabels(metrics, rotation=0, ha='center')

            # Add value labels
            for bar, value, context in zip(bars, values, contexts):
                height = bar.get_height()
                label = f'{value:.1f}%'
                if context:
                    label += f'\n({context})'
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height,
                    label,
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    fontweight='bold'
                )

            # Y-axis limits
            max_val = max(values)
            ax.set_ylim(0, max(100, max_val * 1.2))

            # Grid
            ax.yaxis.grid(True, linestyle='--', alpha=0.7)
            ax.set_axisbelow(True)

            # Tight layout
            plt.tight_layout()

            # Save
            output_path = self.output_dir / f"{chart_name}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

            logger.info(f"✓ Multi-metric chart saved: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to generate multi-metric chart: {e}")
            return None

    def generate_results_summary(
        self,
        results: List[NumericResult],
        chart_name: str = "results_summary"
    ) -> Optional[str]:
        """
        Generate a summary chart with all key results

        Args:
            results: List of NumericResult objects
            chart_name: Name for output file

        Returns:
            Path to generated chart
        """
        logger.info(f"Generating results summary chart")

        if not results:
            logger.warning("No results to plot")
            return None

        # Take top 5-6 most important results
        top_results = results[:6]

        try:
            fig, ax = plt.subplots(figsize=(12, 7))

            # Horizontal bar chart for better label readability
            metrics = [r.metric for r in top_results]
            values = [r.value for r in top_results]
            contexts = [r.context for r in top_results]

            y = np.arange(len(metrics))
            bars = ax.barh(y, values, color=self.colors[:len(metrics)])

            # Customize
            ax.set_xlabel('Value (%)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Metric', fontsize=12, fontweight='bold')
            ax.set_title('Key Results Summary', fontsize=14, fontweight='bold', pad=20)
            ax.set_yticks(y)
            ax.set_yticklabels(metrics)

            # Add value labels
            for bar, value, context in zip(bars, values, contexts):
                width = bar.get_width()
                label = f'{value:.1f}%'
                if context:
                    label += f' ({context})'
                ax.text(
                    width + 2,  # Offset from bar
                    bar.get_y() + bar.get_height() / 2.,
                    label,
                    ha='left',
                    va='center',
                    fontsize=10,
                    fontweight='bold'
                )

            # X-axis limits
            max_val = max(values)
            ax.set_xlim(0, max(100, max_val * 1.3))

            # Grid
            ax.xaxis.grid(True, linestyle='--', alpha=0.7)
            ax.set_axisbelow(True)

            # Tight layout
            plt.tight_layout()

            # Save
            output_path = self.output_dir / f"{chart_name}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

            logger.info(f"✓ Results summary chart saved: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to generate results summary: {e}")
            return None
