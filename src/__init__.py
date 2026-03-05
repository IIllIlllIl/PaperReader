"""
PaperReader - Academic Paper Reading and Presentation Generation Tool

This package provides tools for:
- PDF paper parsing and analysis
- AI-powered content extraction
- Academic presentation generation
"""

__version__ = "0.1.0"
__author__ = "PaperReader Team"

from .pdf_parser import PDFParser
from .ai_analyzer import AIAnalyzer
from .content_extractor import ContentExtractor
from .ppt_generator import PPTGenerator
from .cache_manager import CacheManager

__all__ = [
    "PDFParser",
    "AIAnalyzer",
    "ContentExtractor",
    "PPTGenerator",
    "CacheManager",
]
