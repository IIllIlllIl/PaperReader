"""
Tests for PPT Generator
"""

import pytest
from src.generation.ppt_generator import PPTGenerator
from src.analysis.content_extractor import ContentExtractor, OrganizedPresentation, SlideContent


class TestPPTGenerator:
    """Test PPT generator"""

    def test_generator_init(self):
        """Test generator initialization"""
        generator = PPTGenerator()
        assert generator is not None

    def test_generate_markdown(self):
        """Test Markdown generation"""
        generator = PPTGenerator()

        # Create sample presentation
        slides = [
            SlideContent(title="Test Slide", bullet_points=["Point 1", "Point 2"], notes="Test notes")
        ]
        presentation = OrganizedPresentation(slides=slides, total_slides=1)

        # Generate Markdown
        markdown = generator.generate_markdown(presentation)

        assert markdown is not None
        assert len(markdown) > 0
        assert "marp: true" in markdown
        assert "Test Slide" in markdown

    def test_save_presentation(self, tmp_path):
        """Test saving presentation to file"""
        generator = PPTGenerator()

        markdown = "---\nmarp: true\n---\n\n## Test\n\n- Point 1"
        output_path = tmp_path / "test.md"

        generator.save_presentation(markdown, str(output_path))

        assert output_path.exists()
        assert output_path.read_text() == markdown


class TestContentExtractor:
    """Test content extractor"""

    def test_extractor_init(self):
        """Test extractor initialization"""
        extractor = ContentExtractor()
        assert extractor is not None

    def test_suggest_visualizations(self):
        """Test visualization suggestions"""
        extractor = ContentExtractor()

        results = [
            "Accuracy improved to 95%",
            "Faster than baseline"
        ]

        suggestions = extractor.suggest_visualizations(results)

        assert len(suggestions) <= 5
        assert all('type' in s for s in suggestions)
        assert all('suggestion' in s for s in suggestions)
