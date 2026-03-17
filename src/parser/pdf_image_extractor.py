"""
PDF Image Extractor for PaperReader

Extracts key figures and charts from PDF papers
"""

import hashlib
import io
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF

try:
    from pdf2image import convert_from_path
except ImportError:  # pragma: no cover - optional dependency at runtime
    convert_from_path = None

try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer
except ImportError:  # pragma: no cover - optional dependency at runtime
    extract_pages = None
    LTTextContainer = None

logger = logging.getLogger(__name__)


class PDFImageExtractor:
    """Extract key figures from PDF papers"""

    CAPTION_PATTERNS = [
        re.compile(r"Figure\s+(\d+)\s*[:.]\s*(.*)", re.IGNORECASE),
        re.compile(r"Fig\.\s*(\d+)\s*[:.]\s*(.*)", re.IGNORECASE),
        re.compile(r"FIG\.\s*(\d+)\s*[:.]\s*(.*)", re.IGNORECASE),
    ]

    def __init__(self, output_dir: str = "outputs/images"):
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

        caption_figures = self.extract_figures_by_caption(
            pdf_path,
            self.output_dir,
            max_figures=max_figures,
        )

        if len(caption_figures) >= max_figures:
            logger.info(f"Extracted {len(caption_figures)} figures via caption-based extraction")
            return caption_figures[:max_figures]

        embedded_limit = max_figures if not caption_figures else max_figures - len(caption_figures)
        embedded_figures = self._extract_embedded_figures(pdf_path, embedded_limit)

        figures = self._merge_figure_results(caption_figures, embedded_figures)
        logger.info(f"Extracted {len(figures)} figures")
        return figures[:max_figures]

    def extract_figures_by_caption(
        self,
        pdf_path: str,
        output_dir: Optional[Path] = None,
        max_figures: int = 5,
    ) -> List[dict]:
        """Extract complete figure regions by locating figure captions first."""
        output_dir = Path(output_dir or self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_doc = fitz.open(pdf_path)
        paper_name = Path(pdf_path).stem
        text_positions = self._extract_text_positions(pdf_path)
        captions = self._find_figure_captions(text_positions)

        if not captions:
            pdf_doc.close()
            logger.info("No figure captions found for caption-based extraction")
            return []

        captions_by_page: Dict[int, List[dict]] = {}
        for caption in captions:
            captions_by_page.setdefault(caption["page_num"], []).append(caption)

        figures = []

        try:
            for page_num, page_captions in sorted(captions_by_page.items()):
                page = pdf_doc[page_num - 1]
                page_width = page.rect.width
                page_height = page.rect.height
                graphic_regions = self._collect_graphic_regions(page, page_height)

                ordered_captions = sorted(page_captions, key=lambda item: item["y0"], reverse=True)

                for index, caption in enumerate(ordered_captions):
                    if len(figures) >= max_figures:
                        break

                    bbox = self._determine_figure_region(
                        page_width=page_width,
                        page_height=page_height,
                        caption=caption,
                        ordered_captions=ordered_captions,
                        index=index,
                        graphic_regions=graphic_regions,
                    )

                    if not bbox or not self._is_likely_figure_region(bbox, page_height):
                        continue

                    image_name = f"{paper_name}_figure_{caption['figure_num']}.png"
                    extracted = self._extract_region_as_image(
                        pdf_path=pdf_path,
                        page_num=page_num,
                        bbox=bbox,
                        output_dir=output_dir,
                        image_name=image_name,
                    )

                    if not extracted:
                        continue

                    image_path, width, height, image_hash = extracted
                    figures.append(
                        {
                            "image_path": image_path,
                            "caption": caption["caption"],
                            "page_num": page_num,
                            "figure_num": caption["figure_num"],
                            "width": width,
                            "height": height,
                            "hash": image_hash,
                        }
                    )

                    logger.info(
                        "Extracted caption-based figure %s from page %s",
                        caption["figure_num"],
                        page_num,
                    )

                if len(figures) >= max_figures:
                    break
        finally:
            pdf_doc.close()

        return figures

    def _extract_embedded_figures(self, pdf_path: str, max_figures: int) -> List[dict]:
        """Fallback strategy: extract embedded images that look like figures."""
        pdf_doc = fitz.open(pdf_path)
        figures = []
        paper_name = Path(pdf_path).stem

        try:
            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                image_list = page.get_images(full=True)
                page_rect = page.rect

                for img in image_list:
                    if len(figures) >= max_figures:
                        break

                    xref = img[0]
                    base_image = pdf_doc.extract_image(xref)
                    width = base_image["width"]
                    height = base_image["height"]
                    image_rects = page.get_image_rects(xref)

                    if not self._should_keep_image(
                        width=width,
                        height=height,
                        image_rects=image_rects,
                        page_rect=page_rect,
                    ):
                        continue

                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_hash = hashlib.md5(image_bytes).hexdigest()

                    figure_num = len(figures) + 1
                    image_filename = f"{paper_name}_figure_{figure_num}.{image_ext}"
                    image_path = self.output_dir / image_filename

                    with open(image_path, "wb") as file_obj:
                        file_obj.write(image_bytes)

                    caption = self._find_caption(page, page_num, pdf_doc)

                    figures.append(
                        {
                            "image_path": str(image_path),
                            "caption": caption,
                            "page_num": page_num + 1,
                            "figure_num": figure_num,
                            "width": width,
                            "height": height,
                            "hash": image_hash,
                        }
                    )

                    logger.info(
                        "Extracted embedded figure %s: %s (%sx%s)",
                        figure_num,
                        image_filename,
                        width,
                        height,
                    )

                if len(figures) >= max_figures:
                    break
        finally:
            pdf_doc.close()

        return figures

    def _extract_text_positions(self, pdf_path: str) -> List[dict]:
        """Extract text blocks with bounding boxes via PDFMiner."""
        if extract_pages is None or LTTextContainer is None:
            logger.warning("pdfminer.six is not installed; skipping caption-based extraction")
            return []

        text_positions = []

        for page_num, layout in enumerate(extract_pages(pdf_path), start=1):
            for element in self._iter_layout_elements(layout):
                if not isinstance(element, LTTextContainer):
                    continue

                text = re.sub(r"\s+", " ", element.get_text()).strip()
                if not text:
                    continue

                text_positions.append(
                    {
                        "text": text,
                        "x0": float(element.x0),
                        "y0": float(element.y0),
                        "x1": float(element.x1),
                        "y1": float(element.y1),
                        "page_num": page_num,
                    }
                )

        return text_positions

    def _iter_layout_elements(self, element):
        """Yield layout elements recursively."""
        yield element
        if hasattr(element, "_objs"):
            for child in element:
                yield from self._iter_layout_elements(child)

    def _find_figure_captions(self, text_positions: List[dict]) -> List[dict]:
        """Find figure captions and return their positions."""
        captions = []

        for block in text_positions:
            text = block["text"]

            for pattern in self.CAPTION_PATTERNS:
                match = pattern.search(text)
                if not match:
                    continue

                figure_num = int(match.group(1))
                caption_text = re.sub(r"\s+", " ", text).strip()
                captions.append(
                    {
                        "caption": caption_text[:300],
                        "figure_num": figure_num,
                        "page_num": block["page_num"],
                        "x0": block["x0"],
                        "y0": block["y0"],
                        "x1": block["x1"],
                        "y1": block["y1"],
                    }
                )
                break

        captions.sort(key=lambda item: (item["page_num"], -item["y0"], item["x0"]))
        return captions

    def _determine_figure_region(
        self,
        page_width: float,
        page_height: float,
        caption: dict,
        ordered_captions: List[dict],
        index: int,
        graphic_regions: List[Tuple[float, float, float, float]],
    ) -> Optional[Tuple[float, float, float, float]]:
        """Estimate the figure region above a caption."""
        lower_bound = min(page_height - 8, caption["y1"] + 8)
        upper_bound = page_height - 18

        if index > 0:
            upper_bound = min(upper_bound, ordered_captions[index - 1]["y0"] - 8)

        if upper_bound <= lower_bound:
            return None

        candidate_regions = []
        for region in graphic_regions:
            x0, y0, x1, y1 = region
            if y1 < lower_bound or y0 > upper_bound:
                continue
            if x1 - x0 < page_width * 0.12:
                continue
            candidate_regions.append(region)

        if candidate_regions:
            bbox = self._merge_regions(candidate_regions)
            bbox = (
                max(12, bbox[0] - 12),
                max(lower_bound, bbox[1] - 12),
                min(page_width - 12, bbox[2] + 12),
                min(upper_bound, bbox[3] + 12),
            )
            return self._clamp_bbox(bbox, page_width, page_height)

        estimated_height = min(max(page_height * 0.32, 180), page_height * 0.55)
        fallback_bbox = (
            page_width * 0.08,
            lower_bound,
            page_width * 0.92,
            min(upper_bound, lower_bound + estimated_height),
        )
        return self._clamp_bbox(fallback_bbox, page_width, page_height)

    def _collect_graphic_regions(
        self,
        page,
        page_height: float,
    ) -> List[Tuple[float, float, float, float]]:
        """Collect image and vector graphic bounds on a page in PDF coordinates."""
        regions = []
        seen = set()

        for image in page.get_images(full=True):
            xref = image[0]
            for rect in page.get_image_rects(xref):
                region = self._fitz_rect_to_pdf_bbox(rect, page_height)
                key = tuple(round(value, 1) for value in region)
                if key not in seen:
                    regions.append(region)
                    seen.add(key)

        for drawing in page.get_drawings():
            rect = drawing.get("rect")
            if not rect:
                continue
            if rect.width < 40 or rect.height < 40:
                continue

            region = self._fitz_rect_to_pdf_bbox(rect, page_height)
            key = tuple(round(value, 1) for value in region)
            if key not in seen:
                regions.append(region)
                seen.add(key)

        return regions

    def _fitz_rect_to_pdf_bbox(
        self,
        rect: fitz.Rect,
        page_height: float,
    ) -> Tuple[float, float, float, float]:
        """Convert a PyMuPDF rect to bottom-left PDF coordinates."""
        return (
            float(rect.x0),
            float(page_height - rect.y1),
            float(rect.x1),
            float(page_height - rect.y0),
        )

    def _merge_regions(
        self,
        regions: List[Tuple[float, float, float, float]],
    ) -> Tuple[float, float, float, float]:
        """Return the union of multiple regions."""
        return (
            min(region[0] for region in regions),
            min(region[1] for region in regions),
            max(region[2] for region in regions),
            max(region[3] for region in regions),
        )

    def _clamp_bbox(
        self,
        bbox: Tuple[float, float, float, float],
        page_width: float,
        page_height: float,
    ) -> Tuple[float, float, float, float]:
        """Clamp a bbox to page bounds."""
        x0, y0, x1, y1 = bbox
        return (
            max(0.0, min(x0, page_width)),
            max(0.0, min(y0, page_height)),
            max(0.0, min(x1, page_width)),
            max(0.0, min(y1, page_height)),
        )

    def _extract_region_as_image(
        self,
        pdf_path: str,
        page_num: int,
        bbox: Tuple[float, float, float, float],
        output_dir: Path,
        image_name: str,
    ) -> Optional[Tuple[str, int, int, str]]:
        """Render a PDF region to an image file and return path, size, and hash."""
        output_path = Path(output_dir) / image_name

        try:
            if convert_from_path is None:
                raise RuntimeError("pdf2image is not installed")

            rendered_page = convert_from_path(
                pdf_path,
                dpi=200,
                first_page=page_num,
                last_page=page_num,
                fmt="png",
            )[0]
            pdf_doc = fitz.open(pdf_path)
            try:
                page = pdf_doc[page_num - 1]
                page_width = page.rect.width
                page_height = page.rect.height
            finally:
                pdf_doc.close()

            scale_x = rendered_page.width / page_width
            scale_y = rendered_page.height / page_height
            x0, y0, x1, y1 = bbox
            crop_box = (
                max(0, int(round(x0 * scale_x))),
                max(0, int(round((page_height - y1) * scale_y))),
                min(rendered_page.width, int(round(x1 * scale_x))),
                min(rendered_page.height, int(round((page_height - y0) * scale_y))),
            )
            cropped = rendered_page.crop(crop_box)
            if cropped.width < 50 or cropped.height < 50:
                return None

            buffer = io.BytesIO()
            cropped.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            with open(output_path, "wb") as file_obj:
                file_obj.write(image_bytes)

            return str(output_path), cropped.width, cropped.height, hashlib.md5(image_bytes).hexdigest()
        except Exception as exc:
            logger.warning("pdf2image region extraction failed on page %s: %s", page_num, exc)
            return self._extract_region_as_image_with_fitz(pdf_path, page_num, bbox, output_path)

    def _extract_region_as_image_with_fitz(
        self,
        pdf_path: str,
        page_num: int,
        bbox: Tuple[float, float, float, float],
        output_path: Path,
    ) -> Optional[Tuple[str, int, int, str]]:
        """Fallback renderer using PyMuPDF if pdf2image is unavailable."""
        pdf_doc = fitz.open(pdf_path)

        try:
            page = pdf_doc[page_num - 1]
            page_height = page.rect.height
            x0, y0, x1, y1 = bbox
            clip = fitz.Rect(x0, page_height - y1, x1, page_height - y0)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip, alpha=False)
            if pixmap.width < 50 or pixmap.height < 50:
                return None

            pixmap.save(str(output_path))
            image_bytes = output_path.read_bytes()
            return str(output_path), pixmap.width, pixmap.height, hashlib.md5(image_bytes).hexdigest()
        finally:
            pdf_doc.close()

    def _is_likely_figure_region(
        self,
        bbox: Tuple[float, float, float, float],
        page_height: float,
    ) -> bool:
        """Return whether a region looks like a plausible figure area."""
        x0, y0, x1, y1 = bbox
        width = x1 - x0
        height = y1 - y0

        if width < 160 or height < page_height * 0.12:
            return False

        if height > page_height * 0.85:
            return False

        aspect_ratio = width / height if height else 0
        if aspect_ratio > 6 or aspect_ratio < 0.3:
            return False

        return True

    def _merge_figure_results(self, primary: List[dict], secondary: List[dict]) -> List[dict]:
        """Merge figure results while avoiding obvious duplicates."""
        merged = []
        seen = set()

        for fig in primary + secondary:
            caption = re.sub(r"\s+", " ", fig.get("caption", "")).strip().lower()
            if caption:
                key = ("caption", fig.get("page_num"), caption)
            else:
                key = ("hash", fig.get("hash"))

            if key in seen:
                continue

            seen.add(key)
            merged.append(fig)

        return merged

    def _should_keep_image(
        self,
        width: int,
        height: int,
        image_rects: List[fitz.Rect],
        page_rect: fitz.Rect,
    ) -> bool:
        """Return whether an extracted PDF image is likely to be a useful figure."""
        if width < 200 or height < 200:
            return False

        if width > 2000 or height > 2000:
            return False

        aspect_ratio = width / height if height else 0
        if aspect_ratio > 5 or aspect_ratio < 0.2:
            return False

        if width < 240 and height < 240 and 0.8 <= aspect_ratio <= 1.25:
            return False

        if image_rects:
            page_width = page_rect.width
            page_height = page_rect.height
            edge_margin_x = page_width * 0.04
            edge_margin_y = page_height * 0.04

            if all(
                rect.x0 <= page_rect.x0 + edge_margin_x
                or rect.y0 <= page_rect.y0 + edge_margin_y
                or rect.x1 >= page_rect.x1 - edge_margin_x
                or rect.y1 >= page_rect.y1 - edge_margin_y
                for rect in image_rects
            ):
                return False

        return True

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
        text = page.get_text()

        patterns = [
            r"Figure\s+\d+[:.].*",
            r"Fig\.?\s+\d+[:.].*",
            r"Table\s+\d+[:.].*",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                caption = matches[0].strip()
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
        scored_figures = []

        for fig in figures:
            score = 0

            if fig["caption"]:
                score += 3

            width = fig["width"]
            height = fig["height"]
            aspect_ratio = width / height if height > 0 else 0

            if 0.8 <= aspect_ratio <= 2.0:
                score += 2

            if 400 <= width <= 1500 and 300 <= height <= 1200:
                score += 1

            scored_figures.append((score, fig))

        scored_figures.sort(key=lambda item: item[0], reverse=True)
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
        figures = self.extract_key_figures(pdf_path, max_figures * 2)
        prioritized = self.prioritize_figures(figures)
        return prioritized[:max_figures]
