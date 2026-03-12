#!/usr/bin/env python3
"""
Generate V3 PPTX Presentation (Optimized)

Optimized version with:
- Better keyword extraction
- More tables (Datasets, Baselines, Metrics)
- Smarter figure selection
- V3 formatting
"""

import sys
import re
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
from src.content_extractor_enhanced_v3 import (
    EnhancedOrganizedPresentationV3, 
    EnhancedSlideContentV3
)

def smart_extract_keywords(text, max_words=6):
    """
    Smart keyword extraction from text
    
    Args:
            text: Input text
            max_words: Maximum words to extract
            
    Returns:
            List of keywords
    """
    if not text:
        return []
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    keywords = []
    for sent in sentences[:max_words]:
        # Remove common words
        sent = re.sub(r'\b(the|a|an|is|are|was|were|been|being|have|has|had|to|of|in|for|on|with|at|by)\b', ' ', sent)
        # Get first N meaningful words
        words = sent.strip().split()[:8]
        if words:
            keyword = ' '.join(words)
            if len(keyword) > 10:  # Min 10 chars
                keywords.append(keyword)
    
    return keywords[:max_words]

def convert_to_v3_format_optimized(analysis):
    """
    Convert old format analysis to V3 keywords format (Optimized)
    """
    from dataclasses import dataclass
    
    @dataclass
    class V3Analysis:
        title: str
        authors: str
        year: str
        research_background_keywords: list
        research_problem_keywords: list
        key_insights: list
        method_keywords: list
        technical_details_keywords: list
        datasets_table: str
        baselines_table: str
        metrics_table: str
        experimental_setup_keywords: list
        main_results_keywords: list
        key_findings_keywords: list
        advantages_keywords: list
        limitations_keywords: list
        future_work_keywords: list
    
    # Convert authors
    authors_str = ', '.join(analysis.authors) if isinstance(analysis.authors, list) else str(analysis.authors)
    
    # Extract keywords from old format
    background_keywords = smart_extract_keywords(analysis.research_background, 5)
    problem_keywords = smart_extract_keywords(analysis.core_problem, 4)
    
    # Format key insights with emoji
    insights = []
    for i, insight in enumerate(analysis.key_insights[:5]):
        if i < 2:  # Mark first 2 as breakthroughs
            insights.append(f"🔥 {insight}")
        else:
            insights.append(f"💡 {insight}")
    
    # Extract method keywords
    method_kw = smart_extract_keywords(analysis.method_overview, 6)
    tech_kw = analysis.technical_innovations[:6] if analysis.technical_innovations else []
    
    # Create tables
    datasets_table = create_datasets_table(analysis.datasets)
    baselines_table = create_baselines_table(analysis.baselines)
    metrics_table = create_metrics_table(analysis.metrics)
    
    # Format main results with bold numbers
    results = []
    for result in analysis.main_results[:6]:
        # Bold all numbers
        result_bold = re.sub(r'(\d+(?:\.\d+)?%)', r'**\1**', result)
        results.append(f"🔥 {result_bold}")
    
    # Extract other keywords
    findings_kw = smart_extract_keywords(analysis.performance_analysis, 4)
    advantages_kw = analysis.advantages[:4] if analysis.advantages else []
    limitations_kw = analysis.limitations[:3] if analysis.limitations else []
    future_kw = analysis.future_work[:3] if analysis.future_work else []
    
    return V3Analysis(
        title=analysis.title,
        authors=authors_str,
        year="2024",
        research_background_keywords=background_keywords,
        research_problem_keywords=problem_keywords,
        key_insights=insights,
        method_keywords=method_kw,
        technical_details_keywords=tech_kw,
        datasets_table=datasets_table,
        baselines_table=baselines_table,
        metrics_table=metrics_table,
        experimental_setup_keywords=smart_extract_keywords(analysis.experimental_setup, 4),
        main_results_keywords=results,
        key_findings_keywords=findings_kw,
        advantages_keywords=advantages_kw,
        limitations_keywords=limitations_kw,
        future_work_keywords=future_kw
    )

def create_datasets_table(datasets):
    """Create Markdown table for datasets"""
    if not datasets:
        return "| Dataset | Size | Description |
