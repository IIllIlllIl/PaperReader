"""
Tests for AI Analyzer
"""

import pytest
from src.analysis.ai_analyzer import AIAnalyzer, PaperAnalysis


class TestAIAnalyzer:
    """Test AI analyzer"""

    def test_analyzer_init(self):
        """Test analyzer initialization"""
        # Would need API key for real test
        assert AIAnalyzer is not None

    def test_paper_analysis_dataclass(self):
        """Test PaperAnalysis dataclass (V3 API)"""
        # V3 uses keyword-first approach with many fields
        # Just test that we can create an instance with minimal required fields
        analysis = PaperAnalysis(
            title="Test Paper",
            authors="Author 1, Author 2",
            year="2024",
            summary="Test summary",
            research_background_keywords=["keyword1", "keyword2"],
            research_context_stats={"metric": "value"},
            research_gap_keywords=["gap1"],
            research_problem_statement="Test problem statement",
            key_insights=["insight1", "insight2"],
            framework_name="TestFramework",
            key_components=["component1"],
            workflow_steps=["step1"],
            core_algorithms=["algo1"],
            key_techniques=["tech1"],
            techniques_comparison_table={"Tech": ["Pro", "Con"]},
            datasets_table={"Dataset": "Description"},
            baselines_table={"Baseline": "Description"},
            metrics_table={"Metric": "Description"},
            experimental_setup_table={"Config": "Value"},
            main_results=["result1"],
            performance_comparison_table={"Metric": ["Val1", "Val2"]},
            key_findings=["finding1"],
            implications=["implication1"],
            strengths=["strength1"],
            limitations_keywords=["limitation1"],
            future_work_keywords=["future1"],
            key_takeaways=["takeaway1"]
        )

        assert analysis.title == "Test Paper"
        assert analysis.authors == "Author 1, Author 2"
        assert len(analysis.research_background_keywords) == 2
        assert len(analysis.key_insights) == 2


class TestAnalyzerMethods:
    """Test analyzer methods exist"""

    def test_analyze_paper_detailed_method_exists(self):
        """Test analyze_paper_detailed method exists"""
        assert hasattr(AIAnalyzer, 'analyze_paper_detailed')

    def test_get_stats_method_exists(self):
        """Test get_stats method exists"""
        assert hasattr(AIAnalyzer, 'get_stats')
