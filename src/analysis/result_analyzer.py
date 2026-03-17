"""
Result Analyzer

Extracts numeric results from PaperAnalysis for chart generation.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class NumericResult:
    """Represents a single numeric result"""
    metric: str
    value: float
    unit: str = ""
    context: str = ""  # "SWE-bench", "Internal", "baseline", etc.
    is_percentage: bool = False

    def to_dict(self) -> dict:
        return {
            "metric": self.metric,
            "value": self.value,
            "unit": self.unit,
            "context": self.context,
            "is_percentage": self.is_percentage
        }


@dataclass
class ComparisonResult:
    """Represents comparison between methods"""
    methods: List[str]
    values: List[float]
    metric: str
    is_percentage: bool = False

    def to_dict(self) -> dict:
        return {
            "methods": self.methods,
            "values": self.values,
            "metric": self.metric,
            "is_percentage": self.is_percentage
        }


class ResultAnalyzer:
    """Analyzes and extracts numeric results from paper analysis"""

    def __init__(self):
        self.percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
        self.number_pattern = r'(\d+(?:\.\d+)?)'

    def extract_results(self, analysis: Any) -> List[NumericResult]:
        """
        Extract numeric results from PaperAnalysis

        Args:
            analysis: PaperAnalysis or ResearchMeetingAnalysis object

        Returns:
            List of NumericResult objects
        """
        logger.info("Extracting numeric results from analysis")

        results = []

        # Extract from main_results field
        if hasattr(analysis, 'main_results') and analysis.main_results:
            for result_text in analysis.main_results:
                numeric = self._parse_result_text(result_text)
                if numeric:
                    results.append(numeric)

        logger.info(f"Extracted {len(results)} numeric results")
        return results

    def extract_comparisons(self, analysis: Any) -> List[ComparisonResult]:
        """
        Extract comparison results for chart generation

        Args:
            analysis: PaperAnalysis or ResearchMeetingAnalysis object

        Returns:
            List of ComparisonResult objects
        """
        logger.info("Extracting comparison results")

        comparisons = []

        # Look for performance comparison data
        if hasattr(analysis, 'main_results'):
            # Try to detect comparison patterns
            comparisons = self._detect_comparisons(analysis.main_results)

        logger.info(f"Extracted {len(comparisons)} comparison results")
        return comparisons

    def _parse_result_text(self, text: str) -> Optional[NumericResult]:
        """Parse a result text to extract numeric value"""

        # Remove markdown bold markers
        text = text.replace('**', '').replace('*', '')

        # Try to find percentage
        percent_match = re.search(self.percentage_pattern, text)
        if percent_match:
            value = float(percent_match.group(1))

            # Extract metric name
            # Common patterns: "X% approval rate", "Y% merged PR rate"
            metric = self._extract_metric_name(text)

            # Extract context (SWE-bench, Internal, etc.)
            context = self._extract_context(text)

            return NumericResult(
                metric=metric,
                value=value,
                unit="%",
                context=context,
                is_percentage=True
            )

        # Try to find regular number
        number_match = re.search(self.number_pattern, text)
        if number_match:
            value = float(number_match.group(1))
            metric = self._extract_metric_name(text)
            context = self._extract_context(text)

            return NumericResult(
                metric=metric,
                value=value,
                context=context,
                is_percentage=False
            )

        return None

    def _extract_metric_name(self, text: str) -> str:
        """Extract metric name from result text"""

        # Clean text
        text = text.replace('🔥', '').replace('**', '').strip()

        # Common metrics with more specific patterns
        metric_patterns = [
            (r'plan\s+approval\s+rate', "Plan Approval Rate"),
            (r'merged\s+pr\s+rate', "Merged PR Rate"),
            (r'pr\s+merge\s+rate', "PR Merge Rate"),
            (r'recall', "Recall"),
            (r'precision', "Precision"),
            (r'accuracy', "Accuracy"),
            (r'f1\s+score', "F1 Score"),
            (r'code\s+similarity', "Code Similarity"),
            (r'test\s+pass\s+rate', "Test Pass Rate"),
            (r'file\s+localization', "File Localization"),
            (r'approval\s+rate', "Approval Rate"),
            (r'merge\s+rate', "Merge Rate"),
        ]

        text_lower = text.lower()
        for pattern, metric_name in metric_patterns:
            if re.search(pattern, text_lower):
                return metric_name

        # Fallback: Try to extract meaningful phrase before percentage
        # Look for pattern like "X% of Y" or "X% [metric]"
        match = re.search(r'(\d+(?:\.\d+)?%)\s+(?:of\s+)?([a-z\s]+?)(?:\s+(?:in|on|for|indicates|shows|demonstrates))', text_lower)
        if match:
            metric_phrase = match.group(2).strip()
            # Capitalize
            return ' '.join(word.capitalize() for word in metric_phrase.split())

        # Last resort: extract key words
        words = [w for w in text.split() if not w.isdigit() and not w.startswith('*')]
        if len(words) >= 2:
            return ' '.join(words[:2])

        return "Result"

    def _extract_context(self, text: str) -> str:
        """Extract context from result text"""

        contexts = [
            ("SWE-bench", ["swe-bench", "swebench"]),
            ("Internal", ["internal", "enterprise", "production"]),
            ("Baseline", ["baseline", "previous", "prior"])
        ]

        text_lower = text.lower()
        for context_name, keywords in contexts:
            if any(kw in text_lower for kw in keywords):
                return context_name

        return ""

    def _detect_comparisons(self, results: List[str]) -> List[ComparisonResult]:
        """Detect comparison patterns in results"""

        comparisons = []

        # Group results by metric
        metric_values = {}

        for result_text in results:
            numeric = self._parse_result_text(result_text)
            if numeric and numeric.metric and numeric.context:
                key = numeric.metric
                if key not in metric_values:
                    metric_values[key] = {"methods": [], "values": []}

                metric_values[key]["methods"].append(numeric.context)
                metric_values[key]["values"].append(numeric.value)

        # Convert to ComparisonResult if we have multiple values
        for metric, data in metric_values.items():
            if len(data["values"]) >= 2:
                comparisons.append(ComparisonResult(
                    methods=data["methods"],
                    values=data["values"],
                    metric=metric,
                    is_percentage=True  # Most are percentages
                ))

        return comparisons

    def suggest_chart_type(self, comparison: ComparisonResult) -> str:
        """
        Suggest best chart type for a comparison

        Returns: "bar", "grouped_bar", "line", "pie"
        """
        n_methods = len(comparison.methods)

        if n_methods == 1:
            return "pie"  # Single value, show as pie
        elif n_methods == 2:
            return "bar"  # Two values, simple bar chart
        elif n_methods <= 5:
            return "bar"  # Multiple values, bar chart
        else:
            return "line"  # Many values, line chart