|--------|------|-------------|"
    
    table = "| Dataset | Size | Description |\n|--------|------|-------------|\n"
    for i, dataset in enumerate(datasets[:4], 1):
        # Simple extraction
        parts = dataset.split(',')
        name = parts[0].strip() if parts else "Unknown"
        size_desc = ', '.join(parts[1:]).strip() if len(parts) > 1 else "N/A"
        table += f"| {name} | {size_desc} |\n"
    
    return table

def create_baselines_table(baselines):
    """Create Markdown table for baselines"""
    if not baselines:
        return "| Method | Type | Description |
|--------|------|-------------|"
    
    table = "| Method | Type | Description |\n|--------|------|-------------|\n"
    for i, baseline in enumerate(baselines[:4], 1):
        # Simple extraction
        parts = baseline.split(':')
        name = parts[0].strip() if parts else "Unknown"
        desc = ':'.join(parts[1:]).strip() if len(parts) > 1 else "N/A"
        table += f"| {name} | Baseline | {desc} |\n"
    
    return table

def create_metrics_table(metrics):
    """Create Markdown table for metrics"""
    if not metrics:
        return "| Metric | Description |
|--------|-------------|"
    
    table = "| Metric | Description |\n|--------|-------------|\n"
    for i, metric in enumerate(metrics[:4], 1):
        table += f"| {metric} | Evaluation metric |\n"
    
    return table

