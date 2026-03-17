"""
Enhanced PPT Generator V3 for PaperReader

V3 Improvements:
- Larger fonts (28px content, 40px title)
- Better spacing
- Table support
- English only
"""

from pathlib import Path
from typing import Union
import logging
import os
import re

logger = logging.getLogger(__name__)

IMAGE_MARKDOWN_RE = re.compile(r'^!\[(?P<alt>.*?)\]\((?P<path>.+?)\)$')
ITALIC_CAPTION_RE = re.compile(r'^\*[^\s].*\*$')


class PPTGenerator:
    """Generates presentation slides in Markdown format (V3)"""

    def __init__(self, template_path: str = "./templates/ppt_template.md"):
        self.template_path = Path(template_path)

    def generate_markdown(self, presentation) -> str:
        """
        Generate Markdown content from V3 presentation

        Args:
            presentation: Organized presentation (V3)

        Returns:
            Markdown string
        """
        logger.info(f"Generating Markdown (V3) for {presentation.total_slides} slides")

        # Start with Marp front matter (V3)
        markdown_lines = [
            "---",
            "marp: true",
            "theme: academic",
            "paginate: true",
            "size: 16:9",
            "style: |",
            "  section {",
            "    font-family: 'Helvetica Neue', Arial, sans-serif;",
            "    font-size: 28px;",  # V3: Larger font (was 22px)
            "    color: #333;",
            "    background: #fff;",
            "    line-height: 1.6;",  # V3: Better line height
            "  }",
            "  h1 {",
            "    color: #2c3e50;",
            "    font-size: 48px;",
            "    font-weight: bold;",
            "  }",
            "  h2 {",  # V3: Larger title (was 32px)
            "    color: #34495e;",
            "    font-size: 40px;",  # V3: Increased from 32px
            "    border-bottom: 3px solid #3498db;",
            "    padding-bottom: 10px;",
            "  }",
            "  ul, ol {",
            "    margin-left: 2em;",
            "  }",
            "  li {",
            "    margin-bottom: 0.8em;",  # V3: More spacing (was 0.4em)
            "    font-size: 26px;",  # V3: Larger (was 20px)
            "    line-height: 1.5;",  # V3: Better readability
            "  }",
            "  strong {",
            "    color: #e74c3c;",
            "    font-weight: bold;",
            "  }",
            "  table {",  # V3: Table styling
            "    border-collapse: collapse;",
            "    width: 100%;",
            "    margin: 1em 0;",
            "    font-size: 22px;",
            "  }",
            "  th, td {",
            "    border: 1px solid #ddd;",
            "    padding: 8px;",
            "    text-align: left;",
            "  }",
            "  th {",
            "    background-color: #3498db;",
            "    color: white;",
            "    font-weight: bold;",
            "  }",
            "---",
            ""
        ]

        # Generate each slide
        for i, slide in enumerate(presentation.slides):
            markdown_lines.extend(self._generate_v3_slide_markdown(slide, i))

        markdown = "\n".join(markdown_lines)
        logger.info(f"Generated {len(markdown)} characters of Markdown (V3)")

        return markdown

    def _generate_v3_slide_markdown(self, slide, slide_num: int) -> list:
        """Generate Markdown for V3 slide content"""
        lines = []

        # Add slide separator (except for first slide)
        if slide_num > 0:
            lines.append("")
            lines.append("---")
            lines.append("")

        # Add title (English only)
        lines.append(f"<!-- Slide {slide_num + 1}: {slide.title} -->")
        lines.append(f"## {slide.title}")
        lines.append("")

        content_lines = self._get_slide_content_lines(slide)

        # Check if this is a table slide
        if hasattr(slide, 'slide_type') and slide.slide_type == 'table':
            for point in content_lines:
                lines.append(point)
        else:
            for point in content_lines:
                point = point.strip()
                if not point:
                    continue

                if self._should_preserve_raw_line(slide, point):
                    lines.append(point)
                elif not point.startswith('-') and not point.startswith('* '):
                    lines.append(f"- {point}")
                else:
                    lines.append(point)

        # Add notes as HTML comment (optional)
        if slide.notes:
            lines.append("")
            lines.append(f"<!-- Notes: {slide.notes} -->")

        return lines

    def _get_slide_content_lines(self, slide) -> list:
        """Collect slide content lines while preserving figure data."""
        content_lines = list(getattr(slide, 'bullet_points', []) or [])

        figure_path = (getattr(slide, 'figure_path', '') or '').strip()
        has_figure = getattr(slide, 'has_figure', False) or bool(figure_path)
        figure_caption = (getattr(slide, 'figure_caption', '') or '').strip()

        if has_figure and figure_path and not any(
            self._is_image_markdown(line.strip())
            for line in content_lines
            if isinstance(line, str)
        ):
            figure_filename = os.path.basename(figure_path)
            correct_path = f"images/{figure_filename}"
            content_lines.append(f"![{figure_caption or slide.title}]({correct_path})")

        if has_figure and figure_caption and not any(
            line.strip() == f"*{figure_caption}*"
            for line in content_lines
            if isinstance(line, str)
        ):
            content_lines.append(f"*{figure_caption}*")

        return content_lines

    def _should_preserve_raw_line(self, slide, line: str) -> bool:
        """Return whether a content line should be emitted as raw Markdown."""
        return (
            getattr(slide, 'slide_type', '') == 'figure'
            or self._is_image_markdown(line)
            or self._is_italic_caption(line)
        )

    def _is_image_markdown(self, line: str) -> bool:
        """Return whether a line is Markdown image syntax."""
        return bool(IMAGE_MARKDOWN_RE.match(line))

    def _is_italic_caption(self, line: str) -> bool:
        """Return whether a line looks like a standalone italic caption."""
        return bool(ITALIC_CAPTION_RE.match(line))

    def save_presentation(self, markdown: str, output_path: str) -> None:
        """Save Markdown to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"Saved Markdown to {output_path}")
