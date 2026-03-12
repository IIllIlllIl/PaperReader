#!/usr/bin/env python3
"""
Generate V3 PPTX Presentation (Simplified)

Quick fix: Uses existing AI analyzer but formats output in V3 style
"""

import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_parser import PDFParser
from src.ai_analyzer_enhanced import EnhancedAIAnalyzer
from src.ppt_generator_enhanced_v3 import EnhancedPPTGeneratorV3
from src.pdf_image_extractor import PDFImageExtractor
from src.utils import load_config, get_api_key, ensure_dir
from src.content_extractor_enhanced_v3 import EnhancedOrganizedPresentationV3, EnhancedSlideContentV3

def convert_to_v3_format(analysis):
    """Convert old format analysis to V3 keywords format"""
    from dataclasses import dataclass
    
    @dataclass
    class SimpleAnalysis:
        title: str
        authors: str
        year: str
        research_background_keywords: list
        research_problem_keywords: list
        key_insights: list
        method_keywords: list
        technical_details_keywords: list
        experimental_setup_keywords: list
        main_results_keywords: list
        key_findings_keywords: list
        advantages_keywords: list
        limitations_keywords: list
        future_work_keywords: list
    
    # Extract keywords from old format
    def extract_keywords(text, max_items=5):
        """Extract keywords from text"""
        if not text:
            return []
        # Split by sentences and take first few words
        sentences = text.split('.')
        keywords = []
        for sent in sentences[:max_items]:
            words = sent.strip().split()[:6]  # First 6 words
            if words:
                keywords.append(' '.join(words))
        return keywords
    
    # Convert
    v3_analysis = SimpleAnalysis(
        title=analysis.title,
        authors=', '.join(analysis.authors) if isinstance(analysis.authors, list) else str(analysis.authors),
        year="2024",
        research_background_keywords=extract_keywords(analysis.research_background, 5),
        research_problem_keywords=extract_keywords(analysis.core_problem, 4),
        key_insights=[f"💡 {i}" for i in analysis.key_insights[:5]],
        method_keywords=extract_keywords(analysis.method_overview, 6),
        technical_details_keywords=analysis.technical_innovations[:6] if analysis.technical_innovations else [],
        experimental_setup_keywords=extract_keywords(analysis.experimental_setup, 4),
        main_results_keywords=[f"🔥 **{r}**" for r in analysis.main_results[:6]],
        key_findings_keywords=extract_keywords(analysis.performance_analysis, 4),
        advantages_keywords=analysis.advantages[:4] if analysis.advantages else [],
        limitations_keywords=analysis.limitations[:3] if analysis.limitations else [],
        future_work_keywords=analysis.future_work[:3] if analysis.future_work else []
    )
    
    return v3_analysis

