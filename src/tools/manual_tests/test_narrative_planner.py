#!/usr/bin/env python3
"""
Test Narrative Planner

Tests the narrative extraction pipeline:
1. Parse PDF
2. Analyze paper
3. Extract narrative
4. Display results
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.planning.narrative_planner import NarrativePlanner
from src.utils import load_config, get_api_key


def test_narrative_planner():
    """Test narrative extraction from paper analysis"""

    print("📖 Testing Narrative Planner")
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

    # Step 3: Extract narrative
    print("\n📖 Step 3: Extracting narrative...")
    planner = NarrativePlanner(api_key=api_key, model=config['ai']['model'])
    narrative = planner.extract_narrative(analysis)
    print(f"✓ Narrative extracted (cost: ${planner.total_cost:.4f})")

    # Step 4: Display narrative
    print("\n" + "=" * 70)
    print("📖 EXTRACTED NARRATIVE")
    print("=" * 70)

    print(f"\n🎣 Hook:\n  {narrative.hook}")

    print(f"\n❓ Problem:\n  {narrative.problem}")

    print(f"\n⚠️  Limitations of Prior Work:\n  {narrative.limitations_of_prior_work}")

    print(f"\n💡 Key Idea:\n  {narrative.key_idea}")

    print(f"\n🔧 Method:\n  {narrative.method}")

    print(f"\n📊 Evidence:\n  {narrative.evidence}")

    print(f"\n🔮 Implications:\n  {narrative.implications}")

    # Validation
    print("\n" + "=" * 70)
    print("✅ VALIDATION")
    print("=" * 70)

    narrative_dict = narrative.to_dict()
    all_fields_filled = all(narrative_dict.values())

    if all_fields_filled:
        print("✓ All narrative fields filled")
    else:
        missing = [k for k, v in narrative_dict.items() if not v]
        print(f"⚠️ Missing fields: {missing}")

    # Check field lengths
    print("\n📝 Field Lengths:")
    for field, value in narrative_dict.items():
        length = len(value)
        status = "✓" if 20 <= length <= 500 else "⚠️"
        print(f"  {status} {field}: {length} chars")

    # Quality checks
    print("\n🎯 Quality Checks:")

    # Hook should be attention-grabbing
    if any(word in narrative.hook.lower() for word in ["but", "however", "fail", "promise", "challenge"]):
        print("✓ Hook is attention-grabbing")
    else:
        print("⚠️ Hook could be more compelling")

    # Key idea should be concise
    if len(narrative.key_idea) < 200:
        print("✓ Key idea is concise")
    else:
        print("⚠️ Key idea is too long")

    # Evidence should contain numbers
    if any(char.isdigit() for char in narrative.evidence):
        print("✓ Evidence contains numbers")
    else:
        print("⚠️ Evidence lacks specific numbers")

    # Cost summary
    print("\n" + "=" * 70)
    print("💰 COST SUMMARY")
    print("=" * 70)
    print(f"Paper Analysis: ${analyzer.total_cost:.4f}")
    print(f"Narrative Extraction: ${planner.total_cost:.4f}")
    print(f"Total: ${analyzer.total_cost + planner.total_cost:.4f}")

    return narrative


if __name__ == "__main__":
    test_narrative_planner()
