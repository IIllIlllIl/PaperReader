"""
PDF Parser for PaperReader

Extracts text, metadata, and sections from PDF papers
"""

import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging
from pathlib import Path

from .pdf_validator import PDFValidator, PDFQuality

logger = logging.getLogger(__name__)


@dataclass
class Section:
    """Represents a paper section"""
    title: str
    content: str
    level: int  # 1 for main sections, 2 for subsections, etc.


@dataclass
class PaperMetadata:
    """Paper metadata"""
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    year: Optional[str] = None
    venue: Optional[str] = None
    doi: Optional[str] = None


@dataclass
class Image:
    """Represents an extracted image"""
    page_num: int
    image_index: int
    width: int
    height: int
    data: bytes


class PDFParser:
    """Parses PDF academic papers"""

    # Common section patterns
    SECTION_PATTERNS = {
        'abstract': r'(?i)abstract',
        'introduction': r'(?i)introduction',
        'related_work': r'(?i)related\s+work|literature\s+review',
        'method': r'(?i)method|methodology|approach|framework',
        'experiment': r'(?i)experiment|evaluation|implementation',
        'result': r'(?i)result|finding',
        'discussion': r'(?i)discussion',
        'conclusion': r'(?i)conclusion',
        'reference': r'(?i)reference|bibliography',
        'appendix': r'(?i)appendix',
    }

    def __init__(self, pdf_path: str):
        """
        Initialize PDF parser

        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.doc = None
        self.validator = PDFValidator(pdf_path)

    def extract_text(self, keep_open: bool = False) -> str:
        """
        Extract all text from PDF

        Args:
            keep_open: If True, don't close the document (caller will close it)

        Returns:
            Complete text content of the PDF
        """
        try:
            if not self.doc:
                self.doc = fitz.open(self.pdf_path)
            text_parts = []

            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                text = page.get_text()
                text_parts.append(text)

            full_text = "\n\n".join(text_parts)
            logger.info(f"Extracted {len(full_text)} characters from {len(self.doc)} pages")

            return full_text

        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise
        finally:
            if not keep_open and self.doc:
                self.doc.close()
                self.doc = None

    def extract_sections(self) -> Dict[str, str]:
        """
        Extract paper sections based on common section headers

        Returns:
            Dictionary mapping section names to their content
        """
        full_text = self.extract_text()
        sections = self._identify_sections(full_text)

        logger.info(f"Identified {len(sections)} sections")
        return sections

    def extract_metadata(self) -> PaperMetadata:
        """
        Extract paper metadata (title, authors, etc.)

        Returns:
            PaperMetadata object
        """
        try:
            self.doc = fitz.open(self.pdf_path)
            metadata = PaperMetadata()

            # Extract from PDF metadata
            pdf_metadata = self.doc.metadata
            if pdf_metadata:
                metadata.title = pdf_metadata.get('title')
                if pdf_metadata.get('author'):
                    metadata.authors = [a.strip() for a in pdf_metadata.get('author').split(',')]

            # Try to extract from first page if not in metadata
            first_page_text = None
            if not metadata.title or not metadata.authors:
                first_page_text = self.doc[0].get_text()
                if not metadata.title:
                    metadata.title = self._extract_title(first_page_text)
                if not metadata.authors:
                    metadata.authors = self._extract_authors(first_page_text)

            # Extract abstract - use keep_open to prevent document from closing
            full_text = self.extract_text(keep_open=True)
            metadata.abstract = self._extract_abstract(full_text)

            # Extract year
            metadata.year = self._extract_year(pdf_metadata)

            logger.info(f"Extracted metadata: title={metadata.title}, authors={len(metadata.authors)}")
            return metadata

        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            return PaperMetadata()
        finally:
            if self.doc:
                self.doc.close()
                self.doc = None

    def extract_images(self, max_images: int = 10) -> List[Image]:
        """
        Extract images from PDF

        Args:
            max_images: Maximum number of images to extract

        Returns:
            List of Image objects
        """
        images = []

        try:
            self.doc = fitz.open(self.pdf_path)

            for page_num in range(len(self.doc)):
                if len(images) >= max_images:
                    break

                page = self.doc[page_num]
                image_list = page.get_images()

                for img_index, img in enumerate(image_list):
                    if len(images) >= max_images:
                        break

                    xref = img[0]
                    base_image = self.doc.extract_image(xref)

                    image = Image(
                        page_num=page_num,
                        image_index=img_index,
                        width=base_image["width"],
                        height=base_image["height"],
                        data=base_image["image"]
                    )
                    images.append(image)

            logger.info(f"Extracted {len(images)} images")
            return images

        except Exception as e:
            logger.error(f"Failed to extract images: {e}")
            return []
        finally:
            if self.doc:
                self.doc.close()

    def validate(self) -> Tuple[bool, str]:
        """
        Validate PDF quality

        Returns:
            Tuple of (is_valid, message)
        """
        result = self.validator.validate()

        if result.is_valid:
            message = f"PDF quality: {result.quality.value}. "
            if result.recommendations:
                message += result.recommendations[0]
            return True, message
        else:
            message = "PDF cannot be processed. "
            if result.issues:
                message += result.issues[0]
            return False, message

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract sections from text"""
        sections = {}

        # Split text into lines
        lines = text.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            # Check if line is a section header
            section_match = self._match_section_header(line)

            if section_match:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = section_match
                current_content = []
            else:
                # Add to current section
                if current_section:
                    current_content.append(line)

        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _match_section_header(self, line: str) -> Optional[str]:
        """Check if line matches a section header"""
        line = line.strip()

        # Must be reasonably short and not empty
        if not line or len(line) > 100:
            return None

        # Check against known patterns
        for section_name, pattern in self.SECTION_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                # Additional check: line should not contain too many words
                # (to avoid matching sentences that contain these words)
                word_count = len(line.split())
                if word_count <= 10:
                    return section_name

        return None

    def _extract_title(self, first_page_text: str) -> Optional[str]:
        """Extract title from first page text"""
        lines = first_page_text.split('\n')

        # Title is usually in the first few lines
        for line in lines[:10]:
            line = line.strip()
            # Title is usually longer than a few words but not too long
            if 10 < len(line) < 200 and not line.isupper():
                # Check if it's not an author line
                if not re.search(r'\b(and|,)\b', line) or line.count(' ') > 3:
                    return line

        return None

    def _extract_authors(self, first_page_text: str) -> List[str]:
        """Extract authors from first page text"""
        authors = []

        # Look for lines with multiple names separated by commas or 'and'
        lines = first_page_text.split('\n')

        for line in lines[1:15]:  # Skip title, look at next lines
            line = line.strip()

            # Skip empty lines and very short lines
            if len(line) < 10:
                continue

            # Check if line looks like author list
            if re.search(r'\b(and|,)\b', line):
                # Split by 'and' and commas
                parts = re.split(r'\s+and\s+|\s*,\s*', line)

                for part in parts:
                    part = part.strip()
                    # Author names usually contain spaces and are not too long
                    if 3 < len(part) < 50 and ' ' in part:
                        # Check if it looks like a name (not institution)
                        if not re.search(r'(university|institute|department|lab)', part, re.I):
                            authors.append(part)

                if authors:
                    break

        return authors[:10]  # Limit to 10 authors

    def _extract_abstract(self, text: Optional[str] = None) -> Optional[str]:
        """Extract abstract from paper"""
        if text is None:
            text = self.extract_text()

        # Find abstract section
        abstract_match = re.search(
            r'abstract\s*[:.]?\s*(.+?)(?=\n\s*\n|\n\s*(?:introduction|keywords|1\s|1\.))',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Clean up abstract
            abstract = re.sub(r'\s+', ' ', abstract)
            return abstract

        return None

    def _extract_year(self, pdf_metadata: dict) -> Optional[str]:
        """Extract publication year"""
        # Try from PDF metadata
        if pdf_metadata.get('creationDate'):
            date_str = pdf_metadata['creationDate']
            year_match = re.search(r'(\d{4})', date_str)
            if year_match:
                return year_match.group(1)

        # Try from modification date
        if pdf_metadata.get('modDate'):
            date_str = pdf_metadata['modDate']
            year_match = re.search(r'(\d{4})', date_str)
            if year_match:
                return year_match.group(1)

        return None

    def get_page_count(self) -> int:
        """Get number of pages in PDF"""
        try:
            if not self.doc:
                self.doc = fitz.open(self.pdf_path)
            count = len(self.doc)
            return count
        finally:
            if self.doc:
                self.doc.close()
                self.doc = None
