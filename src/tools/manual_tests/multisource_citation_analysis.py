#!/usr/bin/env python3
"""
Example: Multi-Source Citation Analysis

Demonstrates Phase 2 features:
- Multi-source integration (OpenAlex, Semantic Scholar, OpenCitations)
- Cross-validation with configurable thresholds
- Verification scores and source tracking
"""

from src.analysis.citation_analyzer import CitationAnalyzer
import json


def main():
    print("=== Multi-Source Citation Analysis Example ===\n")

    # Initialize analyzer
    analyzer = CitationAnalyzer(cache_dir="outputs/citations", cache_days=7)

    # Setup Semantic Scholar (optional, but recommended)
    print("Setting up Semantic Scholar...")
    analyzer.setup_semantic_scholar()
    print(f"Available sources: {analyzer.sources}\n")

    # Example 1: High-confidence analysis (min_sources=2)
    print("=" * 70)
    print("Example 1: High-Confidence Analysis (requires 2+ sources)")
    print("=" * 70)

    result = analyzer.analyze_citations_multisource(
        paper_title="Attention Is All You Need",
        authors="Vaswani",
        year=2017,
        min_sources=2  # Only citations verified by 2+ sources
    )

    print(f"\nTotal verified citations: {result['total_citations']}")
    print(f"Minimum sources required: {result['min_sources_required']}")

    print(f"\nRaw counts by source:")
    for source, count in result['total_raw'].items():
        print(f"  {source}: {count}")

    print(f"\nVerified counts by source:")
    for source, count in result['by_source_coverage'].items():
        print(f"  {source}: {count}")

    if result['citations']:
        print(f"\nTop 5 verified citations:")
        for i, cit in enumerate(result['citations'][:5], 1):
            print(f"\n{i}. {cit.get('title', 'N/A')[:80]}")
            print(f"   Year: {cit.get('year')}")
            print(f"   Verified by: {cit.get('sources', cit.get('verified_by', []))}")
            if 'verification_score' in cit:
                print(f"   Confidence: {cit['verification_score']:.0%}")

    # Example 2: Comprehensive analysis (min_sources=1)
    print("\n" + "=" * 70)
    print("Example 2: Comprehensive Analysis (requires 1+ sources)")
    print("=" * 70)

    result2 = analyzer.analyze_citations_multisource(
        paper_title="BERT: Pre-training of Deep Bidirectional Transformers",
        authors="Devlin",
        year=2018,
        min_sources=1  # All citations from any source
    )

    print(f"\nTotal citations: {result2['total_citations']}")
    print(f"Sources used: {result2['sources_used']}")

    print(f"\nCitations by year (last 5 years):")
    recent_years = dict(list(result2['by_year'].items())[-5:])
    for year, count in recent_years.items():
        print(f"  {year}: {count}")

    # Example 3: Save results for further analysis
    print("\n" + "=" * 70)
    print("Saving results to JSON...")
    print("=" * 70)

    output_file = "outputs/citation_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Results saved to: {output_file}")

    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main()