def create_v3_presentation(analysis_v3, figures):
    """Create V3 presentation from analysis"""
    slides = []
    
    # Slide 1: Title
    slides.append(EnhancedSlideContentV3(
        title=analysis_v3.title,
        bullet_points=[analysis_v3.authors, analysis_v3.year],
        notes="Welcome slide",
        slide_type="title",
        word_count=len(analysis_v3.authors.split()) + 1
    ))
    
    # Slide 2: Outline
    slides.append(EnhancedSlideContentV3(
        title="Outline",
        bullet_points=[
            "Background & Problem",
            "Key Insights",
            "Method & Technical Details",
            "Experiments & Results",
            "Analysis & Discussion"
        ],
        notes="Presentation outline",
        slide_type="section",
        word_count=10
    ))
    
    # Slide 3: Research Background
    if analysis_v3.research_background_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Research Background",
            bullet_points=analysis_v3.research_background_keywords,
            notes="Research background",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.research_background_keywords).split())
        ))
    
    # Slide 4: Research Problem
    if analysis_v3.research_problem_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Research Problem",
            bullet_points=analysis_v3.research_problem_keywords,
            notes="Research problem",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.research_problem_keywords).split())
        ))
    
    # Slide 5: Key Insights
    if analysis_v3.key_insights:
        slides.append(EnhancedSlideContentV3(
            title="Key Insights & Breakthroughs",
            bullet_points=analysis_v3.key_insights,
            notes="Key insights",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.key_insights).split())
        ))
    
    # Slide 6: Method Overview
    if analysis_v3.method_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Method Overview",
            bullet_points=analysis_v3.method_keywords,
            notes="Method overview",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.method_keywords).split())
        ))
    
    # Slide 7: Technical Details
    if analysis_v3.technical_details_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Technical Details",
            bullet_points=analysis_v3.technical_details_keywords,
            notes="Technical details",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.technical_details_keywords).split())
        ))
    
    # Slide 8: Datasets Table
    if analysis_v3.datasets_table:
        slides.append(EnhancedSlideContentV3(
            title="Datasets",
            bullet_points=[analysis_v3.datasets_table],
            notes="Datasets table",
            slide_type="table",
            word_count=15  # Estimate
        ))
    
    # Slide 9: Baselines Table
    if analysis_v3.baselines_table:
        slides.append(EnhancedSlideContentV3(
            title="Baselines",
            bullet_points=[analysis_v3.baselines_table],
            notes="Baselines table",
            slide_type="table",
            word_count=15
        ))
    
    # Slide 10: Metrics Table
    if analysis_v3.metrics_table:
        slides.append(EnhancedSlideContentV3(
            title="Metrics",
            bullet_points=[analysis_v3.metrics_table],
            notes="Metrics table",
            slide_type="table",
            word_count=15
        ))
    
    # Slide 11: Experimental Setup
    if analysis_v3.experimental_setup_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Experimental Setup",
            bullet_points=analysis_v3.experimental_setup_keywords,
            notes="Experimental setup",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.experimental_setup_keywords).split())
        ))
    
    # Slide 12: Main Results
    if analysis_v3.main_results_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Main Results",
            bullet_points=analysis_v3.main_results_keywords,
            notes="Main results",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.main_results_keywords).split())
        ))
    
    # Slide 13: Key Findings
    if analysis_v3.key_findings_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Key Findings",
            bullet_points=analysis_v3.key_findings_keywords,
            notes="Key findings",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.key_findings_keywords).split())
        ))
    
    # Slide 14: Advantages
    if analysis_v3.advantages_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Advantages",
            bullet_points=analysis_v3.advantages_keywords,
            notes="Advantages",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.advantages_keywords).split())
        ))
    
    # Slide 15: Limitations
    if analysis_v3.limitations_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Limitations",
            bullet_points=analysis_v3.limitations_keywords,
            notes="Limitations",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.limitations_keywords).split())
        ))
    
    # Slide 16: Future Work
    if analysis_v3.future_work_keywords:
        slides.append(EnhancedSlideContentV3(
            title="Future Work",
            bullet_points=analysis_v3.future_work_keywords,
            notes="Future work",
            slide_type="content",
            word_count=len(' '.join(analysis_v3.future_work_keywords).split())
        ))
    
    # Add figure slides (max 3)
    for i, fig in enumerate(figures[:3]):
        slides.append(EnhancedSlideContentV3(
            title=f"Figure {i+1}",
            bullet_points=[f"![Figure {i+1}]({fig['image_path']})"],
            notes=f"Figure from page {fig['page_num']}",
            slide_type="figure",
            word_count=5
        ))
    
    # Final slide: Q&A
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
        print("Usage: python tools/generate_v3_pptx_optimized.py <paper.pdf>")
        sys.exit(1)
    
    paper_path = sys.argv[1]
    paper_name = Path(paper_path).stem
    
    print(f"\n{'='*60}")
    print(f"🚀 PaperReader - V3 PPTX Generator (Optimized)")
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
    
    # Step 2: Extract Figures (Optimized)
    print("🖼️  Step 2: Extracting Figures...")
    image_extractor = PDFImageExtractor(output_dir="output/images")
    figures = image_extractor.extract_and_save(paper_path, max_figures=3)  # Only top 3
    print(f"   ✅ Extracted {len(figures)} key figures\n")
    
    # Step 3: AI Analysis
    print("🤖 Step 3: AI Analysis...")
    analyzer = EnhancedAIAnalyzer(api_key=api_key)
    analysis_old = analyzer.analyze_paper_detailed(paper_text, metadata.__dict__)
    stats = analyzer.get_stats()
    print(f"   ✅ Analysis completed")
    print(f"   💰 Cost: ${stats['total_cost']:.4f}\n")
    
    # Step 4: Convert to V3 (Optimized)
    print("🔄 Step 4: Converting to V3 format...")
    analysis_v3 = convert_to_v3_format_optimized(analysis_old)
    print(f"   ✅ Converted to V3 format\n")
    
    # Step 5: Create V3 Presentation
    print("📋 Step 5: Creating V3 Presentation...")
    presentation = create_v3_presentation(analysis_v3, figures)
    print(f"   ✅ Created {presentation.total_slides} slides\n")
    
    # Step 6: Generate Markdown
    print("📝 Step 6: Generating V3 Markdown...")
    generator = EnhancedPPTGeneratorV3()
    markdown = generator.generate_markdown(presentation)
    
    # Save
    markdown_dir = ensure_dir(Path("output/markdown"))
    markdown_path = markdown_dir / f"{paper_name}_v3_optimized.md"
    generator.save_presentation(markdown, str(markdown_path))
    print(f"   ✅ Saved Markdown: {markdown_path}\n")
    
    # Step 7: Convert to PPTX
    print("📊 Step 7: Converting to PPTX...")
    import subprocess
    
    slides_dir = ensure_dir(Path("output/slides"))
    pptx_path = slides_dir / f"{paper_name}_v3_optimized.pptx"
    
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
    print(f"✨ V3 Generation Complete! (Optimized)")
    print(f"{'='*60}")
    print(f"📄 Paper: {paper_name}")
    print(f"📊 Total slides: {presentation.total_slides}")
    print(f"🖼️  Figures: {len(figures)}")
    print(f"📊  Tables: 3 (Datasets, Baselines, Metrics)")
    print(f"💰 Total cost: ${stats['total_cost']:.4f}")
    print(f"📝 Markdown: {markdown_path}")
    print(f"📊 PPTX: {pptx_path}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
