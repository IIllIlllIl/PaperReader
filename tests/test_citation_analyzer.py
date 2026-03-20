"""Tests for CitationAnalyzer - Phase 1"""

import pytest
from pathlib import Path
import shutil
from src.analysis.citation_analyzer import CitationAnalyzer


@pytest.fixture
def analyzer():
    """Create CitationAnalyzer instance with test cache."""
    analyzer = CitationAnalyzer(cache_dir="test_outputs/citations")
    yield analyzer
    # Cleanup
    shutil.rmtree("test_outputs", ignore_errors=True)


def test_cache_mechanism(analyzer):
    """Test cache save and retrieve."""
    cache_key = analyzer._get_cache_key("test_key")
    test_data = {"test": "data", "number": 123}

    # Save to cache
    analyzer._save_cache(cache_key, test_data)

    # Retrieve from cache
    cached = analyzer._get_cached(cache_key)
    assert cached == test_data


def test_cache_expiration(analyzer):
    """Test that expired cache is not returned."""
    cache_key = analyzer._get_cache_key("expired_key")
    test_data = {"test": "expired"}

    # Save to cache
    analyzer._save_cache(cache_key, test_data)

    # Manually expire by modifying timestamp
    cache_file = analyzer.cache_dir / f"{cache_key}.json"
    import json
    from datetime import datetime, timedelta

    with open(cache_file) as f:
        cached = json.load(f)

    # Set timestamp to 8 days ago (beyond default 7-day expiration)
    cached['timestamp'] = (datetime.now() - timedelta(days=8)).isoformat()

    with open(cache_file, 'w') as f:
        json.dump(cached, f)

    # Should return None for expired cache
    result = analyzer._get_cached(cache_key)
    assert result is None


def test_cache_key_consistency(analyzer):
    """Test that cache keys are consistent for same input."""
    key1 = analyzer._get_cache_key("test_identifier")
    key2 = analyzer._get_cache_key("test_identifier")
    assert key1 == key2

    # Different inputs should produce different keys
    key3 = analyzer._get_cache_key("different_identifier")
    assert key1 != key3


def test_group_by_year(analyzer):
    """Test grouping citations by year."""
    citations = [
        {"year": 2023, "title": "Paper 1"},
        {"year": 2023, "title": "Paper 2"},
        {"year": 2024, "title": "Paper 3"},
        {"year": 2022, "title": "Paper 4"},
        {"title": "No year"},  # Should be skipped
    ]

    by_year = analyzer._group_by_year(citations)

    assert by_year[2022] == 1
    assert by_year[2023] == 2
    assert by_year[2024] == 1
    assert 2025 not in by_year  # Year not in data
    assert list(by_year.keys()) == [2022, 2023, 2024]  # Sorted


def test_get_paper_id_openalex_known_paper(analyzer):
    """Test OpenAlex paper lookup with a known paper."""
    # Use BERT paper which has correct metadata in OpenAlex
    result = analyzer.get_paper_id_openalex(
        title="BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        authors="Devlin",
        year=2018
    )

    # Should find the paper
    assert result is not None
    # Note: OpenAlex metadata may have year discrepancies
    assert 'openalex_id' in result
    assert 'title' in result
    assert result['cited_by_count'] > 0  # Should have citations


def test_get_paper_id_openalex_nonexistent(analyzer):
    """Test OpenAlex lookup for nonexistent paper."""
    result = analyzer.get_paper_id_openalex(
        title="Nonexistent Paper Title That Definitely Doesn't Exist XYZ123",
        authors="Fake Author",
        year=2099
    )

    # Should return None for nonexistent paper
    assert result is None


def test_fetch_citations_openalex_invalid_id(analyzer):
    """Test fetching citations with invalid ID."""
    citations = analyzer.fetch_citations_openalex("INVALID_ID_12345")
    assert isinstance(citations, list)
    assert len(citations) == 0  # Should return empty list for invalid ID


