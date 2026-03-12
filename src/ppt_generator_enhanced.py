"""
Enhanced PPT Generator for PaperReader

Generates detailed Markdown slides from enhanced content
"""

from pathlib import Path
from typing import Union
import logging

from .content_extractor import OrganizedPresentation
from .content_extractor_enhanced import EnhancedOrganizedPresentation

logger = logging.getLogger(__name__)


class EnhancedPPTGenerator:
    """Generates detailed presentation slides in Markdown format"""

    def __init__(self, template_path: str = "./templates/ppt_template.md"):
        self.template_path = Path(template_path)

    def generate_markdown(self, presentation: Union[OrganizedPresentation, EnhancedOrganizedPresentation]) -> str:
        """
        Generate Markdown content from presentation
        
        Args:
            presentation: Organized presentation (standard or enhanced)
            
        Returns:
            Markdown string
        """
        logger.info(f"Generating Markdown for {presentation.total_slides} slides")

        # Start with Marp front matter
        markdown_lines = [
            "---",
            "marp: true",
            "theme: academic",
            "paginate: true",
            "size: 16:9",
            "style: |",
            "  section {",
            "    font-family: 'Helvetica Neue', Arial, sans-serif;",
            "    font-size: 22px;",  # Slightly smaller to fit more content
            "    color: #333;",
            "    background: #fff;",
            "  }",
            "  h1 {",
            "    color: #2c3e50;",
            "    font-size: 44px;",
            "    font-weight: bold;",
            "  }",
            "  h2 {",
            "    color: #34495e;",
            "    font-size: 32px;",  # Smaller to fit longer titles
            "    border-bottom: 3px solid #3498db;",
            "    padding-bottom: 10px;",
            "  }",
            "  ul, ol {",
            "    margin-left: 1.5em;",
            "  }",
            "  li {",
            "    margin-bottom: 0.4em;",  # Tighter spacing for more content
            "    font-size: 20px;",
            "    line-height: 1.4;",
            "  }",
            "  strong {",
            "    color: #e74c3c;",
            "  }",
            "---",
            ""
        ]

        # Generate each slide
        for i, slide in enumerate(presentation.slides):
            # Check if this is enhanced slide content
            if hasattr(slide, 'slide_type'):
                markdown_lines.extend(self._generate_enhanced_slide_markdown(slide, i))
            else:
                markdown_lines.extend(self._generate_standard_slide_markdown(slide, i))

        markdown = "\n".join(markdown_lines)
        logger.info(f"Generated {len(markdown)} characters of Markdown")

        return markdown

    def _generate_enhanced_slide_markdown(self, slide, slide_num: int) -> list:
        """Generate Markdown for enhanced slide content"""
        lines = []

        # Add slide separator (except for first slide)
        if slide_num > 0:
            lines.append("")
            lines.append("---")
            lines.append("")

        # Add title
        lines.append(f"<!-- Slide {slide_num + 1}: {slide.title} -->")
        lines.append(f"## {slide.title}")
        lines.append("")

        # Add content with proper formatting
        if slide.bullet_points:
            for point in slide.bullet_points:
                point = point.strip()
                if not point:
                    # Empty line for spacing
                    lines.append("")
                elif point.startswith('✓') or point.startswith('✗'):
                    # Pros/cons - keep as is
                    lines.append(f"- {point}")
                elif point.startswith(('📚', '❓', '💡', '🔧', '🔬', '📊', '🎯', '⚡', '🚀', '🤔', '⚙️', '📊', '✅', '🔬', '📋', '🔮')):
                    # Emoji bullets - keep as is
                    lines.append(f"- {point}")
                elif not point.startswith('-') and not point.startswith('*'):
                    lines.append(f"- {point}")
                else:
                    lines.append(point)

        # Add notes as HTML comment
        if slide.notes:
            lines.append("")
            lines.append(f"<!-- Notes: {slide.notes} -->")

        return lines

    def _generate_standard_slide_markdown(self, slide, slide_num: int) -> list:
        """Generate Markdown for standard slide content"""
        lines = []

        # Add slide separator (except for first slide)
        if slide_num > 0:
            lines.append("")
            lines.append("---")
            lines.append("")

        # Add title
        lines.append(f"<!-- Slide {slide_num + 1}: {slide.title} -->")
        lines.append(f"## {slide.title}")
        lines.append("")

        # Add content
        if slide.bullet_points:
            for point in slide.bullet_points:
                point = point.strip()
                if point:
                    if not point.startswith('-') and not point.startswith('*'):
                        lines.append(f"- {point}")
                    else:
                        lines.append(point)

        # Add notes as HTML comment
        if slide.notes:
            lines.append("")
            lines.append(f"<!-- Notes: {slide.notes} -->")

        return lines

    def save_presentation(self, markdown: str, output_path: str) -> None:
        """Save Markdown to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"Saved Markdown to {output_path}")
