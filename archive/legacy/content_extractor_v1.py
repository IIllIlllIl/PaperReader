"""
Content Extractor for PaperReader

Extracts and organizes content for presentation slides
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

from .ai_analyzer import PaperAnalysis, PresentationContent

logger = logging.getLogger(__name__)


@dataclass
class SlideContent:
    """Content for a single slide"""
    title: str
    bullet_points: List[str]
    notes: str = ""


@dataclass
class OrganizedPresentation:
    """Organized presentation with all slides"""
    slides: List[SlideContent]
    total_slides: int


class ContentExtractor:
    """Extracts and organizes content for presentation"""

    def __init__(self):
        """Initialize content extractor"""
        pass

    def extract_slide_content(self, analysis: PaperAnalysis,
                             presentation_content: PresentationContent) -> OrganizedPresentation:
        """
        Extract content for all slides

        Args:
            analysis: Paper analysis
            presentation_content: Generated presentation content

        Returns:
            OrganizedPresentation with all slide content
        """
        logger.info("Extracting slide content")

        slides = []

        # Slide 1: Title
        slides.append(SlideContent(
            title=presentation_content.title,
            bullet_points=[
                presentation_content.authors,
                f"{presentation_content.venue} | {presentation_content.year}"
            ],
            notes="Welcome slide. Introduce the paper and authors."
        ))

        # Slides 2-3: Background & Motivation
        if presentation_content.motivation:
            slides.append(SlideContent(
                title="背景与动机",
                bullet_points=presentation_content.motivation[:5],
                notes="Explain the background and motivation for this research."
            ))

        # Slide 4: Existing Problems
        if presentation_content.existing_problems:
            slides.append(SlideContent(
                title="现有问题",
                bullet_points=presentation_content.existing_problems[:5],
                notes="Describe the existing problems this paper addresses."
            ))

        # Slide 5: Research Problem
        slides.append(SlideContent(
            title="研究问题",
            bullet_points=[presentation_content.research_problem],
            notes="State the core research problem clearly."
        ))

        # Slide 6: Method Overview
        slides.append(SlideContent(
            title="方法概述",
            bullet_points=self._extract_method_points(presentation_content.method_overview),
            notes="Provide an overview of the proposed method."
        ))

        # Slides 7-8: Technical Details
        if presentation_content.technical_details:
            slides.append(SlideContent(
                title="技术细节",
                bullet_points=presentation_content.technical_details[:6],
                notes="Explain the technical details of the approach."
            ))

        # Slide 9: Innovations
        if presentation_content.innovations:
            slides.append(SlideContent(
                title="创新点",
                bullet_points=self._format_innovations(presentation_content.innovations),
                notes="Highlight the key innovations and contributions."
            ))

        # Slide 10: Experimental Setup
        slides.append(SlideContent(
            title="实验设置",
            bullet_points=self._extract_setup_points(presentation_content.experimental_setup),
            notes="Describe the experimental setup and evaluation methodology."
        ))

        # Slides 11-12: Main Results
        if presentation_content.main_results:
            slides.append(SlideContent(
                title="主要结果",
                bullet_points=presentation_content.main_results[:5],
                notes="Present the main experimental results."
            ))

        # Slide 13: Result Analysis
        if presentation_content.result_analysis:
            slides.append(SlideContent(
                title="结果分析",
                bullet_points=[presentation_content.result_analysis],
                notes="Analyze and interpret the results."
            ))

        # Slide 14: Discussion
        if presentation_content.discussion:
            slides.append(SlideContent(
                title="讨论",
                bullet_points=self._extract_discussion_points(presentation_content.discussion),
                notes="Discuss the implications of the results."
            ))

        # Slide 15: Pros
        if presentation_content.pros:
            slides.append(SlideContent(
                title="优点",
                bullet_points=[f"✓ {pro}" for pro in presentation_content.pros[:5]],
                notes="Highlight the advantages of the approach."
            ))

        # Slide 16: Cons
        if presentation_content.cons:
            slides.append(SlideContent(
                title="局限性",
                bullet_points=[f"✗ {con}" for con in presentation_content.cons[:5]],
                notes="Discuss the limitations honestly."
            ))

        # Slide 17: Future Work
        if presentation_content.future_work:
            slides.append(SlideContent(
                title="未来工作",
                bullet_points=presentation_content.future_work[:4],
                notes="Suggest directions for future research."
            ))

        # Slide 18: Conclusion
        slides.append(SlideContent(
            title="结论",
            bullet_points=self._extract_conclusion_points(presentation_content.conclusions),
            notes="Summarize the key takeaways."
        ))

        # Slide 19: Q&A
        slides.append(SlideContent(
            title="Q&A",
            bullet_points=["谢谢！", "Questions & Discussion"],
            notes="Open for questions."
        ))

        organized = OrganizedPresentation(
            slides=slides,
            total_slides=len(slides)
        )

        logger.info(f"Extracted content for {organized.total_slides} slides")
        return organized

    def suggest_visualizations(self, results: List[str]) -> List[Dict[str, str]]:
        """
        Suggest visualizations for results

        Args:
            results: List of result strings

        Returns:
            List of visualization suggestions
        """
        suggestions = []

        for i, result in enumerate(results):
            # Detect if result contains numbers (potential chart)
            if any(char.isdigit() for char in result):
                suggestions.append({
                    'type': 'chart',
                    'result': result,
                    'suggestion': 'Consider visualizing with bar chart or table'
                })
            else:
                suggestions.append({
                    'type': 'text',
                    'result': result,
                    'suggestion': 'Present as bullet point'
                })

        return suggestions[:5]  # Limit suggestions

    def _extract_method_points(self, method_text: str) -> List[str]:
        """Extract bullet points from method description"""
        # Split by sentences
        sentences = method_text.split('. ')
        points = [s.strip() + '.' for s in sentences if s.strip()]
        return points[:5] if points else [method_text]

    def _format_innovations(self, innovations: List[str]) -> List[str]:
        """Format innovation points"""
        formatted = []
        for i, innovation in enumerate(innovations[:5], 1):
            formatted.append(f"{i}. {innovation}")
        return formatted

    def _extract_setup_points(self, setup_text: str) -> List[str]:
        """Extract experimental setup points"""
        # Try to identify key components
        points = []

        # Look for dataset mentions
        if 'dataset' in setup_text.lower() or 'data' in setup_text.lower():
            points.append("Datasets: " + self._extract_dataset_info(setup_text))

        # Look for baseline mentions
        if 'baseline' in setup_text.lower() or 'comparison' in setup_text.lower():
            points.append("Baselines: " + self._extract_baseline_info(setup_text))

        # Look for metrics
        if 'metric' in setup_text.lower() or 'evaluation' in setup_text.lower():
            points.append("Metrics: " + self._extract_metric_info(setup_text))

        if not points:
            # Fall back to sentence splitting
            sentences = setup_text.split('. ')
            points = [s.strip() + '.' for s in sentences[:3] if s.strip()]

        return points[:5]

    def _extract_discussion_points(self, discussion_text: str) -> List[str]:
        """Extract discussion points"""
        sentences = discussion_text.split('. ')
        return [s.strip() + '.' for s in sentences[:4] if s.strip()]

    def _extract_conclusion_points(self, conclusion_text: str) -> List[str]:
        """Extract conclusion points"""
        sentences = conclusion_text.split('. ')
        points = [s.strip() + '.' for s in sentences if s.strip()]
        return points[:4] if points else [conclusion_text]

    def _extract_dataset_info(self, text: str) -> str:
        """Extract dataset information"""
        # Simple extraction - look for capitalized words
        words = text.split()
        datasets = [w for w in words if w[0].isupper() and len(w) > 3][:3]
        return ', '.join(datasets) if datasets else "Standard benchmarks"

    def _extract_baseline_info(self, text: str) -> str:
        """Extract baseline information"""
        if 'state-of-the-art' in text.lower() or 'sota' in text.lower():
            return "State-of-the-art methods"
        return "Standard baselines"

    def _extract_metric_info(self, text: str) -> str:
        """Extract metric information"""
        # Look for common metrics
        common_metrics = ['accuracy', 'precision', 'recall', 'F1', 'AUC', 'BLEU', 'ROUGE']
        found_metrics = [m for m in common_metrics if m.lower() in text.lower()]

        if found_metrics:
            return ', '.join(found_metrics[:3])
        return "Standard evaluation metrics"
