"""
PDF Validator for PaperReader

Validates PDF quality and detects layout type
"""

import fitz  # PyMuPDF
from enum import Enum
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger(__name__)


class LayoutType(Enum):
    """PDF layout types"""
    SINGLE_COLUMN = "single_column"
    MULTI_COLUMN = "multi_column"
    SCANNED = "scanned"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class PDFQuality(Enum):
    """PDF quality levels"""
    EXCELLENT = "excellent"  # Perfect text extraction
    GOOD = "good"            # Minor issues
    FAIR = "fair"            # Some issues, still usable
    POOR = "poor"            # Major issues, may need OCR
    UNSUITABLE = "unsuitable"  # Cannot process


@dataclass
class ValidationResult:
    """Result of PDF validation"""
    is_valid: bool
    quality: PDFQuality
    layout_type: LayoutType
    page_count: int
    has_text: bool
    text_ratio: float  # Ratio of pages with extractable text
    issues: List[str]
    recommendations: List[str]


class PDFValidator:
    """Validates PDF files for processing"""

    def __init__(self, pdf_path: str):
        """
        Initialize PDF validator

        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.doc = None

    def validate(self) -> ValidationResult:
        """
        Perform comprehensive PDF validation

        Returns:
            ValidationResult with quality assessment and recommendations
        """
        try:
            self.doc = fitz.open(self.pdf_path)
            page_count = len(self.doc)

            # Check for extractable text
            has_text, text_ratio = self._check_text_extraction()

            # Detect layout type
            layout_type = self._detect_layout()

            # Assess quality
            quality, issues = self._assess_quality(has_text, text_ratio, layout_type)

            # Generate recommendations
            recommendations = self._generate_recommendations(quality, layout_type, issues)

            is_valid = quality != PDFQuality.UNSUITABLE

            return ValidationResult(
                is_valid=is_valid,
                quality=quality,
                layout_type=layout_type,
                page_count=page_count,
                has_text=has_text,
                text_ratio=text_ratio,
                issues=issues,
                recommendations=recommendations
            )

        except Exception as e:
            logger.error(f"PDF validation failed: {e}")
            return ValidationResult(
                is_valid=False,
                quality=PDFQuality.UNSUITABLE,
                layout_type=LayoutType.UNKNOWN,
                page_count=0,
                has_text=False,
                text_ratio=0.0,
                issues=[f"Failed to open PDF: {str(e)}"],
                recommendations=["Check if file is a valid PDF"]
            )
        finally:
            if self.doc:
                self.doc.close()

    def _check_text_extraction(self) -> tuple[bool, float]:
        """Check if text can be extracted from PDF"""
        if not self.doc:
            return False, 0.0

        pages_with_text = 0
        total_pages = len(self.doc)

        for page in self.doc:
            text = page.get_text()
            if text.strip():  # Non-empty text
                pages_with_text += 1

        has_text = pages_with_text > 0
        text_ratio = pages_with_text / total_pages if total_pages > 0 else 0.0

        return has_text, text_ratio

    def _detect_layout(self) -> LayoutType:
        """Detect PDF layout type"""
        if not self.doc:
            return LayoutType.UNKNOWN

        # Sample a few pages
        sample_pages = min(5, len(self.doc))
        layouts = []

        for i in range(sample_pages):
            page = self.doc[i]
            layout = self._detect_page_layout(page)
            layouts.append(layout)

        # Determine overall layout
        if not layouts:
            return LayoutType.UNKNOWN

        # If all scanned
        if all(l == LayoutType.SCANNED for l in layouts):
            return LayoutType.SCANNED

        # If all single column
        if all(l == LayoutType.SINGLE_COLUMN for l in layouts):
            return LayoutType.SINGLE_COLUMN

        # If all multi-column
        if all(l == LayoutType.MULTI_COLUMN for l in layouts):
            return LayoutType.MULTI_COLUMN

        # Mixed layout
        return LayoutType.MIXED

    def _detect_page_layout(self, page) -> LayoutType:
        """Detect layout type for a single page"""
        text = page.get_text()

        # If very little text, likely scanned
        if len(text.strip()) < 100:
            return LayoutType.SCANNED

        # Check for multi-column layout using text blocks
        blocks = page.get_text("blocks")

        if len(blocks) < 2:
            return LayoutType.SINGLE_COLUMN

        # Analyze x-coordinates of blocks
        x_coords = [b[0] for b in blocks if len(b) >= 4]

        if not x_coords:
            return LayoutType.SINGLE_COLUMN

        # Check for distinct left positions (indicating columns)
        page_width = page.rect.width
        left_positions = [x for x in x_coords if x < page_width * 0.3]
        right_positions = [x for x in x_coords if x > page_width * 0.5]

        if len(left_positions) > 2 and len(right_positions) > 2:
            return LayoutType.MULTI_COLUMN

        return LayoutType.SINGLE_COLUMN

    def _assess_quality(self, has_text: bool, text_ratio: float,
                       layout_type: LayoutType) -> tuple[PDFQuality, List[str]]:
        """Assess overall PDF quality"""
        issues = []

        if not has_text:
            return PDFQuality.UNSUITABLE, ["No extractable text found"]

        if layout_type == LayoutType.SCANNED:
            issues.append("PDF appears to be scanned image")
            return PDFQuality.POOR, issues

        if text_ratio < 0.5:
            issues.append(f"Only {text_ratio*100:.1f}% of pages have extractable text")
            return PDFQuality.POOR, issues

        if layout_type == LayoutType.MULTI_COLUMN:
            issues.append("Multi-column layout may affect text extraction order")

        if text_ratio >= 0.9 and layout_type == LayoutType.SINGLE_COLUMN:
            return PDFQuality.EXCELLENT, issues

        if text_ratio >= 0.8:
            if layout_type == LayoutType.MULTI_COLUMN:
                return PDFQuality.GOOD, issues
            return PDFQuality.EXCELLENT, issues

        if text_ratio >= 0.7:
            return PDFQuality.GOOD, issues

        if text_ratio >= 0.5:
            return PDFQuality.FAIR, issues

        return PDFQuality.POOR, issues

    def _generate_recommendations(self, quality: PDFQuality, layout_type: LayoutType,
                                 issues: List[str]) -> List[str]:
        """Generate processing recommendations"""
        recommendations = []

        if quality == PDFQuality.UNSUITABLE:
            recommendations.append("This PDF cannot be processed in its current form")
            recommendations.append("Consider using OCR tools to convert to text")
            return recommendations

        if quality == PDFQuality.POOR:
            if layout_type == LayoutType.SCANNED:
                recommendations.append("Enable OCR support for scanned PDFs")
            else:
                recommendations.append("Try alternative PDF parsing methods")

        if layout_type == LayoutType.MULTI_COLUMN:
            recommendations.append("Multi-column layout detected - text may need reordering")
            recommendations.append("Consider section-by-section analysis")

        if quality in [PDFQuality.EXCELLENT, PDFQuality.GOOD]:
            recommendations.append("PDF is suitable for standard processing")

        return recommendations
