"""
PhD Research Meeting Content Extractor V2

Enhanced features:
- Figure insertion support (architecture diagrams)
- Result interpretations (why it matters)
- Related work comparison format
- Discussion depth
- Presentation script generation
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PhDMeetingSlide:
    """Content for a PhD research meeting slide"""
    title: str
    bullet_points: List[str]
    notes: str = ""
    slide_type: str = "content"  # content, title, discussion, figure
    word_count: int = 0
    figure_path: str = ""  # Path to figure image
    figure_caption: str = ""  # Figure caption


    has_figure: bool = False


@dataclass
class PhDMeetingPresentation:
    """Complete PhD research meeting presentation"""
    slides: List[PhDMeetingSlide]
    total_slides: int


class PhDMeetingContentExtractorV2:
    """Extract content optimized for PhD research group meeting V2"""

    def __init__(self):
        self.max_words_per_slide = 100
        self.max_bullets_per_slide = 5

    def extract_phd_meeting_slides(self, analysis: Any, figures: List[dict] = None) -> PhDMeetingPresentation:
        """
        Extract slides from PhD meeting analysis with figure support

        Args:
            analysis: ResearchMeetingAnalysis object
            figures: List of figure dicts from PDF (optional)

        Returns:
            PhDMeetingPresentation with 11+ slides
        """
        logger.info("Extracting PhD meeting slides (V2)")

        slides = []

        # Slide 1: Title
        slides.append(self._create_title_slide(analysis))

        # Slide 2: Motivation
        if hasattr(analysis, 'motivation') and analysis.motivation:
            slides.append(self._create_motivation_slide(analysis))

        # Slide 3: Problem Definition
        if hasattr(analysis, 'problem_definition') and analysis.problem_definition:
            slides.append(self._create_problem_slide(analysis))

        # Slide 4: Related Work (Enhanced format)
        if hasattr(analysis, 'related_work') and analysis.related_work:
            slides.append(self._create_related_work_slide(analysis))

        # Slide 5: Core Idea
        if hasattr(analysis, 'core_idea') and analysis.core_idea:
            slides.append(self._create_core_idea_slide(analysis))

        # Slide 6: Method Overview (WITH FIGURE)
        slides.append(self._create_method_overview_slide(analysis, figures))

        # Slide 7: Method Details
        if hasattr(analysis, 'method_details') and analysis.method_details:
            slides.append(self._create_method_details_slide(analysis))

        # Slide 8: Experiment Setup
        if hasattr(analysis, 'experiment_setup') and analysis.experiment_setup:
            slides.append(self._create_experiment_setup_slide(analysis))

        # Slide 9: Results (WITH INTERPRETATIONS)
        if hasattr(analysis, 'main_results') and analysis.main_results:
            slides.append(self._create_results_slide(analysis))

        # Slide 10: Limitations
        if hasattr(analysis, 'limitations') and analysis.limitations:
            slides.append(self._create_limitations_slide(analysis))

        # Slide 11: Takeaways & Discussion
        slides.append(self._create_takeaways_discussion_slide(analysis))

        logger.info(f"Created {len(slides)} PhD meeting slides (V2)")

        return PhDMeetingPresentation(
            slides=slides,
            total_slides=len(slides)
        )

    def _create_title_slide(self, analysis) -> PhDMeetingSlide:
        """Create title slide"""
        return PhDMeetingSlide(
            title=analysis.title,
            bullet_points=[
                f"Authors: {analysis.authors}",
                f"Year: {analysis.year}"
            ],
            notes="Welcome slide - introduce paper",
            slide_type="title",
            word_count=self._count_words([analysis.title, analysis.authors, analysis.year]),
            has_figure=False
        )

    def _create_motivation_slide(self, analysis) -> PhDMeetingSlide:
        """Create motivation slide (WHY this matters)"""
        bullets = self._limit_bullets(analysis.motivation, self.max_bullets_per_slide)

        return PhDMeetingSlide(
            title="Motivation",
            bullet_points=bullets,
            notes="Why this problem is important - real-world impact and research gap",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_problem_slide(self, analysis) -> PhDMeetingSlide:
        """Create problem definition slide"""
        bullets = self._limit_bullets(analysis.problem_definition, self.max_bullets_per_slide)

        return PhDMeetingSlide(
            title="Problem Definition",
            bullet_points=bullets,
            notes="The specific problem this paper solves",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_related_work_slide(self, analysis) -> PhDMeetingSlide:
        """Create related work slide with comparison format"""
        bullets = []

        # Format: "Previous work | Limitation | Our improvement"
        for item in self._limit_bullets(analysis.related_work, 4):
            bullets.append(item)

        return PhDMeetingSlide(
            title="Related Work & Our Advantage",
            bullet_points=bullets,
            notes="How this paper differs from previous work - focus on limitations and improvements",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_core_idea_slide(self, analysis) -> PhDMeetingSlide:
        """Create core idea slide (main contribution)"""
        return PhDMeetingSlide(
            title="Core Idea",
            bullet_points=[analysis.core_idea],
            notes="Main contribution in one clear sentence - the key insight",
            slide_type="content",
            word_count=self._count_words([analysis.core_idea]),
            has_figure=False
        )

    def _create_method_overview_slide(self, analysis, figures: List[dict]) -> PhDMeetingSlide:
        """Create method overview slide WITH FIGURE"""
        bullets = self._limit_bullets(analysis.method_overview, 3)  # Fewer bullets when figure exists

        # Find architecture figure if available
        figure_path = ""
        figure_caption = ""
        has_figure = False

        if figures:
            # Prefer figures that look like architecture diagrams
            for fig in figures:
                caption = fig.get('caption', '').lower()
                if any(keyword in caption for keyword in ['architecture', 'framework', 'pipeline', 'overview', 'system', 'diagram']):
                    figure_path = fig['image_path']
                    figure_caption = caption
                    has_figure = True
                    break

        return PhDMeetingSlide(
            title="Method Overview",
            bullet_points=bullets,
            notes="High-level approach and key components",
            slide_type="content",
            word_count=self._count_words(bullets),
            figure_path=figure_path,
            figure_caption=figure_caption,
            has_figure=has_figure
        )

    def _create_method_details_slide(self, analysis) -> PhDMeetingSlide:
        """Create method details slide"""
        bullets = self._limit_bullets(analysis.method_details, self.max_bullets_per_slide)

        return PhDMeetingSlide(
            title="Method Details",
            bullet_points=bullets,
            notes="Technical details and implementation insights",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_experiment_setup_slide(self, analysis) -> PhDMeetingSlide:
        """Create experiment setup slide with table"""
        setup = analysis.experiment_setup

        # Convert dict to markdown table
        table_rows = ["| Component | Details |", "|-----------|---------|"]
        for key, value in setup.items():
            table_rows.append(f"| **{key}** | {value} |")

        table_md = "\n".join(table_rows)

        return PhDMeetingSlide(
            title="Experiment Setup",
            bullet_points=[table_md],
            notes="Experimental configuration - datasets, baselines, metrics",
            slide_type="table",
            word_count=self._count_table_words(table_md),
            has_figure=False
        )

    def _create_results_slide(self, analysis) -> PhDMeetingSlide:
        """Create results slide WITH INTERPRETATIONS"""
        bullets = []

        # Each result already has interpretation (from AI)
        for result in self._limit_bullets(analysis.main_results, self.max_bullets_per_slide):
            bullets.append(result)

        return PhDMeetingSlide(
            title="Results & Interpretations",
            bullet_points=bullets,
            notes="Main experimental results with interpretations - what they mean",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_limitations_slide(self, analysis) -> PhDMeetingSlide:
        """Create limitations slide (critical analysis)"""
        bullets = self._limit_bullets(analysis.limitations, self.max_bullets_per_slide)

        return PhDMeetingSlide(
            title="Limitations & Critical Analysis",
            bullet_points=bullets,
            notes="Honest weaknesses, scope constraints, evaluation gaps",
            slide_type="content",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _create_takeaways_discussion_slide(self, analysis) -> PhDMeetingSlide:
        """Create takeaways + discussion questions slide"""
        bullets = []

        # Add takeaways
        if hasattr(analysis, 'key_takeaways') and analysis.key_takeaways:
            bullets.append("**Key Takeaways:**")
            bullets.extend([f"✓ {t}" for t in analysis.key_takeaways[:3]])

        # add discussion questions
        if hasattr(analysis, 'discussion_questions') and analysis.discussion_questions:
            bullets.append("")
            bullets.append("**Discussion Questions:**")
            bullets.extend([f"❓ {q}" for q in analysis.discussion_questions[:3]])

        return PhDMeetingSlide(
            title="Takeaways & Discussion",
            bullet_points=bullets,
            notes="Summary of key insights and open questions for audience discussion",
            slide_type="discussion",
            word_count=self._count_words(bullets),
            has_figure=False
        )

    def _limit_bullets(self, bullets: List[str], max_count: int) -> List[str]:
        """Limit bullet points to max_count"""
        return bullets[:max_count]

    def _count_words(self, texts: List[str]) -> int:
        """Count words in list of texts"""
        total = 0
        for text in texts:
            if text:
                clean = text.replace("|", " ").replace("*", "").replace("#", "")
                clean = clean.replace(":", " ").replace("-", " ")
                total += len(clean.split())
        return total

    def _count_table_words(self, table: str) -> int:
        """Count words in markdown table"""
        lines = table.split('\n')
        if len(lines) < 2:
            return 0

        # Skip header and separator
        content_lines = lines[2:]
        total = 0
        for line in content_lines:
            if line.strip():
                cells = line.split('|')
                for cell in cells:
                    clean = cell.strip().replace('*', '')
                    total += len(clean.split())
        return total
