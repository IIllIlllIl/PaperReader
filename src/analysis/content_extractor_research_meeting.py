"""
Research Group Meeting Content Extractor for PaperReader

Optimized for academic research group presentations (组会专用)

Slide structure (11 slides):
1. Title + Paper Info
2. Motivation (WHY this problem matters)
3. Problem Definition
4. Related Work / Baselines
5. Core Idea (Main Contribution)
6. Method Overview
7. Method Details
8. Experiment Setup
9. Results
10. Limitations
11. Takeaways + Discussion Questions
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResearchMeetingSlide:
    """Content for a research meeting slide"""
    title: str
    bullet_points: List[str]
    notes: str = ""
    slide_type: str = "content"  # content, title, discussion
    word_count: int = 0


@dataclass
class ResearchMeetingPresentation:
    """Complete research meeting presentation"""
    slides: List[ResearchMeetingSlide]
    total_slides: int


class ResearchMeetingContentExtractor:
    """Extract content optimized for research group meeting"""

    def __init__(self):
        self.max_words_per_slide = 100  # Allow more words for research meetings
        self.max_bullets_per_slide = 5  # Strict limit for clarity

    def extract_research_meeting_slides(self, analysis: Any) -> ResearchMeetingPresentation:
        """
        Extract slides from research meeting analysis

        Args:
            analysis: ResearchMeetingAnalysis object

        Returns:
            ResearchMeetingPresentation with 11 slides
        """
        logger.info("Extracting research meeting slides")

        slides = []

        # Slide 1: Title
        slides.append(self._create_title_slide(analysis))

        # Slide 2: Motivation
        if hasattr(analysis, 'motivation') and analysis.motivation:
            slides.append(self._create_motivation_slide(analysis))

        # Slide 3: Problem Definition
        if hasattr(analysis, 'problem_definition') and analysis.problem_definition:
            slides.append(self._create_problem_slide(analysis))

        # Slide 4: Related Work
        if hasattr(analysis, 'related_work') and analysis.related_work:
            slides.append(self._create_related_work_slide(analysis))

        # Slide 5: Core Idea
        if hasattr(analysis, 'core_idea') and analysis.core_idea:
            slides.append(self._create_core_idea_slide(analysis))

        # Slide 6: Method Overview
        if hasattr(analysis, 'method_overview') and analysis.method_overview:
            slides.append(self._create_method_overview_slide(analysis))

        # Slide 7: Method Details
        if hasattr(analysis, 'method_details') and analysis.method_details:
            slides.append(self._create_method_details_slide(analysis))

        # Slide 8: Experiment Setup
        if hasattr(analysis, 'experiment_setup') and analysis.experiment_setup:
            slides.append(self._create_experiment_setup_slide(analysis))

        # Slide 9: Results
        if hasattr(analysis, 'main_results') and analysis.main_results:
            slides.append(self._create_results_slide(analysis))

        # Slide 10: Limitations
        if hasattr(analysis, 'limitations') and analysis.limitations:
            slides.append(self._create_limitations_slide(analysis))

        # Slide 11: Takeaways + Discussion
        slides.append(self._create_takeaways_discussion_slide(analysis))

        logger.info(f"Created {len(slides)} research meeting slides")

        return ResearchMeetingPresentation(
            slides=slides,
            total_slides=len(slides)
        )

    def _create_title_slide(self, analysis) -> ResearchMeetingSlide:
        """Create title slide"""
        return ResearchMeetingSlide(
            title=analysis.title,
            bullet_points=[
                f"Authors: {analysis.authors}",
                f"Year: {analysis.year}"
            ],
            notes="Welcome slide - introduce paper",
            slide_type="title",
            word_count=self._count_words([analysis.title, analysis.authors, analysis.year])
        )

    def _create_motivation_slide(self, analysis) -> ResearchMeetingSlide:
        """Create motivation slide (WHY this matters)"""
        bullets = self._limit_bullets(analysis.motivation, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Motivation",
            bullet_points=bullets,
            notes="Why this problem is important - real-world impact",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_problem_slide(self, analysis) -> ResearchMeetingSlide:
        """Create problem definition slide"""
        bullets = self._limit_bullets(analysis.problem_definition, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Problem Definition",
            bullet_points=bullets,
            notes="The specific problem this paper solves",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_related_work_slide(self, analysis) -> ResearchMeetingSlide:
        """Create related work slide"""
        bullets = self._limit_bullets(analysis.related_work, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Related Work",
            bullet_points=bullets,
            notes="How this paper differs from previous work",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_core_idea_slide(self, analysis) -> ResearchMeetingSlide:
        """Create core idea slide (main contribution)"""
        return ResearchMeetingSlide(
            title="Core Idea",
            bullet_points=[analysis.core_idea],
            notes="Main contribution in one sentence",
            slide_type="content",
            word_count=self._count_words([analysis.core_idea])
        )

    def _create_method_overview_slide(self, analysis) -> ResearchMeetingSlide:
        """Create method overview slide"""
        bullets = self._limit_bullets(analysis.method_overview, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Method Overview",
            bullet_points=bullets,
            notes="High-level approach and key components",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_method_details_slide(self, analysis) -> ResearchMeetingSlide:
        """Create method details slide"""
        bullets = self._limit_bullets(analysis.method_details, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Method Details",
            bullet_points=bullets,
            notes="Technical details and implementation insights",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_experiment_setup_slide(self, analysis) -> ResearchMeetingSlide:
        """Create experiment setup slide with table"""
        setup = analysis.experiment_setup

        # Convert dict to markdown table
        table_rows = ["| Component | Details |", "|-----------|---------|"]
        for key, value in setup.items():
            table_rows.append(f"| **{key}** | {value} |")

        table_md = "\n".join(table_rows)

        return ResearchMeetingSlide(
            title="Experiment Setup",
            bullet_points=[table_md],
            notes="Experimental configuration",
            slide_type="table",
            word_count=self._count_table_words(table_md)
        )

    def _create_results_slide(self, analysis) -> ResearchMeetingSlide:
        """Create main results slide"""
        bullets = self._limit_bullets(analysis.main_results, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Results",
            bullet_points=bullets,
            notes="Main experimental results with key numbers",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_limitations_slide(self, analysis) -> ResearchMeetingSlide:
        """Create limitations slide (critical analysis)"""
        bullets = self._limit_bullets(analysis.limitations, self.max_bullets_per_slide)

        return ResearchMeetingSlide(
            title="Limitations",
            bullet_points=bullets,
            notes="Honest weaknesses and constraints",
            slide_type="content",
            word_count=self._count_words(bullets)
        )

    def _create_takeaways_discussion_slide(self, analysis) -> ResearchMeetingSlide:
        """Create takeaways + discussion questions slide"""
        bullets = []

        # Add takeaways
        if hasattr(analysis, 'key_takeaways') and analysis.key_takeaways:
            bullets.append("**Key Takeaways:**")
            bullets.extend([f"✓ {t}" for t in analysis.key_takeaways[:3]])

        # Add discussion questions
        if hasattr(analysis, 'discussion_questions') and analysis.discussion_questions:
            bullets.append("")
            bullets.append("**Discussion:**")
            bullets.extend([f"❓ {q}" for q in analysis.discussion_questions[:3]])

        # If empty, add default discussion
        if not bullets:
            bullets = [
                "**Key Takeaways:**",
                "✓ Paper presented",
                "",
                "**Discussion:**",
                "❓ What are your thoughts on this approach?"
            ]

        return ResearchMeetingSlide(
            title="Takeaways & Discussion",
            bullet_points=bullets,
            notes="Summary and open questions for audience",
            slide_type="discussion",
            word_count=self._count_words(bullets)
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
