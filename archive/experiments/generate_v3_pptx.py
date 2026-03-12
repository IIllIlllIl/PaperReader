#!/usr/bin/env python3
"""
Generate V3 PPTX Presentation

Uses V3 modules to create slides with:
- English only
- Max 30 words per slide
- Keywords
- Tables
- Figures from PDF
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_parser import PDFParser
from src.ai_analyzer_enhanced import EnhancedAIAnalyzer
from src.content_extractor_enhanced_v3 import EnhancedContentExtractorV3
from src.ppt_generator_enhanced_v3 import EnhancedPPTGeneratorV3
from src.pdf_image_extractor import PDFImageExtractor
from src.utils import load_config, get_api_key, ensure_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_v3_pptx.py <paper.pdf>")
        sys.exit(1)
    
    paper_path = sys.argv[1]
    paper_name = Path(paper_path).stem
    
    print(f"\n{'='*60}")
    print(f"🚀 PaperReader - V3 PPTX Generator")
    print(f"{'='*60}\n")
    print(f"📄 Paper: {paper_name}\n")
    
    # Load config
    config = load_config()
    api_key = get_api_key(config)
    
    # Step 1: Parse PDF
    print("📖 Step 1: Parsing PDF...")
    parser = PDFParser(paper_path)
    paper_text = parser.extract_text()
    metadata = parser.extract_metadata()
    print(f"   ✅ Extracted {len(paper_text)} characters")
    print(f"   📊 Title: {metadata.title}")
    print()
    
    # Step 2: Extract Figures
    print("🖼️  Step 2: Extracting Figures...")
    image_extractor = PDFImageExtractor(output_dir="output/images")
    figures = image_extractor.extract_and_save(paper_path, max_figures=5)
    print(f"   ✅ Extracted {len(figures)} key figures")
    for fig in figures:
        print(f"      - Figure {fig['figure_num']}: {fig['width']}x{fig['height']}")
    print()
    
    # Step 3: AI Analysis (V3)
    print("🤖 Step 3: AI Analysis (V3)...")
    analyzer = EnhancedAIAnalyzer(api_key=api_key)
    
    # TODO: Use V3 prompt from src/prompts/v3_prompt.py
    # For now, use existing analyzer
    analysis = analyzer.analyze_paper_detailed(paper_text, metadata.__dict__)
    stats = analyzer.get_stats()
    print(f"   ✅ Analysis completed")
    print(f"   💰 Cost: ${stats['total_cost']:.4f}")
    print()
    
    # Step 4: Extract Content (V3)
    print("📋 Step 4: Extracting Slide Content (V3)...")
    extractor = EnhancedContentExtractorV3()
    presentation = extractor.extract_detailed_slides(analysis)
    
    # Add figures if available
    if figures:
        extractor.add_figures_to_slides(presentation.slides, figures)
    
    print(f"   ✅ Created {presentation.total_slides} slides")
    print()
    
    # Step 5: Generate Markdown (V3)
    print("📝 Step 5: Generating V3 Markdown...")
    generator = EnhancedPPTGeneratorV3()
    markdown = generator.generate_markdown(presentation)
    
    # Save Markdown
    markdown_dir = ensure_dir(Path(config['presentation']['output_dir']) / 'markdown')
    markdown_path = markdown_dir / f"{paper_name}_v3.md"
    generator.save_presentation(markdown, str(markdown_path))
    print(f"   ✅ Saved Markdown: {markdown_path}")
    print()
    
    # Step 6: Convert to PPTX
    print("📊 Step 6: Converting to PPTX...")
    import subprocess
    
    slides_dir = ensure_dir(Path(config['presentation']['output_dir']) / 'slides')
    pptx_path = slides_dir / f"{paper_name}_v3.pptx"
    
    result = subprocess.run(
        ['python3', 'tools/md_to_pptx.py', str(markdown_path), str(pptx_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"   ✅ Saved PPTX: {pptx_path}")
    else:
        print(f"   ❌ Conversion failed: {result.stderr}")
    print()
    
    # Summary
    print(f"{'='*60}")
    print(f"✨ V3 Generation Complete!")
    print(f"{'='*60}")
    print(f"📄 Paper: {paper_name}")
    print(f"📊 Total slides: {presentation.total_slides}")
    print(f"🖼️  Figures: {len(figures)}")
    print(f"💰 Total cost: ${stats['total_cost']:.4f}")
    print(f"📝 Markdown: {markdown_path}")
    print(f"📊 PPTX: {pptx_path}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
