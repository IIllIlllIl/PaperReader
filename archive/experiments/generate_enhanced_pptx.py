#!/usr/bin/env python3
"""
Generate Enhanced PPTX Presentation

Uses the enhanced analyzer and content extractor to create detailed slides
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_parser import PDFParser
from src.ai_analyzer_enhanced import EnhancedAIAnalyzer
from src.content_extractor_enhanced import EnhancedContentExtractor
from src.ppt_generator_enhanced import EnhancedPPTGenerator
from src.utils import load_config, get_api_key, ensure_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_enhanced_pptx.py <paper.pdf>")
        sys.exit(1)
    
    paper_path = sys.argv[1]
    paper_name = Path(paper_path).stem
    
    print(f"\n{'='*60}")
    print(f"🚀 PaperReader - Enhanced PPTX Generator")
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
    
    # Step 2: AI Analysis (Enhanced)
    print("🤖 Step 2: AI Analysis (Enhanced - This may take a minute)...")
    analyzer = EnhancedAIAnalyzer(api_key=api_key)
    analysis = analyzer.analyze_paper_detailed(paper_text, metadata.__dict__)
    stats = analyzer.get_stats()
    print(f"   ✅ Analysis completed")
    print(f"   💰 Cost: ${stats['total_cost']:.4f}")
    print()
    
    # Step 3: Extract Content (Enhanced)
    print("📋 Step 3: Extracting Slide Content (Enhanced)...")
    extractor = EnhancedContentExtractor()
    presentation = extractor.extract_detailed_slides(analysis)
    print(f"   ✅ Created {presentation.total_slides} slides")
    print()
    
    # Step 4: Generate Markdown
    print("📝 Step 4: Generating Enhanced Markdown...")
    generator = EnhancedPPTGenerator()
    markdown = generator.generate_markdown(presentation)
    
    # Save Markdown
    markdown_dir = ensure_dir(Path(config['presentation']['output_dir']) / 'markdown')
    markdown_path = markdown_dir / f"{paper_name}_enhanced.md"
    generator.save_presentation(markdown, str(markdown_path))
    print(f"   ✅ Saved Markdown: {markdown_path}")
    print()
    
    # Step 5: Convert to PPTX
    print("📊 Step 5: Converting to PPTX...")
    import subprocess
    
    slides_dir = ensure_dir(Path(config['presentation']['output_dir']) / 'slides')
    pptx_path = slides_dir / f"{paper_name}_enhanced.pptx"
    
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
    print(f"✨ Generation Complete!")
    print(f"{'='*60}")
    print(f"📄 Paper: {paper_name}")
    print(f"📊 Total slides: {presentation.total_slides}")
    print(f"💰 Total cost: ${stats['total_cost']:.4f}")
    print(f"📝 Markdown: {markdown_path}")
    print(f"📊 PPTX: {pptx_path}")
    print(f"{'='*60}\n")
    
    # Show slide outline
    print(f"📑 Slide Outline:")
    print(f"{'-'*60}")
    for i, slide in enumerate(presentation.slides[:10], 1):  # Show first 10 slides
        emoji = "📖" if i == 1 else "🎬" if i == 2 else "📝"
        print(f"{emoji}  {i:2d}. {slide.title}")
    if presentation.total_slides > 10:
        print(f"    ... and {presentation.total_slides - 10} more slides")
    print(f"{'-'*60}\n")

if __name__ == '__main__':
    main()
