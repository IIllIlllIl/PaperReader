"""
Enhanced Content Extractor V3 for PaperReader

V3 Improvements:
- English ONLY (no Chinese)
- Max 30 words per slide
- Keywords-first approach
- Tables for structured data
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SlideContent:
    """Content for a single slide (V3)"""
    title: str  # English only
    bullet_points: List[str]  # Keywords only
    notes: str = ""
    slide_type: str = "content"  # content, title, section, table
    word_count: int = 0
    figure_path: str = ""
    figure_caption: str = ""
    has_figure: bool = False


@dataclass
class OrganizedPresentation:
    """Organized presentation with all slides (V3)"""
    slides: List[SlideContent]
    total_slides: int


class ContentExtractor:
    """Extracts and organizes content for V3 presentation"""

    def __init__(self):
        self.max_words_per_slide = 30

    def extract_detailed_slides(self, analysis: Any, slide_plan=None, figures=None) -> OrganizedPresentation:
        """
        Extract slides from analysis with V3 requirements

        Args:
            analysis: Analysis object from AI
            slide_plan: SlidePlan object (source of truth for slide structure)
            figures: Extracted figure metadata from PDFImageExtractor

        Returns:
            Organized presentation with slides
        """
        logger.info("Extracting detailed slides (V3)")

        # CRITICAL: If slide_plan is provided, use it as the source of truth
        if slide_plan is not None:
            logger.info(f"Using SlidePlan as source of truth ({slide_plan.total_slides} slides planned)")
            slides = self._generate_slides_from_plan(analysis, slide_plan, figures=figures)
        else:
            # Fallback: Legacy behavior (independent slide generation)
            logger.warning("No SlidePlan provided, using legacy independent generation")
            slides = self._generate_slides_independently(analysis)

        logger.info(f"Created {len(slides)} slides (V3)")

        return OrganizedPresentation(
            slides=slides,
            total_slides=len(slides)
        )

    def _generate_slides_from_plan(self, analysis: Any, slide_plan, figures=None) -> List[SlideContent]:
        """
        Generate slides following the SlidePlan structure

        FOR EACH slide in SlidePlan:
            Generate slide content based on title and key_points
        """
        slides = []
        figure_assignments = self._build_figure_assignments(slide_plan.slides, figures or [])

        for index, planned_slide in enumerate(slide_plan.slides):
            assigned_figure = figure_assignments.get(index)
            slide = self._create_slide_from_plan(analysis, planned_slide, figure=assigned_figure)
            slides.append(slide)

        # Validate: ensure all planned slides are generated
        if len(slides) < len(slide_plan.slides):
            logger.warning(f"Generated {len(slides)} slides but planned {len(slide_plan.slides)}")
            # Auto-generate missing slides with placeholder content
            missing_count = len(slide_plan.slides) - len(slides)
            for i in range(missing_count):
                placeholder = SlideContent(
                    title=f"Placeholder Slide {len(slides) + 1}",
                    bullet_points=["[Content to be added]"],
                    notes="Placeholder slide",
                    slide_type="content"
                )
                slides.append(placeholder)
                logger.info(f"Added placeholder slide for missing planned slide")

        return slides

    def _create_slide_from_plan(self, analysis: Any, planned_slide, figure=None) -> SlideContent:
        """
        Create a slide based on the planned slide topic

        Maps planned slide title to appropriate content from analysis
        """
        title = planned_slide.title
        slide_type = planned_slide.slide_type
        key_points = planned_slide.key_points or []

        # Special handling for standard slides
        if title.lower() in ['title', 'paper title']:
            return self._create_title_slide(analysis)
        elif title.lower() in ['outline', 'agenda']:
            return self._create_outline_slide()
        elif title.lower() in ['q&a', 'qa', 'questions', 'thank you']:
            return self._create_qa_slide()

        # Map slide title to analysis attributes
        content = self._extract_content_for_title(analysis, title, key_points)

        # Determine if this should be a table slide
        if slide_type == 'table' or self._should_be_table(title, analysis):
            slide = self._create_table_slide(title, content)
        else:
            # Regular content slide
            slide = SlideContent(
                title=title,
                bullet_points=content if isinstance(content, list) else [content],
                notes=planned_slide.notes or f"{title} slide",
                slide_type=slide_type,
                word_count=self._count_words(content if isinstance(content, list) else [content])
            )

        if figure:
            slide.figure_path = figure.get('image_path', '')
            slide.figure_caption = figure.get('caption', '')
            slide.has_figure = bool(slide.figure_path)
            if slide.has_figure:
                logger.info(f"Assigned figure to slide '{title}': {slide.figure_path}")

        return slide

    def _build_figure_assignments(self, planned_slides: List[Any], figures: List[dict]) -> Dict[int, dict]:
        """Assign extracted figures to the most relevant planned slides."""
        if not figures:
            return {}

        preferred_keywords = [
            'method', 'approach', 'framework', 'architecture', 'workflow',
            'overview', 'system', 'experiment', 'setup', 'result', 'analysis',
            'finding', 'evaluation'
        ]

        candidate_indices = []
        fallback_indices = []
        for index, planned_slide in enumerate(planned_slides):
            title_lower = planned_slide.title.lower()
            if title_lower in ['title', 'paper title', 'outline', 'agenda', 'q&a', 'qa', 'questions', 'thank you']:
                continue

            fallback_indices.append(index)
            if any(keyword in title_lower for keyword in preferred_keywords):
                candidate_indices.append(index)

        ordered_indices = candidate_indices + [
            index for index in fallback_indices
            if index not in candidate_indices
        ]
        assignments = {}
        for index, figure in zip(ordered_indices, figures):
            assignments[index] = figure

        logger.info(f"Prepared {len(assignments)} figure assignments from {len(figures)} extracted figures")
        return assignments

    def _extract_content_for_title(self, analysis: Any, title: str, key_points: List[str]) -> List[str]:
        """
        Extract content from analysis based on slide title

        Uses key_points as hints for what to extract
        """
        title_lower = title.lower()

        # Map title keywords to analysis attributes
        if 'background' in title_lower or 'motivation' in title_lower:
            return self._safe_get_attr(analysis, 'research_background_keywords', key_points)
        elif 'problem' in title_lower:
            return self._safe_get_attr(analysis, 'research_problem_keywords', key_points)
        elif 'insight' in title_lower or 'breakthrough' in title_lower:
            return self._safe_get_attr(analysis, 'key_insights', key_points)
        elif 'method' in title_lower or 'approach' in title_lower:
            return self._safe_get_attr(analysis, 'method_keywords', key_points)
        elif 'technical' in title_lower or 'detail' in title_lower:
            return self._safe_get_attr(analysis, 'technical_details_keywords', key_points)
        elif 'dataset' in title_lower:
            return self._safe_get_attr(analysis, 'datasets_table', key_points)
        elif 'baseline' in title_lower or 'comparison' in title_lower:
            return self._safe_get_attr(analysis, 'baselines_table', key_points)
        elif 'metric' in title_lower:
            return self._safe_get_attr(analysis, 'metrics_table', key_points)
        elif 'experiment' in title_lower or 'setup' in title_lower:
            return self._safe_get_attr(analysis, 'experimental_setup_keywords', key_points)
        elif 'result' in title_lower:
            return self._safe_get_attr(analysis, 'main_results_keywords', key_points)
        elif 'finding' in title_lower:
            return self._safe_get_attr(analysis, 'key_findings_keywords', key_points)
        elif 'advantage' in title_lower or 'strength' in title_lower:
            return self._safe_get_attr(analysis, 'advantages_keywords', key_points)
        elif 'limitation' in title_lower or 'weakness' in title_lower:
            return self._safe_get_attr(analysis, 'limitations_keywords', key_points)
        elif 'future' in title_lower or 'conclusion' in title_lower:
            return self._safe_get_attr(analysis, 'future_work_keywords', key_points)
        elif 'discussion' in title_lower or 'takeaway' in title_lower:
            return self._safe_get_attr(analysis, 'key_findings_keywords', key_points)
        else:
            # Default: return key_points as content
            return key_points[:6]  # Max 6 items

    def _safe_get_attr(self, obj: Any, attr: str, fallback: List[str]) -> List[str]:
        """Safely get attribute from object, with fallback"""
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if isinstance(value, list):
                return value[:6]  # Max 6 items
            elif isinstance(value, dict):
                return value  # Return dict for table slides
            else:
                return [str(value)]
        else:
            # Use fallback key_points
            return fallback[:6]

    def _should_be_table(self, title: str, analysis: Any) -> bool:
        """Determine if slide should be a table based on title"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in ['dataset', 'baseline', 'metric', 'setup'])

    def _generate_slides_independently(self, analysis: Any) -> List[SlideContent]:
        """
        Legacy method: Generate slides independently without SlidePlan

        This is kept as a fallback but should not be the primary path
        """
        slides = []

        # Slide 1: Title
        slides.append(self._create_title_slide(analysis))

        # Slide 2: Outline
        slides.append(self._create_outline_slide())

        # Background slides
        if hasattr(analysis, 'research_background_keywords'):
            slides.append(self._create_keywords_slide(
                "Research Background",
                analysis.research_background_keywords
            ))

        # Problem slides
        if hasattr(analysis, 'research_problem_keywords'):
            slides.append(self._create_keywords_slide(
                "Research Problem",
                analysis.research_problem_keywords
            ))

        # Key insights
        if hasattr(analysis, 'key_insights'):
            slides.append(self._create_insights_slide(analysis.key_insights))

        # Method slides
        if hasattr(analysis, 'method_keywords'):
            slides.append(self._create_keywords_slide(
                "Method Overview",
                analysis.method_keywords
            ))

        # Technical details
        if hasattr(analysis, 'technical_details_keywords'):
            slides.append(self._create_keywords_slide(
                "Technical Details",
                analysis.technical_details_keywords
            ))

        # Datasets table
        if hasattr(analysis, 'datasets_table'):
            slides.append(self._create_table_slide(
                "Datasets",
                analysis.datasets_table
            ))

        # Baselines table
        if hasattr(analysis, 'baselines_table'):
            slides.append(self._create_table_slide(
                "Baselines",
                analysis.baselines_table
            ))

        # Metrics table
        if hasattr(analysis, 'metrics_table'):
            slides.append(self._create_table_slide(
                "Metrics",
                analysis.metrics_table
            ))

        # Experimental setup
        if hasattr(analysis, 'experimental_setup_keywords'):
            slides.append(self._create_keywords_slide(
                "Experimental Setup",
                analysis.experimental_setup_keywords
            ))

        # Main results
        if hasattr(analysis, 'main_results_keywords'):
            slides.append(self._create_results_slide(analysis.main_results_keywords))

        # Key findings
        if hasattr(analysis, 'key_findings_keywords'):
            slides.append(self._create_keywords_slide(
                "Key Findings",
                analysis.key_findings_keywords
            ))

        # Advantages
        if hasattr(analysis, 'advantages_keywords'):
            slides.append(self._create_keywords_slide(
                "Advantages",
                analysis.advantages_keywords
            ))

        # Limitations
        if hasattr(analysis, 'limitations_keywords'):
            slides.append(self._create_keywords_slide(
                "Limitations",
                analysis.limitations_keywords
            ))

        # Future work
        if hasattr(analysis, 'future_work_keywords'):
            slides.append(self._create_keywords_slide(
                "Future Work",
                analysis.future_work_keywords
            ))

        # Slide: Q&A
        slides.append(self._create_qa_slide())

        return slides
    
    def _create_title_slide(self, analysis: Any) -> SlideContent:
        """Create title slide"""
        title = getattr(analysis, 'title', 'Unknown Title')
        authors = getattr(analysis, 'authors', [])
        year = getattr(analysis, 'year', '2024')
        
        if isinstance(authors, list):
            authors_str = ', '.join(authors[:3])
        else:
            authors_str = str(authors)
        
        bullet_points = [
            f"{authors_str}",
            f"{year}"
        ]
        
        return SlideContent(
            title=title,
            bullet_points=bullet_points,
            notes="Welcome slide",
            slide_type="title",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_outline_slide(self) -> SlideContent:
        """Create outline slide"""
        bullet_points = [
            "Background & Problem",
            "Key Insights",
            "Method & Technical Details",
            "Experiments & Results",
            "Analysis & Discussion",
            "Conclusion & Future Work"
        ]
        
        return SlideContent(
            title="Outline",
            bullet_points=bullet_points,
            notes="Presentation outline",
            slide_type="section",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_keywords_slide(self, title: str, keywords: List[str]) -> SlideContent:
        """Create slide with keywords"""
        # Ensure max 30 words
        bullet_points = keywords[:6]  # Max 6 items
        
        return SlideContent(
            title=title,
            bullet_points=bullet_points,
            notes=f"{title} slide",
            slide_type="content",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_insights_slide(self, insights: List[str]) -> SlideContent:
        """Create insights slide with emoji"""
        bullet_points = insights[:5]  # Max 5 insights
        
        return SlideContent(
            title="Key Insights",
            bullet_points=bullet_points,
            notes="Key insights and breakthroughs",
            slide_type="content",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_results_slide(self, results: Any) -> SlideContent:
        """
        Create results slide with comparison table (TASK 4)

        If baseline comparison data exists, generates comparison table.
        Otherwise, formats results as bullet points.

        Args:
            results: Results data (list or dict with comparison data)

        Returns:
            SlideContent with results table or bullet points
        """
        # Try to generate comparison table if data available
        comparison_table = self._generate_results_table(results)

        if comparison_table:
            # Use comparison table
            return SlideContent(
                title="Results",
                bullet_points=[comparison_table],
                notes="Results comparison with baseline",
                slide_type="table",
                word_count=self._count_table_words(comparison_table)
            )
        else:
            # Fallback to bullet points
            if isinstance(results, list):
                bullet_points = results[:6]  # Max 6 results
            else:
                bullet_points = [str(results)]

            return SlideContent(
                title="Results",
                bullet_points=bullet_points,
                notes="Main experimental results",
                slide_type="content",
                word_count=self._count_words(bullet_points)
            )

    def _generate_results_table(self, results: Any) -> str:
        """
        Generate markdown comparison table if baseline data exists (TASK 4)

        Args:
            results: Results data (may include baseline comparison)

        Returns:
            Markdown table string or empty string if no comparison data
        """
        # If results is a dict with comparison structure
        if isinstance(results, dict):
            if 'proposed' in results and 'baseline' in results:
                # Generate comparison table
                lines = ["| Metric | Proposed | Baseline | Improvement |",
                        "|--------|----------|----------|-------------|"]

                proposed = results['proposed']
                baseline = results['baseline']

                # Get all metrics
                metrics = set(proposed.keys()) | set(baseline.keys())

                for metric in sorted(metrics):
                    prop_val = proposed.get(metric, 'N/A')
                    base_val = baseline.get(metric, 'N/A')

                    # Calculate improvement if both are numbers
                    improvement = self._calculate_improvement(prop_val, base_val)

                    lines.append(f"| **{metric}** | {prop_val} | {base_val} | {improvement} |")

                return "\n".join(lines)

        # If results is a list with structured comparison data
        elif isinstance(results, list):
            # Check if list items have comparison format
            has_comparison = any(
                isinstance(item, dict) and ('proposed' in str(item) or 'baseline' in str(item))
                for item in results
            )

            if has_comparison:
                # Try to extract comparison data from list
                lines = ["| Metric | Proposed | Baseline | Improvement |",
                        "|--------|----------|----------|-------------|"]

                for item in results:
                    if isinstance(item, dict):
                        metric = item.get('metric', item.get('name', 'Unknown'))
                        prop_val = item.get('proposed', item.get('value', 'N/A'))
                        base_val = item.get('baseline', 'N/A')
                        improvement = self._calculate_improvement(prop_val, base_val)

                        lines.append(f"| **{metric}** | {prop_val} | {base_val} | {improvement} |")

                return "\n".join(lines)

        # No comparison data available
        return ""

    def _calculate_improvement(self, proposed: Any, baseline: Any) -> str:
        """
        Calculate improvement percentage between proposed and baseline

        Args:
            proposed: Proposed method value
            baseline: Baseline method value

        Returns:
            Improvement string (e.g., "+90%" or "N/A")
        """
        try:
            # Extract numeric values
            prop_num = self._extract_number(proposed)
            base_num = self._extract_number(baseline)

            if prop_num is not None and base_num is not None and base_num != 0:
                improvement = ((prop_num - base_num) / base_num) * 100
                if improvement > 0:
                    return f"+{improvement:.0f}%"
                else:
                    return f"{improvement:.0f}%"
        except (ValueError, TypeError, ZeroDivisionError):
            pass

        return "N/A"

    def _extract_number(self, value: Any) -> Optional[float]:
        """
        Extract numeric value from string (e.g., "59%" → 59.0)

        Args:
            value: Value to extract number from

        Returns:
            Float value or None
        """
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Remove percentage sign and extract number
            import re
            match = re.search(r'(\d+\.?\d*)', value)
            if match:
                return float(match.group(1))

        return None
    
    def _create_table_slide(self, title: str, content) -> SlideContent:
        """
        Create slide from various content types (TASK 1 fix)

        Supports:
        - dict → markdown table
        - list → bullet points
        - string → paragraph

        Args:
            title: Slide title
            content: Content (dict, list, or string)

        Returns:
            SlideContent with appropriate formatting
        """
        # Determine slide type using intelligent detection (TASK 2)
        slide_type = self._determine_slide_type(title, content)

        # Format content based on type
        formatted_content = self._format_content(content, slide_type)

        bullet_points = [formatted_content] if slide_type == "table" else formatted_content

        return SlideContent(
            title=title,
            bullet_points=bullet_points,
            notes=f"{title} {'table' if slide_type == 'table' else 'content'}",
            slide_type=slide_type,
            word_count=self._count_words(bullet_points)
        )

    def _format_content(self, content: Any, slide_type: str) -> Any:
        """
        Format content based on type (TASK 1)

        Args:
            content: Raw content (dict, list, or string)
            slide_type: Type of slide (table, content, diagram)

        Returns:
            Formatted content
        """
        if slide_type == "table":
            # Dict → markdown table
            if isinstance(content, dict):
                return self._dict_to_markdown_table(content)
            # List → convert to bullet list
            elif isinstance(content, list):
                return "\n".join(f"- {item}" for item in content)
            else:
                return str(content)
        else:
            # Content slide: ensure list format
            if isinstance(content, list):
                return content
            elif isinstance(content, dict):
                # Convert dict to bullet points
                return [f"**{k}**: {v}" for k, v in content.items()]
            else:
                return [str(content)]

    def _determine_slide_type(self, title: str, content: Any) -> str:
        """
        Intelligently determine slide type (TASK 2)

        Rules:
        - If content is dict → table slide
        - If title contains setup/dataset/baseline/comparison/metric → table slide
        - If title contains architecture/workflow/overview → diagram slide
        - Otherwise → content slide

        Args:
            title: Slide title
            content: Content to analyze

        Returns:
            Slide type (table, diagram, or content)
        """
        # Priority 1: If content is dict, always table
        if isinstance(content, dict):
            return "table"

        # Priority 2: Check title keywords
        title_lower = title.lower()

        # Table indicators
        table_keywords = ['setup', 'dataset', 'baseline', 'comparison', 'metric', 'experiment']
        if any(kw in title_lower for kw in table_keywords):
            return "table"

        # Diagram indicators
        diagram_keywords = ['architecture', 'workflow', 'overview', 'framework', 'system']
        if any(kw in title_lower for kw in diagram_keywords):
            return "diagram"

        # Default: content slide
        return "content"

    def _dict_to_markdown_table(self, data: dict) -> str:
        """Convert dictionary to markdown table"""
        if not data:
            return ""

        lines = ["| Item | Content |", "|------|---------|"]
        for key, value in data.items():
            lines.append(f"| **{key}** | {value} |")

        return "\n".join(lines)
    
    def _create_qa_slide(self) -> SlideContent:
        """Create Q&A slide"""
        return SlideContent(
            title="Q&A",
            bullet_points=["Thank you", "Questions?"],
            notes="Open for questions",
            slide_type="section",
            word_count=2
        )
    
    def _count_words(self, bullet_points: List[str]) -> int:
        """Count total words in bullet points"""
        total = 0
        for point in bullet_points:
            # Remove markdown formatting
            clean = point.replace('*', '').replace('#', '').replace('|', ' ')
            total += len(clean.split())
        return total
    
    def _count_table_words(self, table: str) -> int:
        """Estimate words in table"""
        # Count cells in table
        lines = table.split('\n')
        if len(lines) < 2:
            return 0
        
        # Count header cells
        header_cells = lines[0].count('|') - 1
        data_rows = len([l for l in lines[2:] if l.strip()])
        
        # Estimate words: ~2 words per cell
        return header_cells * data_rows * 2

    def _create_figure_slide(self, title: str, image_path: str, caption: str = "") -> SlideContent:
        """Create slide with figure"""
        bullet_points = []
        
        # Add image markdown
        if image_path:
            bullet_points.append(f"![{title}]({image_path})")
        
        # Add caption if available
        if caption:
            bullet_points.append(f"*{caption}*")
        
        return SlideContent(
            title=title,
            bullet_points=bullet_points,
            notes=f"Figure: {title}",
            slide_type="figure",
            word_count=self._count_words(bullet_points)
        )

    def add_figures_to_slides(self, slides: List, figures: List[dict], max_per_slide: int = 1) -> None:
        """
        Add figure slides to presentation
        
        Args:
            slides: Existing slides list
            figures: List of figure dicts from PDFImageExtractor
            max_per_slide: Max figures per slide
        """
        if not figures:
            return
        
        for i, fig in enumerate(figures[:6]):  # Max 6 figures total
            # Create dedicated figure slide
            slide = self._create_figure_slide(
                title=f"Figure {fig['figure_num']}",
                image_path=fig['image_path'],
                caption=fig.get('caption', '')
            )
            slides.append(slide)
            
            logger.info(f"Added figure {fig['figure_num']} from page {fig['page_num']}")

