"""
PaperReader - Academic Paper Reading and Presentation Generation Tool

This package provides tools for:
- PDF paper parsing and analysis
- AI-powered content extraction
- Academic presentation generation

Architecture (V3):
- parser: PDF processing modules
- analysis: AI analysis and content extraction
- generation: Presentation generation
- core: Infrastructure (cache, resilience, progress)
"""

__version__ = "0.3.0"
__author__ = "PaperReader Team"

# Parser modules
from .parser.pdf_parser import PDFParser

# Analysis modules
from .analysis.ai_analyzer import AIAnalyzer
from .analysis.content_extractor import ContentExtractor

# Generation modules
from .generation.ppt_generator import PPTGenerator

# Core modules
from .core.cache_manager import CacheManager

__all__ = [
    "PDFParser",
    "AIAnalyzer",
    "ContentExtractor",
    "PPTGenerator",
    "CacheManager",
]
