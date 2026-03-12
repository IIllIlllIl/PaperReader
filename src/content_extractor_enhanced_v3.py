"""
Enhanced Content Extractor V3 for PaperReader

V3 Improvements:
- English ONLY (no Chinese)
- Max 30 words per slide
- Keywords-first approach
- Tables for structured data
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class EnhancedSlideContentV3:
    """Content for a single slide (V3)"""
    title: str  # English only
    bullet_points: List[str]  # Keywords only
    notes: str = ""
    slide_type: str = "content"  # content, title, section, table
    word_count: int = 0


@dataclass
class EnhancedOrganizedPresentationV3:
    """Organized presentation with all slides (V3)"""
    slides: List[EnhancedSlideContentV3]
    total_slides: int


class EnhancedContentExtractorV3:
    """Extracts and organizes content for V3 presentation"""

    def __init__(self):
        self.max_words_per_slide = 30

    def extract_detailed_slides(self, analysis: Any) -> EnhancedOrganizedPresentationV3:
        """
        Extract slides from analysis with V3 requirements
        
        Args:
            analysis: Analysis object from AI
            
        Returns:
            Organized presentation with slides
        """
        logger.info("Extracting detailed slides (V3)")
        
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
        
        logger.info(f"Created {len(slides)} slides (V3)")
        
        return EnhancedOrganizedPresentationV3(
            slides=slides,
            total_slides=len(slides)
        )
    
    def _create_title_slide(self, analysis: Any) -> EnhancedSlideContentV3:
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
        
        return EnhancedSlideContentV3(
            title=title,
            bullet_points=bullet_points,
            notes="Welcome slide",
            slide_type="title",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_outline_slide(self) -> EnhancedSlideContentV3:
        """Create outline slide"""
        bullet_points = [
            "Background & Problem",
            "Key Insights",
            "Method & Technical Details",
            "Experiments & Results",
            "Analysis & Discussion",
            "Conclusion & Future Work"
        ]
        
        return EnhancedSlideContentV3(
            title="Outline",
            bullet_points=bullet_points,
            notes="Presentation outline",
            slide_type="section",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_keywords_slide(self, title: str, keywords: List[str]) -> EnhancedSlideContentV3:
        """Create slide with keywords"""
        # Ensure max 30 words
        bullet_points = keywords[:6]  # Max 6 items
        
        return EnhancedSlideContentV3(
            title=title,
            bullet_points=bullet_points,
            notes=f"{title} slide",
            slide_type="content",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_insights_slide(self, insights: List[str]) -> EnhancedSlideContentV3:
        """Create insights slide with emoji"""
        bullet_points = insights[:5]  # Max 5 insights
        
        return EnhancedSlideContentV3(
            title="Key Insights",
            bullet_points=bullet_points,
            notes="Key insights and breakthroughs",
            slide_type="content",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_results_slide(self, results: List[str]) -> EnhancedSlideContentV3:
        """Create results slide with bold numbers"""
        bullet_points = results[:6]  # Max 6 results
        
        return EnhancedSlideContentV3(
            title="Main Results",
            bullet_points=bullet_points,
            notes="Main experimental results",
            slide_type="content",
            word_count=self._count_words(bullet_points)
        )
    
    def _create_table_slide(self, title: str, table_content: str) -> EnhancedSlideContentV3:
        """Create table slide"""
        # Table content is already in Markdown format
        bullet_points = [table_content]
        
        return EnhancedSlideContentV3(
            title=title,
            bullet_points=bullet_points,
            notes=f"{title} table",
            slide_type="table",
            word_count=self._count_table_words(table_content)
        )
    
    def _create_qa_slide(self) -> EnhancedSlideContentV3:
        """Create Q&A slide"""
        return EnhancedSlideContentV3(
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

    def _create_figure_slide(self, title: str, image_path: str, caption: str = "") -> EnhancedSlideContentV3:
        """Create slide with figure"""
        bullet_points = []
        
        # Add image markdown
        if image_path:
            bullet_points.append(f"![{title}]({image_path})")
        
        # Add caption if available
        if caption:
            bullet_points.append(f"*{caption}*")
        
        return EnhancedSlideContentV3(
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