def create_v3_presentation(analysis, figures=None):
    """Create V3 presentation from analysis"""
    slides = []
    
    # Title slide
    slides.append(EnhancedSlideContentV3(
        title=analysis.title,
        bullet_points=[analysis.authors, analysis.year],
        notes="Welcome slide",
        slide_type="title",
        word_count=3
    ))
    
    # Outline
    slides.append(EnhancedSlideContentV3(
        title="Outline",
        bullet_points=[
            "Background & Problem",
            "Key Insights", 
            "Method & Technical Details",
            "Experiments & Results",
            "Analysis & Discussion",
            "Conclusion & Future Work"
        ],
        notes="Presentation outline",
        slide_type="section",
        word_count=10
    ))
    
    # Background
    if hasattr(analysis, 'research_background_keywords') and analysis.research_background_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Research Background",
            bullet_points=analysis.research_background_keywords[:5],
            notes="Research background",
            slide_type="content",
            word_count=len(' '.join(analysis.research_background_keywords[:5]).split())
        ))
    
    # Problem
    if hasattr(analysis, 'research_problem_keywords') and analysis.research_problem_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Research Problem",
            bullet_points=analysis.research_problem_keywords[:4],
            notes="Research problem",
            slide_type="content",
            word_count=len(' '.join(analysis.research_problem_keywords[:4]).split())
        ))
    
    # Key insights
    if hasattr(analysis, 'key_insights') and analysis.key_insights:
        slides.append(EnhancedSlideContentV3(
            title="Key Insights",
            bullet_points=analysis.key_insights[:5],
            notes="Key insights and breakthroughs",
            slide_type="content",
            word_count=len(' '.join(analysis.key_insights[:5]).split())
        ))
    
    # Method
    if hasattr(analysis, 'method_keywords') and analysis.method_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Method Overview",
            bullet_points=analysis.method_keywords[:6],
            notes="Method overview",
            slide_type="content",
            word_count=len(' '.join(analysis.method_keywords[:6]).split())
        ))
    
    # Technical details
    if hasattr(analysis, 'technical_details_keywords') and analysis.technical_details_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Technical Details",
            bullet_points=analysis.technical_details_keywords[:6],
            notes="Technical details",
            slide_type="content",
            word_count=len(' '.join(analysis.technical_details_keywords[:6]).split())
        ))
    
    # Experimental setup
    if hasattr(analysis, 'experimental_setup_keywords') and analysis.experimental_setup_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Experimental Setup",
            bullet_points=analysis.experimental_setup_keywords[:4],
            notes="Experimental setup",
            slide_type="content",
            word_count=len(' '.join(analysis.experimental_setup_keywords[:4]).split())
        ))
    
    # Main results
    if hasattr(analysis, 'main_results_keywords') and analysis.main_results_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Main Results",
            bullet_points=analysis.main_results_keywords[:6],
            notes="Main results",
            slide_type="content",
            word_count=len(' '.join(analysis.main_results_keywords[:6]).split())
        ))
    
    # Key findings
    if hasattr(analysis, 'key_findings_keywords') and analysis.key_findings_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Key Findings",
            bullet_points=analysis.key_findings_keywords[:4],
            notes="Key findings",
            slide_type="content",
            word_count=len(' '.join(analysis.key_findings_keywords[:4]).split())
        ))
    
    # Advantages
    if hasattr(analysis, 'advantages_keywords') and analysis.advantages_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Advantages",
            bullet_points=analysis.advantages_keywords[:4],
            notes="Advantages",
            slide_type="content",
            word_count=len(' '.join(analysis.advantages_keywords[:4]).split())
        ))
    
    # Limitations
    if hasattr(analysis, 'limitations_keywords') and analysis.limitations_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Limitations",
            bullet_points=analysis.limitations_keywords[:3],
            notes="Limitations",
            slide_type="content",
            word_count=len(' '.join(analysis.limitations_keywords[:3]).split())
        ))
    
    # Future work
    if hasattr(analysis, 'future_work_keywords') and analysis.future_work_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Future Work",
            bullet_points=analysis.future_work_keywords[:3],
            notes="Future work",
            slide_type="content",
            word_count=len(' '.join(analysis.future_work_keywords[:3]).split())
        ))
    
    # Add figures if available
    if figures:
        for i, fig in enumerate(figures[:3]):  # Max 3 figures
            slides.append(EnhancedSlideContentV3(
                title=f"Figure {fig['figure_num']}",
                bullet_points=[f"![Figure {fig['figure_num']}]({fig['image_path']})"],
                notes=f"Figure from page {fig['page_num']}",
                slide_type="figure",
                word_count=5
            ))
    
    # Q&A
    slides.append(EnhancedSlideContentV3(
        title="Q&A",
        bullet_points=["Thank you", "Questions?"],
        notes="Open for questions",
        slide_type="section",
        word_count=2
    ))
    
    return EnhancedOrganizedPresentationV3(
        slides=slides,
        total_slides=len(slides)
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_v3_pptx_simple.py <paper.pdf>")
        sys.exit(1)
    
    paper_path = sys.argv[1]
    paper_name = Path(paper_path).stem
    
    print(f"\n{'='*60}")
    print(f"🚀 PaperReader - V3 PPTX Generator (Simplified)")
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
    print(f"   ✅ Extracted {len(paper_text)} characters\n")
    
    # Step 2: Extract Figures
    print("🖼️  Step 2: Extracting Figures...")
    image_extractor = PDFImageExtractor(output_dir="output/images")
    figures = image_extractor.extract_and_save(paper_path, max_figures=3)
    print(f"   ✅ Extracted {len(figures)} key figures\n")
    
    # Step 3: AI Analysis
    print("🤖 Step 3: AI Analysis...")
    analyzer = EnhancedAIAnalyzer(api_key=api_key)
    analysis_old = analyzer.analyze_paper_detailed(paper_text, metadata.__dict__)
    stats = analyzer.get_stats()
    
    # Convert to V3 format
    analysis_v3 = convert_to_v3_format(analysis_old)
    print(f"   ✅ Analysis completed (converted to V3)")
    print(f"   💰 Cost: ${stats['total_cost']:.4f}\n")
    
    # Step 4: Create V3 Presentation
    print("📋 Step 4: Creating V3 Presentation...")
    presentation = create_v3_presentation(analysis_v3, figures)
    print(f"   ✅ Created {presentation.total_slides} slides\n")
    
    # Step 5: Generate Markdown (V3)
    print("📝 Step 5: Generating V3 Markdown...")
    generator = EnhancedPPTGeneratorV3()
    markdown = generator.generate_markdown(presentation)
    
    # Save
    markdown_dir = ensure_dir(Path("output/markdown"))
    markdown_path = markdown_dir / f"{paper_name}_v3.md"
    generator.save_presentation(markdown, str(markdown_path))
    print(f"   ✅ Saved Markdown: {markdown_path}\n")
    
    # Step 6: Convert to PPTX
    print("📊 Step 6: Converting to PPTX...")
    import subprocess
    
    slides_dir = ensure_dir(Path("output/slides"))
    pptx_path = slides_dir / f"{paper_name}_v3.pptx"
    
    result = subprocess.run(
        ['python3', 'tools/md_to_pptx.py', str(markdown_path), str(pptx_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"   ✅ Saved PPTX: {pptx_path}\n")
    else:
        print(f"   ❌ Conversion failed: {result.stderr}\n")
    
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
