#!/usr/bin/env python3
"""
PaperReader - Academic Paper Reading and Presentation Generation Tool

Main entry point for processing papers and generating presentations
"""

import sys
import time
from pathlib import Path
from typing import Optional, List
import click

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    load_config, setup_logging, get_file_hash, ensure_dir,
    get_api_key, scan_papers, format_time
)
from src.parser.pdf_parser import PDFParser
from src.parser.pdf_validator import PDFQuality
from src.analysis.ai_analyzer import AIAnalyzer
from src.analysis.content_extractor import ContentExtractor
from src.generation.ppt_generator import PPTGenerator
from src.core.cache_manager import CacheManager
from src.core.resilience import ResilientAIAnalyzer, RetryConfig
from src.core.progress_reporter import get_reporter

# Import enhanced modules
try:
    from src.analysis.ai_analyzer import EnhancedAIAnalyzer
    from src.analysis.content_extractor import EnhancedContentExtractor
    from src.generation.ppt_generator import EnhancedPPTGenerator
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False


@click.group()
@click.version_option(version='0.2.0')
def cli():
    """PaperReader - Generate presentations from academic papers"""
    pass


@cli.command()
@click.option('--paper', '-p', type=click.Path(exists=True), help='Path to a single PDF paper')
@click.option('--all', 'process_all', is_flag=True, help='Process all papers in the papers directory')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'pdf']), default='html',
              help='Output format (default: html)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output with progress details')
@click.option('--no-cache', is_flag=True, help='Disable cache')
@click.option('--config', type=click.Path(exists=True), default='config.yaml', help='Path to config file')
def process(paper: Optional[str], process_all: bool, format: str, verbose: bool,
           no_cache: bool, config: str):
    """Process paper(s) and generate presentation(s)"""
    
    # Load configuration
    cfg = load_config(config)
    
    # Setup logging
    logger = setup_logging(cfg)
    
    # Setup progress reporter
    reporter = get_reporter(verbose)
    
    # Get API key
    try:
        api_key = get_api_key(cfg)
    except ValueError as e:
        reporter.error(str(e))
        sys.exit(1)
    
    # Initialize components
    cache_manager = CacheManager(
        cache_dir=cfg['cache']['cache_dir'],
        ttl=cfg['cache']['ttl']
    )
    
    if no_cache:
        cache_manager.disable()
    
    ai_analyzer = AIAnalyzer(
        api_key=api_key,
        model=cfg['ai']['model'],
        haiku_model=cfg['ai']['haiku_model']
    )
    
    resilient_analyzer = ResilientAIAnalyzer(
        analyzer=ai_analyzer,
        config=RetryConfig(max_retries=cfg['ai']['max_retries'])
    )
    
    content_extractor = ContentExtractor()
    ppt_generator = PPTGenerator(template_path=cfg['presentation']['template'])
    
    # Determine which papers to process
    if process_all:
        try:
            papers = scan_papers(cfg['paper']['input_dir'])
        except FileNotFoundError as e:
            reporter.error(str(e))
            sys.exit(1)
    elif paper:
        papers = [paper]
    else:
        reporter.error("Please specify --paper or --all")
        sys.exit(1)
    
    if not papers:
        reporter.warning("No papers found to process")
        sys.exit(0)
    
    # Process papers
    stats = {
        'papers_processed': 0,
        'papers_failed': 0,
        'cache_hits': 0,
        'total_time': 0,
        'estimated_cost': 0.0,
    }
    
    start_time = time.time()
    
    reporter.show_panel(
        "PaperReader",
        f"Papers to process: {len(papers)}\nOutput format: {format}\nCache: {'disabled' if no_cache else 'enabled'}"
    )
    
    for i, paper_path in enumerate(papers, 1):
        reporter.info(f"\n[{i}/{len(papers)}] Processing: {Path(paper_path).name}")
        
        try:
            success = process_single_paper(
                paper_path=paper_path,
                cfg=cfg,
                cache_manager=cache_manager,
                analyzer=resilient_analyzer,
                raw_analyzer=ai_analyzer,
                content_extractor=content_extractor,
                ppt_generator=ppt_generator,
                output_format=format,
                reporter=reporter
            )
            
            if success:
                stats['papers_processed'] += 1
                stats['cache_hits'] += 1 if cache_manager.enabled else 0
            else:
                stats['papers_failed'] += 1
                
        except Exception as e:
            logger.error(f"Failed to process {paper_path}: {e}")
            reporter.error(f"Failed: {e}")
            stats['papers_failed'] += 1
    
    # Calculate stats
    stats['total_time'] = format_time(time.time() - start_time)
    stats['estimated_cost'] = ai_analyzer.get_stats()['total_cost']
    
    # Show summary
    reporter.show_summary(stats)
    
    if stats['papers_failed'] > 0:
        sys.exit(1)


