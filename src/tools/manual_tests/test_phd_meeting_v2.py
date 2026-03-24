#!/usr/bin/env python3
"""
Test PhD Research Meeting Pipeline V2

Enhanced features:
1. Figure extraction from PDF
2. Result interpretations (why it matters)
3. Related work comparison format
4. Discussion depth
5. Presentation script generation
"""

import subprocess
import sys
from pathlib import Path

from src.parser.pdf_parser import PDFParser
from src.parser.pdf_image_extractor import PDFImageExtractor
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.analysis.content_extractor_phd_meeting import PhDMeetingContentExtractorV2
from src.generation.ppt_generator import PPTGenerator
from src.utils import load_config, get_api_key

from src.prompts.phd_meeting_prompt_v2 import PHD_MEETING_PROMPT_V2

def test_phd_meeting_pipeline_v2():
    """Test PhD research meeting pipeline V2 with figure extraction"""

    print("🧪 Testing PhD Research Meeting Pipeline V2")
    print("=" * 70)

    # Load config
    config = load_config()
    api_key = get_api_key(config)

    # Initialize components
    pdf_path = "papers/Human-In-the-Loop.pdf"

    parser = PDFParser(pdf_path)
    image_extractor = PDFImageExtractor(output_dir="outputs/images")
    analyzer_v2 = ResearchMeetingAnalyzer(api_key=api_key, model=config['ai']['model'])
    extractor = PhDMeetingContentExtractorV2()
    generator = PPTGenerator(template_path=config['presentation']['template'])

    # Step 1: Parse PDF
    print("\n📄 Step 1: Parsing PDF...")
    text = parser.extract_text()
    metadata = parser.extract_metadata()
    print(f"✓ Extracted {len(text)} characters from {parser.get_page_count()} pages")

    # Step 2: Extract figures (NEW!)
    print("\n🖼️  Step 2: Extracting figures from PDF...")
    figures = image_extractor.extract_key_figures(pdf_path, max_figures=3)
    print(f"✓ Extracted {len(figures)} figures")
    for i, fig in enumerate(figures, 1):
        print(f"  {i}. {Path(fig['image_path']).name} ({fig['width']}x{fig['height']}) - {fig['caption'][:50]}...")

    # Step 3: AI Analysis (with enhanced prompt)
    print("\n🤖 Step 3: AI Analysis (PhD-level)...")

    # Modify to use V2 prompt (match original signature)
    def generate_v2_prompt(paper_text, max_chars):
        return PHD_MEETING_PROMPT_V2.format(paper_text=paper_text[:max_chars])
    analyzer_v2._generate_research_meeting_prompt = generate_v2_prompt

    analysis = analyzer_v2.analyze_paper_for_meeting(text, metadata.__dict__)
    print(f"✓ Analysis completed (cost: ${analyzer_v2.total_cost:.4f})")
    print(f"  - Motivation: {len(analysis.motivation)} points")
    print(f"  - Core idea: {analysis.core_idea[:60]}...")
    print(f"  - Results with interpretations: {len(analysis.main_results)}")
    print(f"  - Discussion questions: {len(analysis.discussion_questions)}")

    # Step 4: Extract slides (with figures)
    print("\n📊 Step 4: Extracting slides (with figure support)...")
    presentation = extractor.extract_phd_meeting_slides(analysis, figures)
    print(f"✓ Created {presentation.total_slides} slides")

    # Check which slides have figures
    slides_with_figures = [s for s in presentation.slides if s.has_figure]
    print(f"  - {len(slides_with_figures)} slides have figures")

    # Step 5: Generate markdown
    print("\n📝 Step 5: Generating markdown...")
    markdown = generator.generate_markdown(presentation)

    # Save markdown
    output_path = Path("outputs/intermediates/markdown/Human-In-the-Loop_PhD_Meeting_V2.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"✓ Markdown saved to {output_path}")

    # Step 6: Convert to PPTX
    print("\n📑 Step 6: Converting to PPTX...")
    result = subprocess.run([
        sys.executable, "-m", "src.tools.md_to_pptx",
        str(output_path),
        "outputs/slides/Human-In-the-Loop_PhD_Meeting_V2.pptx"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ PPTX generated successfully")
        print(result.stdout)
    else:
        print(f"⚠️ PPTX conversion had issues")
        print(result.stderr)

    # Step 7: Generate presentation script (NEW!)
    print("\n🎬 Step 7: Generating presentation script...")
    script_path = Path("outputs/scripts/Human-In-the-Loop_PresentationScript.md")
    script_path.parent.mkdir(parents=True, exist_ok=True)

    script = generate_presentation_script(presentation)
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)

    print(f"✓ Presentation script saved to {script_path}")

    # Summary
    print("\n" + "=" * 70)
    print("✅ PhD Research Meeting Pipeline V2 Complete!")
    print("=" * 70)

    print(f"\n📊 Enhanced Features:")
    print(f"  ✓ Figure extraction: {len(figures)} figures")
    print(f"  ✓ Result interpretations: Included")
    print(f"  ✓ Related work comparisons: Included")
    print(f"  ✓ Discussion depth: Included")
    print(f"  ✓ Presentation script: Generated")

    print(f"\n💰 Total Cost: ${analyzer_v2.total_cost:.4f}")

    print(f"\n📁 Output Files:")
    print(f"  - {output_path}")
    print(f"  - outputs/slides/Human-In-the-Loop_PhD_Meeting_V2.pptx")
    print(f"  - {script_path}")

    if figures:
        print(f"\n🖼️  Extracted Figures:")
        for i, fig in enumerate(figures, 1):
            print(f"  {i}. {Path(fig['image_path']).name}")
            print(f"     Caption: {fig['caption'][:80]}...")


def generate_presentation_script(presentation) -> str:
    """Generate presentation speaking script"""

    lines = [
        "# Presentation Script",
        "",
        f"Total Slides: {presentation.total_slides}",
        f"Suggested Duration: 10-15 minutes",
        "",
        "---",
        ""
    ]

    for i, slide in enumerate(presentation.slides, 1):
        lines.append(f"## Slide {i}: {slide.title}")
        lines.append("")
        lines.append(f"**Type**: {slide.slide_type}")
        lines.append(f"**Word Count**: {slide.word_count} words")
        if slide.has_figure:
            lines.append(f"**Has Figure**: Yes - {slide.figure_caption[:50]}...")
        lines.append("")
        lines.append("**Speaker Notes:**")
        lines.append(f"{slide.notes}")
        lines.append("")
        lines.append("**Talking Points:**")
        for bullet in slide.bullet_points:
            if bullet.strip():
                lines.append(f"- {bullet}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    test_phd_meeting_pipeline_v2()
