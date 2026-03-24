#!/usr/bin/env python3
"""
Test Chart Generation

Tests the complete chart generation pipeline:
1. Parse PDF
2. Analyze paper
3. Extract numeric results
4. Generate charts
5. Display results
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.analysis.result_analyzer import ResultAnalyzer
from src.generation.chart_generator import ChartGenerator
from src.utils import load_config, get_api_key


def test_chart_generation():
    """Test chart generation from paper analysis"""

    print("📊 Testing Chart Generation Pipeline")
    print("=" * 70)

    # Load config
    config = load_config()
    api_key = get_api_key(config)

    # Step 1: Parse PDF
    print("\n📄 Step 1: Parsing PDF...")
    pdf_path = "papers/Human-In-the-Loop.pdf"
    parser = PDFParser(pdf_path)
    text = parser.extract_text()
    metadata = parser.extract_metadata()
    print(f"✓ Extracted {len(text)} characters")

    # Step 2: Analyze paper
    print("\n🤖 Step 2: Analyzing paper...")
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=config['ai']['model'])
    analysis = analyzer.analyze_paper_for_meeting(text, metadata.__dict__)
    print(f"✓ Analysis completed (cost: ${analyzer.total_cost:.4f})")
    print(f"  - Main results: {len(analysis.main_results)}")

    # Display extracted results
    print("\n📋 Extracted Results:")
    for i, result in enumerate(analysis.main_results, 1):
        print(f"  {i}. {result}")

    # Step 3: Extract numeric results (NEW!)
    print("\n🔍 Step 3: Extracting numeric results...")
    result_analyzer = ResultAnalyzer()
    numeric_results = result_analyzer.extract_results(analysis)
    print(f"✓ Extracted {len(numeric_results)} numeric results")

    for i, result in enumerate(numeric_results, 1):
        print(f"  {i}. {result.metric}: {result.value}{result.unit} ({result.context})")

    # Step 4: Extract comparisons
    print("\n📊 Step 4: Detecting comparisons...")
    comparisons = result_analyzer.extract_comparisons(analysis)
    print(f"✓ Found {len(comparisons)} comparison patterns")

    for i, comp in enumerate(comparisons, 1):
        print(f"  {i}. {comp.metric}: {comp.methods} -> {comp.values}")

    # Step 5: Generate charts
    print("\n🎨 Step 5: Generating charts...")
    chart_gen = ChartGenerator(output_dir="outputs/charts")

    chart_paths = []

    # Generate comparison charts
    if comparisons:
        print("\n  Generating comparison charts...")
        for i, comparison in enumerate(comparisons, 1):
            chart_name = f"comparison_{i}_{comparison.metric.replace(' ', '_').lower()}"
            chart_path = chart_gen.generate_comparison_chart(comparison, chart_name)
            if chart_path:
                chart_paths.append(chart_path)
                print(f"    ✓ {chart_path}")

    # Generate results summary chart
    if numeric_results:
        print("\n  Generating results summary chart...")
        summary_path = chart_gen.generate_results_summary(
            numeric_results,
            chart_name="results_summary"
        )
        if summary_path:
            chart_paths.append(summary_path)
            print(f"    ✓ {summary_path}")

    # Step 6: Display results
    print("\n" + "=" * 70)
    print("✅ CHART GENERATION COMPLETE")
    print("=" * 70)

    print(f"\n📊 Generated Charts: {len(chart_paths)}")
    for i, path in enumerate(chart_paths, 1):
        chart_file = Path(path)
        size_kb = chart_file.stat().st_size / 1024
        print(f"  {i}. {chart_file.name} ({size_kb:.1f} KB)")

    print(f"\n💰 Total Cost:")
    print(f"  Paper Analysis: ${analyzer.total_cost:.4f}")
    print(f"  Total: ${analyzer.total_cost:.4f}")

    print(f"\n📁 Output Location:")
    print(f"  {chart_gen.output_dir}/")

    # Validation
    print("\n" + "=" * 70)
    print("✅ VALIDATION")
    print("=" * 70)

    if len(chart_paths) > 0:
        print("✓ At least 1 chart generated")
    else:
        print("⚠️ No charts generated")

    if any("comparison" in p for p in chart_paths):
        print("✓ Comparison chart generated")
    else:
        print("⚠️ No comparison chart")

    if any("summary" in p for p in chart_paths):
        print("✓ Results summary chart generated")
    else:
        print("⚠️ No summary chart")

    return chart_paths


if __name__ == "__main__":
    test_chart_generation()
