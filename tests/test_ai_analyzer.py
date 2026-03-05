"""
Tests for AI Analyzer
"""

import pytest
from src.ai_analyzer import AIAnalyzer, PaperAnalysis, PresentationContent


class TestAIAnalyzer:
    """Test AI analyzer"""

    def test_analyzer_init(self):
        """Test analyzer initialization"""
        # Would need API key for real test
        assert AIAnalyzer is not None

    def test_paper_analysis_dataclass(self):
        """Test PaperAnalysis dataclass"""
        analysis = PaperAnalysis(
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            problem="Test problem",
            motivation="Test motivation",
            method="Test method",
            innovations=["Innovation 1"],
            experiments="Test experiments",
            results=["Result 1"],
            pros=["Pro 1"],
            cons=["Con 1"],
            conclusions="Test conclusions",
            future_work="Test future work"
        )

        assert analysis.title == "Test Paper"
        assert len(analysis.authors) == 2
        assert len(analysis.innovations) == 1

    def test_presentation_content_dataclass(self):
        """Test PresentationContent dataclass"""
        content = PresentationContent(
            title="Test",
            authors="Test Author",
            venue="Test Venue",
            year="2024",
            motivation=["Motivation 1"],
            existing_problems=["Problem 1"],
            research_problem="Test problem",
            method_overview="Test method",
            technical_details=["Detail 1"],
            innovations=["Innovation 1"],
            experimental_setup="Test setup",
            main_results=["Result 1"],
            result_analysis="Test analysis",
            discussion="Test discussion",
            pros=["Pro 1"],
            cons=["Con 1"],
            future_work=["Future 1"],
            conclusions="Test conclusions"
        )

        assert content.title == "Test"
        assert len(content.motivation) == 1


class TestPromptTemplates:
    """Test AI prompt templates"""

    def test_quick_analysis_prompt_exists(self):
        """Test quick analysis prompt exists"""
        assert hasattr(AIAnalyzer, 'QUICK_ANALYSIS_PROMPT')
        assert len(AIAnalyzer.QUICK_ANALYSIS_PROMPT) > 0

    def test_full_analysis_prompt_exists(self):
        """Test full analysis prompt exists"""
        assert hasattr(AIAnalyzer, 'FULL_ANALYSIS_PROMPT')
        assert len(AIAnalyzer.FULL_ANALYSIS_PROMPT) > 0

    def test_prompts_contain_placeholders(self):
        """Test prompts contain necessary placeholders"""
        assert '{paper_text}' in AIAnalyzer.QUICK_ANALYSIS_PROMPT
        assert '{paper_text}' in AIAnalyzer.FULL_ANALYSIS_PROMPT
