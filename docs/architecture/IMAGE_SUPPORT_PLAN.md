# Image Support Implementation Plan

## Problem Analysis

### Current State
- ✅ Images ARE extracted from PDF (output/images/)
- ✅ Images ARE referenced in Markdown (e.g., `![Figure 1](path/to/image.png)`)
- ❌ Images are LOST during Markdown → PPTX conversion
- ❌ `md_to_pptx.py` treats image markdown as plain text

### Root Cause
`tools/md_to_pptx.py` lacks:
1. Markdown image syntax recognition
2. Image path resolution
3. `python-pptx` image insertion logic
4. Image positioning and sizing logic

---

## Solution Design

### Phase 1: Enhance Markdown Parser

**File**: `tools/md_to_pptx.py`

**Changes**:

#### 1.1 Add Image Detection (Line ~55)
```python
# Current code:
elif line.startswith('- ') or line.startswith('* '):
    bullets.append(line[2:].strip())

# New code:
elif line.startswith('- ') or line.startswith('* '):
    content = line[2:].strip()

    # Check if content is an image markdown
    img_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', content)
    if img_match:
        # Store as image, not text
        bullets.append({
            'type': 'image',
            'alt': img_match.group(1),
            'path': img_match.group(2)
        })
    else:
        bullets.append({
            'type': 'text',
            'content': content
        })
```

#### 1.2 Update Slide Data Structure
```python
# Old structure:
{
    'title': str,
    'bullets': List[str]
}

# New structure:
{
    'title': str,
    'bullets': List[dict]  # Each has 'type' and content
}
```

---

### Phase 2: Implement Image Insertion

**File**: `tools/md_to_pptx.py`

#### 2.1 Add Image Processing Function (after line ~145)

```python
def add_image_to_slide(slide, image_path: str, left: float, top: float, max_width: float, max_height: float):
    """
    Add image to slide with proper sizing

    Args:
        slide: python-pptx slide object
        image_path: Path to image file
        left: Left position in inches
        top: Top position in inches
        max_width: Maximum width in inches
        max_height: Maximum height in inches

    Returns:
        True if successful, False otherwise
    """
    from pathlib import Path

    # Resolve image path
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"⚠️  Image not found: {image_path}")
        return False

    try:
        from PIL import Image

        # Get image dimensions
        with Image.open(img_path) as img:
            img_width, img_height = img.size

        # Calculate aspect ratio
        aspect = img_width / img_height

        # Calculate display size (fit within max bounds)
        if max_width / aspect <= max_height:
            # Width-constrained
            display_width = max_width
            display_height = max_width / aspect
        else:
            # Height-constrained
            display_height = max_height
            display_width = max_height * aspect

        # Add picture to slide
        slide.shapes.add_picture(
            str(img_path),
            Inches(left),
            Inches(top),
            width=Inches(display_width),
            height=Inches(display_height)
        )

        return True

    except Exception as e:
        print(f"❌ Failed to add image {image_path}: {e}")
        return False
```

#### 2.2 Update Slide Creation Logic (Line ~116)

```python
# Current code (simplified):
for i, bullet in enumerate(slide_data['bullets'][:6]):
    p.text = bullet
    p.font.size = Pt(24)

# New code:
has_images = any(b.get('type') == 'image' for b in slide_data['bullets'])

if has_images:
    # Mixed content slide (text + images)
    # Reserve top 2 inches for title
    # Use remaining space for content

    current_top = 2.0
    text_items = [b for b in slide_data['bullets'] if b.get('type') == 'text']
    image_items = [b for b in slide_data['bullets'] if b.get('type') == 'image']

    # Add text on left side (40% width)
    if text_items:
        text_left = Inches(0.75)
        text_top = Inches(2.0)
        text_width = Inches(4.5)
        text_height = Inches(5)

        text_box = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
        text_frame = text_box.text_frame
        text_frame.word_wrap = True

        for i, item in enumerate(text_items[:4]):
            if i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()

            p.text = item['content']
            p.font.size = Pt(20)
            p.space_after = Pt(10)

    # Add image on right side (60% width)
    if image_items:
        for img_item in image_items[:2]:  # Max 2 images per slide
            img_left = 5.5
            img_top = 2.5
            img_max_width = 7.0
            img_max_height = 4.5

            add_image_to_slide(
                slide,
                img_item['path'],
                img_left,
                img_top,
                img_max_width,
                img_max_height
            )

else:
    # Text-only slide (original logic)
    for i, bullet in enumerate(slide_data['bullets'][:6]):
        # ... existing text logic ...
```

---

### Phase 3: Smart Image Selection

**File**: `src/pdf_image_extractor.py` (enhance existing)

#### 3.1 Improve Caption Detection
```python
def _find_caption_enhanced(self, page, page_num: int, pdf_doc) -> dict:
    """
    Enhanced caption detection with structured output

    Returns:
        {
            'text': str,  # Caption text
            'is_framework': bool,  # Is this a framework/architecture diagram?
            'is_results': bool,  # Is this a results table/chart?
            'is_method': bool,  # Is this a method visualization?
        }
    """
    text = page.get_text()

    # Framework detection keywords
    framework_keywords = [
        'framework', 'architecture', 'overview', 'system',
        'pipeline', 'workflow', 'structure', 'diagram'
    ]

    # Results detection keywords
    results_keywords = [
        'results', 'performance', 'comparison', 'accuracy',
        'table', 'chart', 'evaluation'
    ]

    # Find caption
    caption_text = self._find_caption(page, page_num, pdf_doc)

    # Classify type
    is_framework = any(kw in caption_text.lower() for kw in framework_keywords)
    is_results = any(kw in caption_text.lower() for kw in results_keywords)
    is_method = 'method' in caption_text.lower() or 'approach' in caption_text.lower()

    return {
        'text': caption_text,
        'is_framework': is_framework,
        'is_results': is_results,
        'is_method': is_method
    }
```