def test_analyze_citations_no_paper(analyzer):
    """Test behavior when paper not found."""
    result = analyzer.analyze_citations(
        paper_title="Nonexistent Paper Title That Definitely Doesn't Exist 12345"
    )
    assert result["total_citations"] == 0
    assert len(result["citations"]) == 0
    assert result["paper_found"] is False


def test_analyze_citations_known_paper(analyzer):
    """Test full analysis with a known paper."""
    # Use a well-cited paper
    result = analyzer.analyze_citations(
        paper_title="Attention Is All You Need",
        authors="Vaswani",
        year=2017
    )

    # Should find the paper and citations
    assert result["paper_found"] is True
    assert result["total_citations"] > 0
    assert len(result["citations"]) > 0
    assert len(result["citations"]) <= 10  # Should be limited to 10
    assert "OpenAlex" in result["sources_used"]
    assert "by_year" in result
    assert len(result["by_year"]) > 0
    assert "last_updated" in result
    assert "paper_info" in result


def test_analyze_citations_structure(analyzer):
    """Test that result has correct structure."""
    result = analyzer.analyze_citations(
        paper_title="Attention Is All You Need",
        year=2017
    )

    # Check all required fields
    assert "total_citations" in result
    assert "citations" in result
    assert "by_year" in result
    assert "sources_used" in result
    assert "last_updated" in result

    # Check types
    assert isinstance(result["total_citations"], int)
    assert isinstance(result["citations"], list)
    assert isinstance(result["by_year"], dict)
    assert isinstance(result["sources_used"], list)


def test_caching_in_analyze_citations(analyzer):
    """Test that caching works in analyze_citations."""
    # First call should hit API
    result1 = analyzer.analyze_citations(
        paper_title="Attention Is All You Need",
        year=2017
    )

    # Second call should use cache
    result2 = analyzer.analyze_citations(
        paper_title="Attention Is All You Need",
        year=2017
    )

    # Results should be identical
    assert result1["total_citations"] == result2["total_citations"]
    assert result1["paper_info"]["openalex_id"] == result2["paper_info"]["openalex_id"]


# ==================== Phase 2 Tests ====================

def test_semantic_scholar_setup(analyzer):
    """Test Semantic Scholar client initialization."""
    analyzer.setup_semantic_scholar()

    assert analyzer.s2_client is not None
    assert "semantic_scholar" in analyzer.sources


def test_get_paper_id_semanticscholar_known_paper(analyzer):
    """Test Semantic Scholar paper lookup."""
    analyzer.setup_semantic_scholar()

    result = analyzer.get_paper_id_semanticscholar(
        title="Attention Is All You Need",
        authors="Vaswani",
        year=2017
    )

    # Should find the paper
    assert result is not None
    assert 's2_id' in result
    assert 'title' in result
    assert result['citation_count'] > 0


def test_fetch_citations_semanticscholar(analyzer):
    """Test Semantic Scholar citations fetch."""
    analyzer.setup_semantic_scholar()

    # First get paper ID
    paper_info = analyzer.get_paper_id_semanticscholar(
        title="Attention Is All You Need",
        year=2017
    )

    if paper_info:
        citations = analyzer.fetch_citations_semanticscholar(paper_info['s2_id'], limit=10)
        assert isinstance(citations, list)
        if citations:
            assert 'title' in citations[0]
            assert 'year' in citations[0]
            assert citations[0]['source'] == 'semantic_scholar'


def test_fetch_citations_opencitations(analyzer):
    """Test OpenCitations integration."""
    # Use a known DOI
    doi = "10.1038/nature12373"  # Example: CRISPR paper

    citations = analyzer.fetch_citations_opencitations(doi)
    assert isinstance(citations, list)

    # If citations found, check structure
    if citations:
        assert 'citing_doi' in citations[0]
        assert citations[0]['source'] == 'opencitations'


def test_enrich_citation_with_metadata(analyzer):
    """Test DOI enrichment."""
    # Use a known DOI
    doi = "10.1038/nature12373"

    result = analyzer.enrich_citation_with_metadata(doi)

    if result:
        assert 'title' in result
        assert 'year' in result
        assert result['doi'] == doi


