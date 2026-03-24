#!/usr/bin/env python3
"""
Test Slide Planner

Tests the new slide planning layer:
1. Load existing PaperAnalysis
2. Generate SlidePlan using LLM
3. Display slide topics
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.planning.slide_planner import SlidePlanner
from src.utils import load_config, get_api_key


def test_slide_planner():
    """Test the slide planning layer"""

    print("🧪 Testing Slide Planning Layer")
    print("=" * 70)

    # Load config
    config = load_config()
    api_key = get_api_key(config)

    # Step 1: Parse PDF (use existing paper)
    print("\n📄 Step 1: Parsing PDF...")
    pdf_path = "papers/Human-In-the-Loop.pdf"
    parser = PDFParser(pdf_path)
    text = parser.extract_text()
    metadata = parser.extract_metadata()
    print(f"✓ Extracted {len(text)} characters")

    # Step 2: Analyze paper (use existing analyzer)
    print("\n🤖 Step 2: Analyzing paper...")
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=config['ai']['model'])
    analysis = analyzer.analyze_paper_for_meeting(text, metadata.__dict__)
    print(f"✓ Analysis completed (cost: ${analyzer.total_cost:.4f})")
    print(f"  - Title: {analysis.title}")
    print(f"  - Authors: {analysis.authors}")
    print(f"  - Year: {analysis.year}")
    print(f"  - Motivation points: {len(analysis.motivation)}")
    print(f"  - Core idea: {analysis.core_idea[:60]}...")

    # Step 3: Plan slides (NEW!)
    print("\n📊 Step 3: Planning slides...")
    planner = SlidePlanner(api_key=api_key, model=config['ai']['model'])
    slide_plan = planner.plan_slides(analysis)
    print(f"✓ Slide plan generated (cost: ${planner.total_cost:.4f})")
    print(f"  - Total slides: {slide_plan.total_slides}")

    # Step 4: Display slide plan
    print("\n" + "=" * 70)
    print("📋 SLIDE PLAN")
    print("=" * 70)

    for i, slide in enumerate(slide_plan.slides, 1):
        print(f"\n[Slide {i}] {slide.title}")
        print(f"  Type: {slide.slide_type}")
        if slide.key_points:
            print("  Key Points:")
            for j, point in enumerate(slide.key_points, 1):
                print(f"    {j}. {point}")
        if slide.notes:
            print(f"  Notes: {slide.notes}")

    # Step 5: Validate
    print("\n" + "=" * 70)
    print("✅ VALIDATION")
    print("=" * 70)

    # Check slide count
    if slide_plan.total_slides == 11:
        print("✓ Correct number of slides (11)")
    else:
        print(f"⚠️ Expected 11 slides, got {slide_plan.total_slides}")

    # Check for empty slides
    empty_slides = [i for i, s in enumerate(slide_plan.slides) if not s.key_points]
    if not empty_slides:
        print("✓ No empty slides")
    else:
        print(f"⚠️ Empty slides found: {empty_slides}")

    # Check key points per slide
    slides_with_wrong_count = [
        (i, len(s.key_points))
        for i, s in enumerate(slide_plan.slides)
        if len(s.key_points) < 3 or len(s.key_points) > 5
    ]
    if not slides_with_wrong_count:
        print("✓ All slides have 3-5 key points")
    else:
        print(f"⚠️ Slides with wrong key point count:")
        for idx, count in slides_with_wrong_count:
            print(f"    Slide {idx + 1}: {count} points")

    # Step 6: Save slide plan
    print("\n💾 Saving slide plan...")
    output_path = Path("outputs/plans/slide_plan.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(slide_plan.to_dict(), f, indent=2)

    print(f"✓ Slide plan saved to {output_path}")

    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total Slides: {slide_plan.total_slides}")
    print(f"Total Key Points: {sum(len(s.key_points) for s in slide_plan.slides)}")
    print(f"Analysis Cost: ${analyzer.total_cost:.4f}")
    print(f"Planning Cost: ${planner.total_cost:.4f}")
    print(f"Total Cost: ${analyzer.total_cost + planner.total_cost:.4f}")
    print(f"\n📁 Output: {output_path}")

    return slide_plan


if __name__ == "__main__":
    test_slide_planner()
