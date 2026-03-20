"""Integration tests for citation analysis in pipeline."""

import pytest
from pathlib import Path
import shutil
from src.analysis.citation_analyzer import CitationAnalyzer
from src.visualization.citation_charts import CitationChartGenerator
from src.config.citation_config import CitationConfig


@pytest.fixture
def test_env():
    """Setup test environment."""
    test_dirs = ['test_outputs/images/citations', 'test_outputs/slides', 'test_outputs/citations']
    for d in test_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree('test_outputs', ignore_errors=True)


@pytest.fixture
def citation_config():
    """Create test configuration."""
    return CitationConfig(
        enable_openalex=True,
        enable_semantic_scholar=False,  # Disable for faster tests
        enable_opencitations=False,
        min_sources=1,
        cache_dir='test_outputs/citations',
        cache_days=1
    )


def test_citation_config():
    """Test citation configuration."""
    config = CitationConfig.default()
    assert config.enable_openalex is True
    assert config.min_sources == 2
    assert config.cache_days == 7


def test_chart_generation(test_env):
    """Test chart generation."""
    chart_gen = CitationChartGenerator(output_dir='test_outputs/images/citations')

    # Test year trend chart
    by_year = {2023: 5, 2024: 12, 2025: 8}
    year_chart = chart_gen.generate_year_trend_chart(by_year, paper_year=2023)
    assert year_chart is not None
    assert Path(year_chart).exists()

    # Test source coverage chart
    coverage = {'openalex': 15, 'semantic_scholar': 12, 'opencitations': 8}
    cov_chart = chart_gen.generate_source_coverage_chart(coverage)
    assert cov_chart is not None
    assert Path(cov_chart).exists()


def test_chart_generation_empty_data(test_env):
    """Test chart generation with empty data."""
    chart_gen = CitationChartGenerator(output_dir='test_outputs/images/citations')

    # Empty data should return None
    assert chart_gen.generate_year_trend_chart({}) is None
    assert chart_gen.generate_source_coverage_chart({}) is None


def test_citation_analyzer_basic(citation_config):
    """Test basic citation analyzer functionality."""
    analyzer = CitationAnalyzer(
        cache_dir=citation_config.cache_dir,
        cache_days=citation_config.cache_days
    )

    # Test basic analysis
    result = analyzer.analyze_citations(
        paper_title="Attention Is All You Need",
        year=2017
    )

    assert result is not None
    assert 'total_citations' in result
    assert 'citations' in result
    assert 'by_year' in result


def test_citation_data_structure():
    """Test citation data structure."""
    from src.analysis.ai_analyzer import PaperAnalysis

    analysis = PaperAnalysis(
        title="Test Paper",
        authors="Test Author",
        year="2024",
        summary="Test summary"
    )

    # Add citation data
    analysis.citation_data = {
        'total_citations': 25,
        'sources_used': ['openalex'],
        'min_sources_required': 2,
        'by_year': {2023: 5, 2024: 15, 2025: 5},
        'citations': [
            {'title': 'Citation 1', 'authors': ['Author A'], 'year': 2024},
            {'title': 'Citation 2', 'authors': ['Author B'], 'year': 2024}
        ]
    }
    analysis.has_citation_data = True

    assert analysis.has_citation_data is True
    assert analysis.citation_data['total_citations'] == 25


def test_slide_planner_with_citations(test_env):
    """Test slide planner with citation data."""
    from src.planning.slide_planner import SlidePlanner
    from src.analysis.ai_analyzer import PaperAnalysis

    # Create mock analysis with citation data
    analysis = PaperAnalysis(
        title="Test Paper",
        authors="Test Author",
        year="2024",
        summary="Test summary",
        research_background_keywords=["background1", "background2"],
        research_gap_keywords=["gap1"],
        key_insights=["insight1"],
        framework_name="TestFramework",
        key_components=["comp1"],
        workflow_steps=["step1"],
        core_algorithms=["algo1"],
        key_techniques=["tech1"],
        main_results=["result1"],
        key_findings=["finding1"],
        implications=["imp1"],
        strengths=["strength1"],
        limitations_keywords=["limit1"],
        future_work_keywords=["future1"],
        key_takeaways=["takeaway1"]
    )

    # Add citation data
    analysis.citation_data = {
        'total_citations': 10,
        'sources_used': ['openalex', 'semantic_scholar'],
        'min_sources_required': 2,
        'by_year': {2023: 3, 2024: 4, 2025: 3},
        'citations': [
            {'title': 'Test Citation 1', 'authors': ['Author A'], 'year': 2024},
            {'title': 'Test Citation 2', 'authors': ['Author B'], 'year': 2025}
        ],
        'last_updated': '2026-03-18T12:00:00'
    }
    analysis.has_citation_data = True

    # Generate slide plan
    planner = SlidePlanner(api_key="dummy")  # Won't actually call API in structured mode
    plan = planner._create_structured_plan(analysis)

    # Check if citation slide exists
    citation_slides = [s for s in plan.slides if 'Citation Analysis' in s.title]
    assert len(citation_slides) == 1, "Should have exactly one citation slide"

    # Verify slide content
    citation_slide = citation_slides[0]
    assert any('10' in kp for kp in citation_slide.key_points)  # Total citations
    assert any('openalex' in kp.lower() for kp in citation_slide.key_points)  # Source names


def test_no_citation_slide_when_no_data():
    """Test that no citation slide is added when data is missing."""
    from src.planning.slide_planner import SlidePlanner
    from src.analysis.ai_analyzer import PaperAnalysis

    # Create analysis without citation data
    analysis = PaperAnalysis(
        title="Test Paper",
        authors="Test Author",
        year="2024",
        summary="Test summary",
        research_background_keywords=["background1"],
        research_gap_keywords=["gap1"],
        key_insights=["insight1"],
        framework_name="TestFramework",
        key_components=["comp1"],
        workflow_steps=["step1"],
        core_algorithms=["algo1"],
        key_techniques=["tech1"],
        main_results=["result1"],
        key_findings=["finding1"],
        implications=["imp1"],
        strengths=["strength1"],
        limitations_keywords=["limit1"],
        future_work_keywords=["future1"],
        key_takeaways=["takeaway1"]
    )
    analysis.has_citation_data = False

    # Generate slide plan
    planner = SlidePlanner(api_key="dummy")
    plan = planner._create_structured_plan(analysis)

    # Check that NO citation slide exists
    citation_slides = [s for s in plan.slides if 'Citation Analysis' in s.title]
    assert len(citation_slides) == 0, "Should NOT have citation slide when no data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