def test_cross_validation(analyzer):
    """Test cross-validation logic."""
    # Simulate multi-source data
    citations_by_source = {
        'openalex': [
            {'title': 'Paper A', 'year': 2024, 'doi': '10.1234/a', 'authors': ['Author 1']},
            {'title': 'Paper B', 'year': 2024, 'doi': '10.1234/b', 'authors': ['Author 2']}
        ],
        'semantic_scholar': [
            {'title': 'Paper A', 'year': 2024, 'doi': '10.1234/a', 'authors': ['Author 1']},
            {'title': 'Paper C', 'year': 2025, 'doi': '10.1234/c', 'authors': ['Author 3']}
        ]
    }

    verified = analyzer.cross_validate_citations(citations_by_source, min_sources=2)

    # Paper A should appear in both sources
    assert len(verified) >= 1
    assert any(c['title'] == 'Paper A' for c in verified)

    # Find Paper A and check validation
    paper_a = next((c for c in verified if c['title'] == 'Paper A'), None)
    if paper_a:
        assert len(paper_a['sources']) == 2
        assert 'openalex' in paper_a['sources']
        assert 'semantic_scholar' in paper_a['sources']
        assert 'verification_score' in paper_a


def test_cross_validation_min_sources(analyzer):
    """Test that min_sources filter works."""
    citations_by_source = {
        'openalex': [
            {'title': 'Paper A', 'year': 2024, 'doi': '10.1234/a'}
        ],
        'semantic_scholar': [
            {'title': 'Paper A', 'year': 2024, 'doi': '10.1234/a'},
            {'title': 'Paper B', 'year': 2025, 'doi': '10.1234/b'}
        ],
        'opencitations': [
            {'title': 'Paper A', 'year': 2024, 'doi': '10.1234/a'}
        ]
    }

    # min_sources=3 should only return Paper A
    verified = analyzer.cross_validate_citations(citations_by_source, min_sources=3)
    assert len(verified) == 1
    assert verified[0]['title'] == 'Paper A'
    assert len(verified[0]['sources']) == 3

    # min_sources=2 should return at least Paper A
    verified = analyzer.cross_validate_citations(citations_by_source, min_sources=2)
    assert len(verified) >= 1


def test_analyze_citations_multisource_structure(analyzer):
    """Test multi-source analysis result structure."""
    analyzer.setup_semantic_scholar()

    result = analyzer.analyze_citations_multisource(
        paper_title="Attention Is All You Need",
        authors="Vaswani",
        year=2017,
        min_sources=2
    )

    # Check all required fields
    assert "total_citations" in result
    assert "total_raw" in result
    assert "citations" in result
    assert "by_year" in result
    assert "by_source_coverage" in result
    assert "sources_used" in result
    assert "min_sources_required" in result
    assert "last_updated" in result

    # Check types
    assert isinstance(result["total_citations"], int)
    assert isinstance(result["total_raw"], dict)
    assert isinstance(result["citations"], list)
    assert isinstance(result["by_year"], dict)
    assert isinstance(result["by_source_coverage"], dict)
    assert result["min_sources_required"] == 2


def test_analyze_citations_multisource_verification(analyzer):
    """Test that multi-source analysis includes verification metadata."""
    analyzer.setup_semantic_scholar()

    result = analyzer.analyze_citations_multisource(
        paper_title="Attention Is All You Need",
        year=2017,
        min_sources=2
    )

    # If citations found, check verification metadata
    if result["citations"]:
        citation = result["citations"][0]
        assert "sources" in citation or "verified_by" in citation
        if "verification_score" in citation:
            assert 0 <= citation["verification_score"] <= 1


def test_multisource_error_handling(analyzer):
    """Test that errors in one source don't break the analysis."""
    # Don't initialize Semantic Scholar
    # Analysis should still work with OpenAlex

    result = analyzer.analyze_citations_multisource(
        paper_title="Attention Is All You Need",
        year=2017,
        min_sources=1  # Lower threshold since we only have OpenAlex
    )

    # Should still get results from OpenAlex
    assert result["total_citations"] >= 0
    assert "openalex" in result["sources_used"]
