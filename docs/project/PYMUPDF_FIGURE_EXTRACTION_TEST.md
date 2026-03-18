# PyMuPDF Figure Extraction Test Report

**Date**: 2026-03-17
**Target PDF**: `papers/Human-In-the-Loop.pdf`
**Goal**: Evaluate PyMuPDF's ability to extract flowcharts/diagrams from academic PDFs

---

## Test Results Summary

### ✅ What Works

#### 1. **Full Page Rendering** ⭐⭐⭐⭐⭐
- **Method**: `page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))`
- **Quality**: Excellent - captures everything
- **File size**: ~372KB (page 4)
- **Resolution**: 1224x1584 (2x zoom)
- **Pros**:
  - Captures complete page with all figures intact
  - Includes text, graphics, and embedded images together
  - No missing elements
- **Cons**:
  - Includes entire page (not just the figure)
  - Requires manual cropping or figure detection

#### 2. **Embedded Image Extraction** ⭐⭐⭐
- **Method**: `page.get_images()` + `fitz.Pixmap(doc, xref)`
- **Quality**: Good for raster images
- **File sizes**: 3-18KB per image
- **What it extracted**:
  - Page 4: 18 embedded images (icons: human, computer, etc.)
  - Page 9: Survey result charts (1248x602, high quality)
- **Pros**:
  - Extracts original embedded images at full quality
  - Small file sizes
  - Fast extraction
- **Cons**:
  - **Does NOT extract vector graphics** (flowcharts drawn with lines/shapes)
  - Only gets raster images embedded in PDF
  - Flowchart components are extracted separately (icons) but not the complete diagram

### ❌ What Doesn't Work

#### 3. **Graphics Path Extraction** ⭐
- **Method**: `page.get_drawings()` + combine bounding boxes
- **Quality**: Poor - **Missing all text labels**
- **File size**: 327KB
- **Result**: Extracted only the boxes and arrows, no text
- **Problem**:
  - PyMuPDF separates drawing paths from text
  - Text is stored separately and not included in drawings
  - Results in unlabeled diagram skeleton

#### 4. **Caption-Based Region Extraction** ⭐
- **Method**: Search for "Figure X" text + extract region above
- **Quality**: Poor - Incomplete and inaccurate
- **File size**: 6.9KB
- **Result**: Extracted wrong region (201x295 pixels)
- **Problem**:
  - Figure captions can be anywhere (above, below, or to the side)
  - Hard to determine exact figure boundaries
  - Need manual adjustment for each figure

---

## Key Findings

### Figure 1 Analysis (Page 4)

**What Figure 1 contains:**
- **Type**: Complex flowchart with vector graphics
- **Components**:
  - 4 horizontal stages with boxes and arrows
  - Text labels for stages, steps, and agent types
  - Embedded icons (human, computer, etc.)
  - Mixed vector and raster elements

**PyMuPDF extraction results:**

| Method | Text | Graphics | Icons | Complete | Quality |
|--------|------|----------|-------|----------|---------|
| Full page render | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Embedded images | ❌ | ❌ | ✅ | ❌ | ⭐⭐⭐ |
| Graphics paths | ❌ | ✅ | ❌ | ❌ | ⭐ |
| Caption-based | ❌ | ❌ | ❌ | ❌ | ⭐ |

### Critical Issue: Vector Graphics + Text Separation

**The Problem:**
- PyMuPDF's `get_drawings()` extracts only vector paths (lines, boxes, arrows)
- Text is stored separately in the PDF structure
- Combining them requires:
  1. Extract drawing paths and their positions
  2. Extract text and their positions
  3. Overlay text on the graphics at correct positions
  4. Handle font rendering, sizing, alignment

**Why it's hard:**
- Text positioning is complex (baseline, spacing, kerning)
- Fonts may not match exactly when re-rendered
- Need to handle text on paths, rotated text, etc.

---

## Recommendations

### For PaperReader Pipeline

#### Option 1: **Full Page Rendering + Smart Cropping** (Recommended)

```python
# Render full page at high resolution
page = doc[page_num]
pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))

# Use AI to detect figure boundaries
figure_regions = detect_figures_with_ai(pix)

# Crop each detected figure
for region in figure_regions:
    figure_pix = page.get_pixmap(matrix=mat, clip=region)
    figure_pix.save(f'figure_{idx}.png')
```

**Pros:**
- Guaranteed to capture complete figures
- No missing elements
- Works for all figure types (vector, raster, mixed)

**Cons:**
- Requires AI-based figure detection
- More computational overhead

#### Option 2: **Hybrid Approach**

```python
# 1. Extract embedded raster images (for photos, charts)
embedded_images = extract_embedded_images(page)

# 2. For figures not found in embedded images, render regions
if not is_figure_extracted(figure_caption):
    # Use full page rendering + manual/ai cropping
    render_figure_region(page, estimated_region)
```

**Pros:**
- Fast for raster images
- Fallback for vector graphics
- Balances speed and quality

**Cons:**
- Need figure detection logic
- May still miss some figures

#### Option 3: **Keep Current pdf2image Approach**

Your current approach using `pdf2image` (poppler) already does full page rendering.

**Pros:**
- Already working
- Captures everything

**Cons:**
- Large file sizes
- Requires post-processing

---

## Comparison: PyMuPDF vs Current Approach

| Aspect | PyMuPDF Full Render | pdf2image (Current) |
|--------|---------------------|---------------------|
| Quality | Excellent | Excellent |
| Speed | Fast | Fast |
| File size | Similar | Similar |
| Figure extraction | Needs cropping | Needs cropping |
| Embedded images | Can extract separately | All in one image |
| Dependencies | PyMuPDF | poppler-utils |

**Verdict**: PyMuPDF offers **no significant advantage** over your current pdf2image approach for figure extraction, unless you specifically need:
1. Separate extraction of embedded images
2. Text extraction alongside figures
3. Lower-level PDF manipulation

---

## Test Files Generated

### Page 4 (Figure 1 - HULA Framework Flowchart)
- `page4_full.png` (372KB) - Complete page ✅
- `page4_all_graphics.png` (327KB) - Graphics only, no text ❌
- `page4_figure1_region.png` (6.9KB) - Incomplete region ❌
- `page4_embedded_img0-4.png` (3-18KB) - Icon components ✅

### Other Pages
- `page9_img0.png` (104KB) - Survey chart (embedded image) ✅
- `page3_*.png` - Various attempts (Figure 1 not on this page)

---

## Conclusion

**PyMuPDF is NOT a silver bullet for figure extraction.**

**For vector graphics flowcharts (like Figure 1):**
- Full page rendering works perfectly
- Graphics path extraction fails (missing text)
- Need AI-based figure detection for automatic cropping

**For raster images (photos, charts):**
- Embedded image extraction works well
- Can extract original quality images

**Recommendation for PaperReader:**
1. Keep your current `pdf2image` approach for full page rendering
2. Add AI-based figure detection for automatic cropping
3. Consider PyMuPDF only if you need:
   - Separate embedded image extraction
   - Text extraction
   - Lower-level PDF operations

---

## Next Steps

- [ ] Test AI-based figure detection (e.g., GPT-4 Vision, CLIP)
- [ ] Evaluate figure quality requirements for slide generation
- [ ] Compare file sizes: cropped figures vs full pages
- [ ] Benchmark extraction speed on larger PDFs