#### 3.2 Prioritize Key Figures
```python
def prioritize_figures_enhanced(self, figures: List[dict]) -> List[dict]:
    """
    Enhanced prioritization with content awareness

    Priority order:
    1. Framework/System diagrams (most important for understanding)
    2. Results/Performance charts (shows impact)
    3. Method visualizations (shows approach)
    4. Other figures
    """
    for fig in figures:
        score = 0

        # Framework diagram: +5 points (highest priority)
        if fig.get('is_framework'):
            score += 5

        # Results chart: +4 points
        elif fig.get('is_results'):
            score += 4

        # Method diagram: +3 points
        elif fig.get('is_method'):
            score += 3

        # Has caption: +3 points
        if fig['caption']:
            score += 3

        # Good aspect ratio: +2 points
        aspect = fig['width'] / fig['height'] if fig['height'] > 0 else 0
        if 0.8 <= aspect <= 2.0:
            score += 2

        fig['priority_score'] = score

    # Sort by score
    return sorted(figures, key=lambda x: x['priority_score'], reverse=True)
```

---

## Implementation Timeline

### Week 1: Core Image Support
- [ ] Day 1-2: Implement Phase 1 (Markdown parser enhancement)
- [ ] Day 3-4: Implement Phase 2 (Image insertion logic)
- [ ] Day 5: Testing with Human-In-the-Loop paper

### Week 2: Enhanced Features
- [ ] Day 1-2: Implement Phase 3 (Smart selection)
- [ ] Day 3-4: Testing and refinement
- [ ] Day 5: Documentation and final validation

---

## Testing Plan

### Test Case 1: Human-In-the-Loop Paper
**Input**: `papers/Human-In-the-Loop.pdf`
**Expected**:
- Extract at least 3 figures
- Figure 1 (Framework diagram) should be highest priority
- PPTX should contain actual images, not text references
- Images should be properly sized and positioned

### Test Case 2: Text-Only Slide
**Input**: Slide with no images
**Expected**:
- Slide renders as before (no layout changes)
- Text layout remains unchanged

### Test Case 3: Mixed Content Slide
**Input**: Slide with both text and image
**Expected**:
- Text on left (40% width)
- Image on right (60% width)
- Proper vertical alignment

---

## Success Metrics

### Before
- ❌ Images in Markdown: 0/3 displayed in PPTX
- ❌ HULA Framework diagram: Not visible
- ❌ Results charts: Not visible

### After
- ✅ Images in Markdown: 3/3 displayed in PPTX
- ✅ HULA Framework diagram: Visible and prominent
- ✅ Results charts: Visible and readable
- ✅ Image quality: No quality loss
- ✅ Layout: Professional appearance

---

## Risk Mitigation

### Risk 1: Image Path Resolution
**Issue**: Relative paths might not resolve correctly
**Solution**: Convert to absolute paths before insertion

### Risk 2: Image Size Too Large
**Issue**: Large images might overflow slide
**Solution**: Implement max_width/max_height constraints with aspect ratio preservation

### Risk 3: Missing Dependencies
**Issue**: PIL/Pillow might not be available
**Solution**: Add try/except fallback, use python-pptx size detection

### Risk 4: Performance
**Issue**: Large images slow down processing
**Solution**: Cache resized images, implement size limits (200-2000px)

---

## Rollback Plan

If issues arise:
1. Revert `md_to_pptx.py` to original version
2. Existing text-based slides continue to work
3. No impact on PDF parsing or Markdown generation

---

## Dependencies

**Required** (already installed):
- ✅ python-pptx >= 1.0.2
- ✅ Pillow >= 10.2.0
- ✅ PyMuPDF (fitz)

**Optional** (for enhanced features):
- None

---

## Files to Modify

1. **tools/md_to_pptx.py** (main changes)
   - Add image detection (~20 lines)
   - Add image insertion function (~40 lines)
   - Update slide creation logic (~50 lines)

2. **src/pdf_image_extractor.py** (optional enhancements)
   - Enhanced caption detection (~30 lines)
   - Improved prioritization (~20 lines)

3. **docs/architecture/IMAGE_SUPPORT_PLAN.md** (this file)
   - Implementation guide

---

## Estimated Effort

- **Development**: 2-3 days
- **Testing**: 1 day
- **Documentation**: 0.5 day
- **Total**: 3.5 - 4.5 days

---

## Next Steps

1. ✅ Create implementation plan (this document)
2. ⬜ Implement Phase 1: Markdown parser
3. ⬜ Implement Phase 2: Image insertion
4. ⬜ Test with Human-In-the-Loop paper
5. ⬜ Implement Phase 3: Smart selection (optional)
6. ⬜ Final validation and documentation

---

**Document Version**: 1.0
**Created**: 2026-03-10
**Status**: Ready for Implementation
