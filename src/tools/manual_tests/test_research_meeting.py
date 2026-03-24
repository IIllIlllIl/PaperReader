#!/usr/bin/env python3
"""
Test Research Meeting Pipeline

Tests the new research group meeting optimized pipeline:
1. PDF → AI Analysis (research meeting prompt)
2. JSON → ResearchMeetingAnalysis
3. Analysis → 11-slide presentation
"""

import subprocess
from pathlib import Path

from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.analysis.content_extractor_research_meeting import ResearchMeetingContentExtractor
from src.generation.ppt_generator import PPTGenerator
from src.utils import load_config, get_api_key

def test_research_meeting_pipeline():
    """Test research meeting pipeline"""

    print("🧪 Testing Research Meeting Pipeline")
    print("=" * 60)

    # Load config
    config = load_config()
    api_key = get_api_key(config)

    # Initialize components
    parser = PDFParser("papers/Human-In-the-Loop.pdf")
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=config['ai']['model'])
    extractor = ResearchMeetingContentExtractor()
    generator = PPTGenerator(template_path=config['presentation']['template'])

    # Step 1: Parse PDF
    print("\n📄 Step 1: Parsing PDF...")
    text = parser.extract_text()
    metadata = parser.extract_metadata()
    print(f"✓ Extracted {len(text)} characters")

    # Step 2: AI Analysis
    print("\n🤖 Step 2: AI Analysis (Research Meeting)...")
    analysis = analyzer.analyze_paper_for_meeting(text, metadata.__dict__)
    print(f"✓ Analysis completed (cost: ${analyzer.total_cost:.4f})")
    print(f"  - Motivation points: {len(analysis.motivation)}")
    print(f"  - Core idea: {analysis.core_idea[:50]}...")
    print(f"  - Results: {len(analysis.main_results)}")
    print(f"  - Discussion questions: {len(analysis.discussion_questions)}")

    # Step 3: Extract slides
    print("\n📊 Step 3: Extracting slides...")
    presentation = extractor.extract_research_meeting_slides(analysis)
    print(f"✓ Created {presentation.total_slides} slides")

    # Step 4: Generate markdown
    print("\n📝 Step 4: Generating markdown...")
    markdown = generator.generate_markdown(presentation)

    # Save markdown
    output_path = Path("outputs/intermediates/markdown/Human-In-the-Loop_ResearchMeeting.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"✓ Markdown saved to {output_path}")

    # Step 5: Convert to PPTX
    print("\n📑 Step 5: Converting to PPTX...")
    result = subprocess.run([
        "python3", "-m", "src.tools.md_to_pptx",
        str(output_path),
        "outputs/slides/Human-In-the-Loop_ResearchMeeting.pptx"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ PPTX generated successfully")
        print(result.stdout)
    else:
        print(f"❌ PPTX generation failed")
        print(result.stderr)

    # Summary
    print("\n" + "=" * 60)
    print("✅ Research Meeting Pipeline Test Complete!")
    print("=" * 60)
    print(f"\n📊 Slide Structure:")
    print(f"  - Title")
    print(f"  - Motivation (WHY)")
    print(f"  - Problem Definition")
    print(f"  - Related Work")
    print(f"  - Core Idea")
    print(f"  - Method Overview")
    print(f"  - Method Details")
    print(f"  - Experiment Setup")
    print(f"  - Results")
    print(f"  - Limitations")
    print(f"  - Takeaways + Discussion")
    print(f"\n💰 Total Cost: ${analyzer.total_cost:.4f}")
    print(f"\n📁 Output Files:")
    print(f"  - {output_path}")
    print(f"  - outputs/slides/Human-In-the-Loop_ResearchMeeting.pptx")


if __name__ == "__main__":
    test_research_meeting_pipeline()