def process_single_paper(paper_path: str, cfg: dict, cache_manager: CacheManager,
                        analyzer: ResilientAIAnalyzer, raw_analyzer: AIAnalyzer,
                        content_extractor: ContentExtractor, ppt_generator: PPTGenerator,
                        output_format: str, reporter) -> bool:
    """
    Process a single paper
    
    Returns:
        True if successful, False otherwise
    """
    paper_name = Path(paper_path).stem
    
    # Start progress
    reporter.start(total_steps=6, description=f"Processing {paper_name}")
    
    # Step 1: Validate PDF
    reporter.update(description="Validating PDF...")
    parser = PDFParser(paper_path)
    is_valid, validation_msg = parser.validate()
    
    if not is_valid:
        reporter.error(validation_msg)
        reporter.stop(success=False, message="PDF validation failed")
        return False
    
    reporter.success(f"PDF validation: {validation_msg}")
    
    # Step 2: Extract text and metadata
    reporter.update(description="Extracting text...")
    try:
        paper_text = parser.extract_text()
        metadata = parser.extract_metadata()
        reporter.success(f"Extracted {len(paper_text)} characters from {parser.get_page_count()} pages")
    except Exception as e:
        reporter.error(f"Text extraction failed: {e}")
        reporter.stop(success=False, message="Text extraction failed")
        return False
    
    # Step 3: Check cache
    reporter.update(description="Checking cache...")
    pdf_hash = get_file_hash(paper_path)
    cached_analysis = cache_manager.get_cached_analysis(pdf_hash)
    
    if cached_analysis:
        reporter.success("Using cached analysis")
        analysis = AIAnalyzer.api_key.__class__(**cached_analysis['analysis'])
        presentation_content = AIAnalyzer.generate_presentation_content.__func__(AIAnalyzer, analysis, metadata.__dict__)
    else:
        # Step 4: AI Analysis
        reporter.update(description="Analyzing with AI...")
        try:
            analysis = analyzer.analyze_with_retry(paper_text, metadata=metadata.__dict__)
            presentation_content = raw_analyzer.generate_presentation_content(analysis, metadata.__dict__)
            
            # Save to cache
            cache_manager.save_analysis(
                pdf_hash,
                {'analysis': analysis.__dict__, 'presentation_content': presentation_content.__dict__}
            )
            
            reporter.success(f"AI analysis completed (cost: ${raw_analyzer.get_stats()['total_cost']:.4f})")
        except Exception as e:
            reporter.error(f"AI analysis failed: {e}")
            reporter.stop(success=False, message="AI analysis failed")
            return False
    
    # Step 5: Extract slide content
    reporter.update(description="Extracting slide content...")
    organized_presentation = content_extractor.extract_slide_content(analysis, presentation_content)
    reporter.success(f"Organized {organized_presentation.total_slides} slides")
    
    # Step 6: Generate presentation
    reporter.update(description="Generating presentation...")
    try:
        # Generate Markdown
        markdown = ppt_generator.generate_markdown(organized_presentation)
        
        # Save Markdown
        markdown_dir = ensure_dir(Path(cfg['presentation']['output_dir']) / 'markdown')
        markdown_path = markdown_dir / f"{paper_name}.md"
        ppt_generator.save_presentation(markdown, str(markdown_path))
        
        reporter.success(f"Markdown saved: {markdown_path}")
        
        # Convert to final format
        if output_format in ['html', 'pdf']:
            slides_dir = ensure_dir(Path(cfg['presentation']['output_dir']) / 'slides')
            output_path = slides_dir / f"{paper_name}.{output_format}"
            
            if output_format == 'html':
                success = ppt_generator.convert_to_html(str(markdown_path), str(output_path))
            else:
                success = ppt_generator.convert_to_pdf(str(markdown_path), str(output_path))
            
            if success:
                reporter.success(f"{output_format.upper()} saved: {output_path}")
            else:
                # Fallback to standalone HTML
                reporter.warning(f"Marp conversion failed, generating standalone HTML")
                standalone_html = ppt_generator.generate_standalone_html(markdown)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(standalone_html)
                reporter.success(f"Standalone HTML saved: {output_path}")
        
        reporter.stop(success=True, message="Processing completed!")
        return True
    
    except Exception as e:
        reporter.error(f"Presentation generation failed: {e}")
        reporter.stop(success=False, message="Presentation generation failed")
        return False


@cli.command()
def stats():
    """Show cache statistics"""
    cfg = load_config()
    cache_manager = CacheManager(
        cache_dir=cfg['cache']['cache_dir'],
        ttl=cfg['cache']['ttl']
    )
    
    cache_stats = cache_manager.get_cache_stats()
    
    click.echo("Cache Statistics:")
    click.echo(f"  Total files: {cache_stats['total_files']}")
    click.echo(f"  Valid files: {cache_stats['valid_files']}")
    click.echo(f"  Expired files: {cache_stats['expired_files']}")
    click.echo(f"  Total size: {cache_stats['total_size_mb']:.2f} MB")


@cli.command()
def clear_cache():
    """Clear all cached data"""
    cfg = load_config()
    cache_manager = CacheManager(
        cache_dir=cfg['cache']['cache_dir'],
        ttl=cfg['cache']['ttl']
    )
    
    count = cache_manager.clear_cache()
    click.echo(f"Cleared {count} cache files")


@cli.command()
def cleanup():
    """Clean up expired cache files"""
    cfg = load_config()
    cache_manager = CacheManager(
        cache_dir=cfg['cache']['cache_dir'],
        ttl=cfg['cache']['ttl']
    )
    
    count = cache_manager.cleanup_expired()
    click.echo(f"Removed {count} expired cache files")


if __name__ == '__main__':
    cli()
