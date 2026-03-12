"""
PDF Image Extractor for PaperReader

Extracts key figures and charts from PDF papers
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)


class PDFImageExtractor:
    """Extract key figures from PDF papers"""

    def __init__(self, output_dir: str = "output/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_key_figures(self, pdf_path: str, max_figures: int = 5) -> List[dict]:
        """
        Extract key figures from PDF
        
        Args:
            pdf_path: Path to PDF file
            max_figures: Maximum number of figures to extract
            
        Returns:
            List of figure info dicts: {
                'image_path': str,
                'caption': str,
                'page_num': int,
                'figure_num': int
            }
        """
        logger.info(f"Extracting key figures from {pdf_path}")
        
        pdf_doc = fitz.open(pdf_path)
        figures = []
        
        paper_name = Path(pdf_path).stem
        
        # Strategy: Extract images that are likely figures
        # 1. Large images (not icons/small graphics)
        # 2. Images with captions (Figure X, Table X)
        # 3. Charts/graphs (detected by size and position)
        
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                if len(figures) >= max_figures:
                    break
                
                # Get image info
                xref = img[0]
                base_image = pdf_doc.extract_image(xref)
                
                # Check image size (skip small images)
                width = base_image["width"]
                height = base_image["height"]
                
                # Skip small images (< 200px in either dimension)
                if width < 200 or height < 200:
                    continue
                
                # Skip very large images (> 2000px)
                if width > 2000 or height > 2000:
                    continue
                
                # Extract image
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Save image
                figure_num = len(figures) + 1
                image_filename = f"{paper_name}_figure_{figure_num}.{image_ext}"
                image_path = self.output_dir / image_filename
                
                with open(image_path, 'wb') as f:
                    f.write(image_bytes)
                
                # Try to find caption
                caption = self._find_caption(page, page_num, pdf_doc)
                
                figures.append({
                    'image_path': str(image_path),
                    'caption': caption,
                    'page_num': page_num + 1,
                    'figure_num': figure_num,
                    'width': width,
                    'height': height
                })
                
                logger.info(f"Extracted figure {figure_num}: {image_filename} ({width}x{height})")
        
        pdf_doc.close()
        
        logger.info(f"Extracted {len(figures)} figures")
        return figures
    
    def _find_caption(self, page, page_num: int, pdf_doc) -> str:
        """
        Try to find figure caption near the image
        
        Args:
            page: PDF page object
            page_num: Page number
            pdf_doc: PDF document
            
        Returns:
            Caption text or empty string
        """
        # Get page text
        text = page.get_text()
        
        # Look for "Figure X" or "Table X" patterns
        patterns = [
            r'Figure\s+\d+[:.].*',
            r'Fig\.?\s+\d+[:.].*',
            r'Table\s+\d+[:.].*',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Return first match (most likely caption)
                caption = matches[0].strip()
                # Limit caption length
                if len(caption) > 100:
                    caption = caption[:100] + "..."
                return caption
        
        return ""

    def prioritize_figures(self, figures: List[dict]) -> List[dict]:
        """
        Prioritize figures by importance
        
        Args:
            figures: List of figure dicts
            
        Returns:
            Prioritized list of figures
        """
        # Priority factors:
        # 1. Has caption (high priority)
        # 2. Good aspect ratio (landscape or square)
        # 3. Reasonable size
        
        scored_figures = []
        
        for fig in figures:
            score = 0
            
            # Has caption: +3 points
            if fig['caption']:
                score += 3
            
            # Good aspect ratio: +2 points
            width = fig['width']
            height = fig['height']
            aspect_ratio = width / height if height > 0 else 0
            
            if 0.8 <= aspect_ratio <= 2.0:  # Landscape or square
                score += 2
            
            # Reasonable size: +1 point
            if 400 <= width <= 1500 and 300 <= height <= 1200:
                score += 1
            
            scored_figures.append((score, fig))
        
        # Sort by score (descending)
        scored_figures.sort(key=lambda x: x[0], reverse=True)
        
        # Return top figures
        return [fig for score, fig in scored_figures]

    def extract_and_save(self, pdf_path: str, max_figures: int = 5) -> List[dict]:
        """
        Extract figures and save to disk
        
        Args:
            pdf_path: Path to PDF
            max_figures: Maximum figures to extract
            
        Returns:
            List of figure info
        """
        # Extract all potential figures
        figures = self.extract_key_figures(pdf_path, max_figures * 2)
        
        # Prioritize
        prioritized = self.prioritize_figures(figures)
        
        # Return top N
        return prioritized[:max_figures]
