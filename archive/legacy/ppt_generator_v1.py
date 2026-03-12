"""
PPT Generator for PaperReader

Generates Markdown slides and converts to final format
"""

from pathlib import Path
from typing import Optional, List
import subprocess
import logging
import shutil

from .content_extractor import OrganizedPresentation, SlideContent

logger = logging.getLogger(__name__)


class PPTGenerator:
    """Generates presentation slides in Markdown format"""

    def __init__(self, template_path: str = "./templates/ppt_template.md"):
        """
        Initialize PPT generator

        Args:
            template_path: Path to Markdown template
        """
        self.template_path = Path(template_path)

    def generate_markdown(self, presentation: OrganizedPresentation) -> str:
        """
        Generate Markdown content from organized presentation

        Args:
            presentation: Organized presentation with slide content

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
            "    font-size: 24px;",
            "    color: #333;",
            "    background: #fff;",
            "  }",
            "  h1 {",
            "    color: #2c3e50;",
            "    font-size: 48px;",
            "    font-weight: bold;",
            "  }",
            "  h2 {",
            "    color: #34495e;",
            "    font-size: 36px;",
            "    border-bottom: 3px solid #3498db;",
            "    padding-bottom: 10px;",
            "  }",
            "  ul, ol {",
            "    margin-left: 2em;",
            "  }",
            "  li {",
            "    margin-bottom: 0.5em;",
            "  }",
            "  strong {",
            "    color: #e74c3c;",
            "  }",
            "---",
            ""
        ]

        # Generate each slide
        for i, slide in enumerate(presentation.slides):
            markdown_lines.extend(self._generate_slide_markdown(slide, i))

        markdown = "\n".join(markdown_lines)
        logger.info(f"Generated {len(markdown)} characters of Markdown")

        return markdown

    def save_presentation(self, markdown: str, output_path: str) -> None:
        """
        Save Markdown to file

        Args:
            markdown: Markdown content
            output_path: Path to save file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"Saved Markdown to {output_path}")

    def convert_to_html(self, markdown_path: str, output_path: str) -> bool:
        """
        Convert Markdown to HTML using Marp CLI

        Args:
            markdown_path: Path to Markdown file
            output_path: Path for output HTML file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if marp CLI is available
            if not shutil.which('marp'):
                logger.warning("Marp CLI not found. Skipping HTML conversion.")
                logger.info("Install Marp CLI: npm install -g @marp-team/marp-cli")
                return False

            # Run Marp conversion
            result = subprocess.run(
                ['marp', markdown_path, '-o', output_path, '--html'],
                capture_output=True,
                text=True,
                check=True
            )

            logger.info(f"Converted to HTML: {output_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Marp conversion failed: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("Marp CLI not found")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during conversion: {e}")
            return False

    def convert_to_pdf(self, markdown_path: str, output_path: str) -> bool:
        """
        Convert Markdown to PDF using Marp CLI

        Args:
            markdown_path: Path to Markdown file
            output_path: Path for output PDF file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if marp CLI is available
            if not shutil.which('marp'):
                logger.warning("Marp CLI not found. Skipping PDF conversion.")
                return False

            # Run Marp conversion
            result = subprocess.run(
                ['marp', markdown_path, '-o', output_path, '--pdf'],
                capture_output=True,
                text=True,
                check=True
            )

            logger.info(f"Converted to PDF: {output_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Marp conversion failed: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("Marp CLI not found")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during conversion: {e}")
            return False

    def _generate_slide_markdown(self, slide: SlideContent, slide_num: int) -> List[str]:
        """Generate Markdown for a single slide"""
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
                # Clean up the point
                point = point.strip()
                if point:
                    # Add as bullet point
                    if not point.startswith('-') and not point.startswith('*'):
                        lines.append(f"- {point}")
                    else:
                        lines.append(point)

        # Add notes as HTML comment
        if slide.notes:
            lines.append("")
            lines.append(f"<!-- Notes: {slide.notes} -->")

        return lines

    def apply_custom_theme(self, markdown: str, theme_config: dict) -> str:
        """
        Apply custom theme to Markdown

        Args:
            markdown: Original Markdown content
            theme_config: Theme configuration

        Returns:
            Modified Markdown with custom theme
        """
        # For now, just return original
        # Theme customization can be added later
        return markdown

    def generate_standalone_html(self, markdown: str) -> str:
        """
        Generate standalone HTML without Marp CLI

        Args:
            markdown: Markdown content

        Returns:
            Standalone HTML string
        """
        # Simple HTML wrapper
        html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Presentation</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .slide {{
            background: white;
            padding: 60px;
            margin: 20px 0;
            page-break-after: always;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            aspect-ratio: 16/9;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        ul, ol {{
            margin-left: 2em;
            line-height: 1.6;
        }}
        li {{
            margin-bottom: 0.8em;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

        # Convert markdown to simple HTML
        slides = markdown.split('---')
        slide_html = []

        for slide in slides[1:]:  # Skip front matter
            if not slide.strip():
                continue

            # Simple markdown-to-HTML conversion
            content = slide.strip()
            content = self._simple_markdown_to_html(content)

            slide_html.append(f'    <div class="slide">\n{content}\n    </div>')

        return html_template.format(content='\n'.join(slide_html))

    def _simple_markdown_to_html(self, markdown: str) -> str:
        """Simple Markdown to HTML conversion"""
        lines = markdown.split('\n')
        html_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip comments
            if line.startswith('<!--'):
                continue

            # Headers
            if line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                html_lines.append(f'<li>{line[2:]}</li>')
            else:
                html_lines.append(f'<p>{line}</p>')

        return '\n'.join(html_lines)
