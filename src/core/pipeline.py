#!/usr/bin/env python3
"""
Paper Presentation Pipeline

Orchestrates the complete end-to-end flow from PDF to PhD meeting presentation.

Pipeline stages:
1. Parse PDF
2. Extract structured sections
3. Run AI analysis
4. Generate slide plan
5. Generate narrative plan
6. Generate slides markdown
7. Export PPTX
8. Generate presentation script
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict

from src.parser.pdf_parser import PDFParser
from src.parser.pdf_image_extractor import PDFImageExtractor
from src.analysis.ai_analyzer import AIAnalyzer, PaperAnalysis
from src.analysis.content_extractor import ContentExtractor, OrganizedPresentation
from src.analysis.citation_integration import CitationIntegrator
from src.config.citation_config import CitationConfig
from src.planning.slide_planner import SlidePlanner
from src.planning.narrative_planner import NarrativePlanner
from src.planning.models import SlidePlan, PresentationNarrative
from src.generation.ppt_generator import PPTGenerator
from src.generation.pptx_exporter import markdown_to_pptx
from src.utils import ensure_dir, format_time

logger = logging.getLogger(__name__)


class PaperPresentationPipeline:
    """
    End-to-end pipeline for generating PhD meeting presentations from papers

    Usage:
        pipeline = PaperPresentationPipeline(api_key=api_key, config=config)
        result = pipeline.run(pdf_path="papers/example.pdf")
    """

    def __init__(self, api_key: str, config: Dict[str, Any], model: str = "claude-sonnet-4-6",
                 clean_intermediates: bool = True):
        """
        Initialize pipeline

        Args:
            api_key: Anthropic API key
            config: Configuration dictionary
            model: AI model to use
            clean_intermediates: Whether to clean intermediate files after pipeline completes (default: True)
        """
        self.api_key = api_key
        self.config = config
        self.model = model
        self.output_dir = "outputs"
        self.pdf_path = ""
        self.clean_intermediates = clean_intermediates

        # Initialize components
        self.ai_analyzer = AIAnalyzer(api_key=api_key, model=model)
        self.slide_planner = SlidePlanner(api_key=api_key, model=model)
        self.narrative_planner = NarrativePlanner(api_key=api_key, model=model)
        self.content_extractor = ContentExtractor()
        self.ppt_generator = PPTGenerator()
        self.image_extractor = None

        # Statistics
        self.stats = {
            'total_time': 0,
            'ai_cost': 0.0,
            'total_tokens': 0,
        }

    def run(self, pdf_path: str, output_dir: Optional[str] = None,
            citation_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete pipeline

        Args:
            pdf_path: Path to PDF file
            output_dir: Output directory (default: outputs/)
            citation_config: Citation analysis configuration (optional)

        Returns:
            Dictionary with paths to generated files and statistics
        """
        start_time = time.time()
        paper_name = Path(pdf_path).stem
        self.pdf_path = pdf_path

        logger.info(f"\n{'='*70}")
        logger.info(f"Pipeline Configuration:")
        logger.info(f"  Paper: {paper_name}")
        logger.info(f"  Clean intermediates: {self.clean_intermediates}")
        logger.info(f"{'='*70}\n")

        # Setup output directories
        if output_dir is None:
            output_dir = "outputs"
        self.output_dir = output_dir

        # Organized output paths
        # Final artifacts (kept)
        # Intermediate artifacts (moved to intermediates/)
        output_paths = {
            'markdown': Path(output_dir) / 'intermediates' / 'markdown' / f"{paper_name}.md",
            'pptx': Path(output_dir) / 'slides' / f"{paper_name}.pptx",
            'script': Path(output_dir) / 'intermediates' / 'scripts' / f"{paper_name}_presentation_script.md",
            'plan': Path(output_dir) / 'intermediates' / 'plans' / f"{paper_name}_plan.json",
        }

        # Ensure all output directories exist
        for path in output_paths.values():
            ensure_dir(path.parent)

        logger.info(f"\n{'='*70}")
        logger.info(f"PIPELINE: {paper_name}")
        logger.info(f"{'='*70}\n")

        try:
            # ------------------------------------------------
            # Stage 1: Parse PDF
            # ------------------------------------------------
            print(f"[1/8] Parsing PDF...")
            paper_text, metadata = self._parse_pdf(pdf_path)
            print(f"      ✓ Extracted {len(paper_text)} characters from {metadata.get('page_count', 'unknown')} pages")

            # ------------------------------------------------
            # Stage 2: Extract structured sections
            # ------------------------------------------------
            print(f"[2/8] Extracting structured sections...")
            sections = self._extract_sections(pdf_path)
            print(f"      ✓ Found {len(sections)} sections: {', '.join(sections.keys())}")

            # ------------------------------------------------
            # Stage 3: Run AI analysis
            # ------------------------------------------------
            print(f"[3/8] Running AI analysis...")
            analysis = self._run_ai_analysis(paper_text, metadata)
            print(f"      ✓ Analysis completed (cost: ${self.ai_analyzer.total_cost:.4f})")

            # ------------------------------------------------
            # Stage 3.5: Citation analysis (optional)
            # ------------------------------------------------
            citation_result = None
            if citation_config and citation_config.get('enabled'):
                print(f"[3.5/8] Analyzing citations...")
                citation_result = self._analyze_citations(
                    metadata,
                    min_sources=citation_config.get('min_sources', 2),
                    display_limit=citation_config.get('display_citations', 20)
                )
                if citation_result:
                    print(f"      ✓ Found {citation_result.get('total_citations', 0)} verified citations")
                else:
                    print(f"      ⚠ No citations found (citation analysis skipped)")

            # ------------------------------------------------
            # Stage 4: Generate slide plan
            # ------------------------------------------------
            print(f"[4/8] Planning slides...")
            slide_plan = self._plan_slides(analysis)
            print(f"      ✓ Generated plan with {slide_plan.total_slides} slides")

            # Save slide plan
            self._save_json(slide_plan.to_dict(), output_paths['plan'])

            # ------------------------------------------------
            # Stage 5: Generate narrative
            # ------------------------------------------------
            print(f"[5/8] Planning narrative...")
            narrative = self._plan_narrative(analysis)
            print(f"      ✓ Narrative extracted: {narrative.key_idea[:60]}...")

            # ------------------------------------------------
            # Extract figures
            # ------------------------------------------------
            image_output_dir = Path(self.output_dir) / "intermediates" / "images"
            image_output_dir.mkdir(parents=True, exist_ok=True)
            self.image_extractor = PDFImageExtractor(str(image_output_dir))
            figures = self.image_extractor.extract_and_save(self.pdf_path)
            logger.info(f"Extracted {len(figures)} figures")

            # ------------------------------------------------
            # Stage 6: Generate slides markdown
            # ------------------------------------------------
            print(f"[6/8] Generating slides...")
            organized_presentation = self._generate_slides(
                analysis, slide_plan, figures=figures, citation_data=citation_result
            )

            # Validate: Ensure all planned slides are generated
            self._validate_slide_generation(slide_plan, organized_presentation)

            markdown = self.ppt_generator.generate_markdown(organized_presentation)
            self.ppt_generator.save_presentation(markdown, str(output_paths['markdown']))
            print(f"      ✓ Generated {organized_presentation.total_slides} slides")
            print(f"      ✓ Markdown saved: {output_paths['markdown']}")

            # ------------------------------------------------
            # Stage 7: Export PPTX
            # ------------------------------------------------
            print(f"[7/8] Exporting PPTX...")
            self._export_pptx(output_paths['markdown'], output_paths['pptx'])
            print(f"      ✓ PPTX saved: {output_paths['pptx']}")

            # ------------------------------------------------
            # Stage 8: Generate presentation script
            # ------------------------------------------------
            print(f"[8/8] Generating presentation script...")
            self._generate_script(narrative, slide_plan, output_paths['script'])
            print(f"      ✓ Script saved: {output_paths['script']}")

            # Calculate statistics
            elapsed_time = time.time() - start_time
            self.stats['total_time'] = format_time(elapsed_time)
            self.stats['ai_cost'] = (
                self.ai_analyzer.total_cost +
                self.slide_planner.total_cost +
                self.narrative_planner.total_cost
            )
            self.stats['total_tokens'] = (
                self.ai_analyzer.total_tokens +
                self.slide_planner.total_tokens +
                self.narrative_planner.total_tokens
            )

            # Print summary
            print(f"\n{'='*70}")
            print(f"PIPELINE COMPLETED SUCCESSFULLY")
            print(f"{'='*70}")
            print(f"\n📊 Statistics:")
            print(f"   Total time: {self.stats['total_time']}")
            print(f"   Total cost: ${self.stats['ai_cost']:.4f}")
            print(f"   Total tokens: {self.stats['total_tokens']:,}")
            print(f"\n📁 Generated files:")
            print(f"   Markdown: {output_paths['markdown']}")
            print(f"   PPTX:     {output_paths['pptx']}")
            print(f"   Script:   {output_paths['script']}")
            print(f"   Plan:     {output_paths['plan']}")
            print(f"{'='*70}\n")

            # Clean intermediate files if requested
            self._clean_intermediate_files()

            return {
                'success': True,
                'output_paths': {k: str(v) for k, v in output_paths.items()},
                'stats': self.stats,
                'analysis': analysis,
                'slide_plan': slide_plan,
                'narrative': narrative,
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            print(f"\n❌ Pipeline failed: {e}")

            # Keep intermediate files on failure for debugging
            if self.clean_intermediates:
                logger.info("Preserving intermediate files for debugging (pipeline failed)")
                print(f"ℹ️  Intermediate files preserved in outputs/intermediates/ for debugging")

            return {
                'success': False,
                'error': str(e),
                'output_paths': {},
                'stats': self.stats,
            }

    # ------------------------------------------------
    # Stage implementations
    # ------------------------------------------------

    def _parse_pdf(self, pdf_path: str) -> tuple:
        """Stage 1: Parse PDF and extract text"""
        parser = PDFParser(pdf_path)

        # Extract text
        paper_text = parser.extract_text()

        # Extract metadata
        metadata_obj = parser.extract_metadata()
        metadata = {
            'title': metadata_obj.title,
            'authors': metadata_obj.authors,
            'year': metadata_obj.year,
            'abstract': metadata_obj.abstract,
            'page_count': parser.get_page_count(),
        }

        return paper_text, metadata

    def _extract_sections(self, pdf_path: str) -> Dict[str, str]:
        """Stage 2: Extract structured sections from PDF"""
        parser = PDFParser(pdf_path)
        sections = parser.extract_sections()
        return sections

    def _run_ai_analysis(self, paper_text: str, metadata: Dict) -> PaperAnalysis:
        """Stage 3: Run AI analysis on paper"""
        analysis = self.ai_analyzer.analyze_paper_detailed(paper_text, metadata)
        return analysis

    def _plan_slides(self, analysis: PaperAnalysis) -> SlidePlan:
        """Stage 4: Generate slide plan from analysis"""
        slide_plan = self.slide_planner.plan_slides(analysis)
        return slide_plan

    def _plan_narrative(self, analysis: PaperAnalysis) -> PresentationNarrative:
        """Stage 5: Extract research narrative from analysis"""
        narrative = self.narrative_planner.extract_narrative(analysis)
        return narrative

    def _analyze_citations(self, metadata: Dict, min_sources: int = 2,
                          display_limit: int = 20) -> Optional[Dict]:
        """Stage 3.5: Analyze paper citations (optional)"""
        try:
            # Create citation config
            citation_cfg = CitationConfig.default()
            citation_cfg.min_sources = min_sources
            citation_cfg.display_citations = display_limit

            # Initialize integrator
            integrator = CitationIntegrator(config=citation_cfg)

            # Extract metadata
            paper_title = metadata.get('title', '')
            authors = ', '.join(metadata.get('authors', []))
            year = metadata.get('year')

            # Run analysis
            result = integrator.analyze_paper_citations(
                paper_title=paper_title,
                authors=authors,
                year=year
            )

            if result and result.get('total_citations', 0) > 0:
                logger.info(f"Citation analysis successful: {result['total_citations']} citations")
                return result
            else:
                logger.info("No citations found or analysis failed")
                return None

        except Exception as e:
            logger.warning(f"Citation analysis failed (non-critical): {e}")
            return None

    def _generate_slides(self, analysis: PaperAnalysis, slide_plan: SlidePlan,
                        figures=None, citation_data=None) -> OrganizedPresentation:
        """Stage 6: Generate organized presentation slides from slide plan"""
        organized_presentation = self.content_extractor.extract_detailed_slides(
            analysis, slide_plan=slide_plan, figures=figures, citation_data=citation_data
        )
        return organized_presentation

    def _export_pptx(self, markdown_path: Path, output_path: Path) -> None:
        """Stage 7: Export Markdown to PPTX"""
        paper_name = output_path.stem
        markdown_to_pptx(str(markdown_path), str(output_path), title=paper_name)

    def _generate_script(self, narrative: PresentationNarrative,
                         slide_plan: SlidePlan,
                         output_path: Path) -> None:
        """Stage 8: Generate presentation script from narrative and plan"""
        script_lines = []

        # Title
        script_lines.append(f"# Presentation Script")
        script_lines.append(f"\n---\n")

        # Narrative overview
        script_lines.append(f"## Research Narrative\n")
        script_lines.append(f"**Hook:** {narrative.hook}\n")
        script_lines.append(f"**Problem:** {narrative.problem}\n")
        script_lines.append(f"**Key Idea:** {narrative.key_idea}\n")
        script_lines.append(f"**Evidence:** {narrative.evidence}\n")
        script_lines.append(f"**Implications:** {narrative.implications}\n")
        script_lines.append(f"\n---\n")

        # Slide-by-slide notes
        script_lines.append(f"## Slide-by-Slide Notes\n")
        for i, slide in enumerate(slide_plan.slides, 1):
            script_lines.append(f"### Slide {i}: {slide.title}\n")
            if slide.notes:
                script_lines.append(f"**Purpose:** {slide.notes}\n")
            if slide.key_points:
                script_lines.append(f"**Key Points:**")
                for point in slide.key_points:
                    script_lines.append(f"- {point}")
            script_lines.append(f"")

        # Join and save
        script_content = "\n".join(script_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

    def _validate_slide_generation(self, slide_plan: SlidePlan, organized_presentation: OrganizedPresentation) -> None:
        """Validate that all planned slides were generated"""
        planned_count = slide_plan.total_slides
        generated_count = organized_presentation.total_slides

        if generated_count < planned_count:
            logger.warning(f"Slide count mismatch: planned {planned_count}, generated {generated_count}")

            # Log which slides are missing
            generated_titles = {slide.title.lower() for slide in organized_presentation.slides}
            for planned_slide in slide_plan.slides:
                if planned_slide.title.lower() not in generated_titles:
                    logger.warning(f"  Missing slide: {planned_slide.title}")
        elif generated_count == planned_count:
            logger.info(f"✓ Slide count validation passed: {generated_count} slides generated as planned")
        else:
            logger.info(f"✓ Generated {generated_count} slides (planned: {planned_count})")

    def _save_json(self, data: Dict, output_path: Path) -> None:
        """Helper: Save data as JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return self.stats

    def _clean_intermediate_files(self):
        """
        Clean intermediate files after pipeline completes successfully.

        This method removes the entire outputs/intermediates/ directory,
        taking advantage of the new centralized structure for simplicity and safety.
        """
        if not self.clean_intermediates:
            logger.info("Preserving intermediate files (--no-clean mode)")
            print(f"\n💾 Intermediate files preserved in outputs/intermediates/")
            return

        logger.info("Cleaning intermediate files...")
        print(f"\n🧹 Cleaning intermediate files...")

        try:
            import shutil

            intermediates_dir = Path(self.output_dir) / "intermediates"

            if not intermediates_dir.exists():
                logger.info("No intermediates directory to clean")
                print(f"   ✓ No intermediates directory found")
                return

            # Calculate statistics before deletion
            total_size = 0
            file_count = 0
            for f in intermediates_dir.glob('**/*'):
                if f.is_file():
                    total_size += f.stat().st_size
                    file_count += 1

            if file_count == 0:
                logger.info("Intermediates directory is empty, nothing to clean")
                print(f"   ✓ Intermediates directory already empty")
                return

            # Log what we're about to delete
            size_kb = total_size / 1024
            logger.info(f"Found {file_count} intermediate files ({size_kb:.2f} KB)")
            print(f"   • {file_count} files ({size_kb:.2f} KB)")

            # Delete entire intermediates directory
            shutil.rmtree(intermediates_dir)
            logger.info(f"Removed intermediates directory: {intermediates_dir}")
            print(f"   ✓ Deleted: {intermediates_dir}")

            # Recreate empty directory structure for next run
            self._create_intermediates_structure()
            logger.info("Recreated empty intermediates directory structure")
            print(f"   ✓ Recreated empty directory structure")

            logger.info(f"Cleaned {file_count} intermediate files ({size_kb:.2f} KB)")
            print(f"   ✅ Cleaned {file_count} intermediate files\n")

        except Exception as e:
            logger.error(f"Failed to clean intermediate files: {e}")
            print(f"   ⚠️  Warning: Failed to clean intermediate files: {e}")

    def _create_intermediates_structure(self):
        """Create empty intermediates directory structure"""
        intermediates_dir = Path(self.output_dir) / "intermediates"

        # Create all intermediate subdirectories
        subdirs = ['images', 'images/citations', 'markdown', 'scripts', 'plans', 'citations', 'temp']

        for subdir in subdirs:
            (intermediates_dir / subdir).mkdir(parents=True, exist_ok=True)
