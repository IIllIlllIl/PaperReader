# Image Support - Visual Design

## Current Flow (Broken)

```
┌─────────────────┐
│  PDF Document   │
│  Human-In-Loop  │
│   (2.8 MB)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  PDFImageExtractor      │
│  ✅ Extract 10 figures  │
│  ✅ Save as PNG         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  output/images/         │
│  ├── figure_1.png 16KB  │ ← HULA Framework (IMPORTANT!)
│  ├── figure_2.png 15KB  │ ← Results Chart
│  └── figure_3.png 13KB  │ ← System Diagram
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  EnhancedPPTGenerator   │
│  ✅ Generate Markdown   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  output/markdown/                   │
│  Human-In-the-Loop_v3.md            │
│  ...                                │
│  ## Figure 1                        │
│  - ![Figure 1](output/images/...)  │ ← Image reference
│  ...                                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  md_to_pptx.py          │
│  ❌ NO IMAGE SUPPORT    │
│  - Treats ![...] as text│
│  - No add_picture()     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  output/slides/                     │
│  Human-In-the-Loop_v3.pptx          │
│  ❌ Slide 14: "Figure 1"            │
│     Content: "![Figure 1](...)"     │ ← TEXT, NOT IMAGE!
│     (User sees markdown text)       │
└─────────────────────────────────────┘
```

---

## Proposed Flow (Fixed)

```
┌─────────────────┐
│  PDF Document   │
│  Human-In-Loop  │
│   (2.8 MB)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  PDFImageExtractor              │
│  ✅ Extract 10 figures          │
│  ✅ Smart prioritization        │
│  🔍 Detect framework diagrams   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  output/images/                     │
│  ├── figure_1.png 16KB              │
│  │   📊 Type: Framework Diagram    │
│  │   🎯 Priority: HIGH (score: 8)  │
│  ├── figure_2.png 15KB              │
│  │   📊 Type: Results Chart        │
│  │   🎯 Priority: MEDIUM (score: 6)│
│  └── figure_3.png 13KB              │
│      📊 Type: System Diagram        │
│      🎯 Priority: MEDIUM (score: 5) │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  EnhancedPPTGenerator               │
│  ✅ Generate Markdown with images   │
│  ✅ Include priority metadata       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  output/markdown/                           │
│  Human-In-the-Loop_v3.md                    │
│  ...                                        │
│  ## Figure 1: Framework Overview           │
│  - ![Framework](output/images/...)         │
│  - Priority: HIGH                          │
│  ...                                        │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  md_to_pptx.py (ENHANCED) ⭐                │
│  ✅ Detect ![alt](path) syntax             │
│  ✅ Resolve image paths                    │
│  ✅ Calculate optimal size & position      │
│  ✅ Use slide.shapes.add_picture()         │
│  📐 Maintain aspect ratio                  │
│  🎨 Professional layout                    │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  output/slides/                             │
│  Human-In-the-Loop_v3.pptx ✨               │
│                                             │
│  ✅ Slide 14: Figure 1 - Framework         │
│     ┌─────────────────────────────┐        │
│     │                             │        │
│     │   [ACTUAL IMAGE HERE]       │        │
│     │   HULA Framework Diagram    │        │
│     │                             │        │
│     └─────────────────────────────┘        │
│     (User sees the actual diagram)          │
│                                             │
│  ✅ Slide 15: Figure 2 - Results           │
│     [Results Chart Image]                   │
│                                             │
│  ✅ Professional layout                     │
│  ✅ Images properly sized                   │
│  ✅ Easy to understand                      │
└─────────────────────────────────────────────┘
```

---

## Slide Layout Examples

### Text-Only Slide (No Change)

```
┌──────────────────────────────────────┐
│  Research Background                 │
├──────────────────────────────────────┤
│                                      │
│  • Large Language Models (LLMs)...  │
│                                      │
│  • Existing frameworks such as...   │
│                                      │
│  • However, the state of...         │
│                                      │
│  • The paper addresses...           │
│                                      │
│  • Key contributions include...     │
│                                      │
└──────────────────────────────────────┘
```

### Image-Only Slide (New)

```
┌──────────────────────────────────────┐
│  Figure 1: HULA Framework           │
├──────────────────────────────────────┤
│                                      │
│  ┌────────────────────────────────┐ │
│  │                                │ │
│  │                                │ │
│  │    [ACTUAL FRAMEWORK IMAGE]    │ │
│  │                                │ │
│  │                                │ │
│  │   AI Planner  →  AI Coding    │ │
│  │        ↓           ↓          │ │
│  │      Human Agent              │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│                                      │
│  *Figure 1: An Overview of our...   │
└──────────────────────────────────────┘
```

### Mixed Content Slide (New)

```
┌──────────────────────────────────────┐
│  Experimental Results                │
├──────────────────────────────────────┤
│                                      │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ Key      │  │                  │ │
│  │ Findings │  │                  │ │
│  │          │  │  [RESULTS CHART] │ │
│  │ • 27%    │  │                  │ │
│  │   better │  │   Performance    │ │
│  │          │  │   Comparison     │ │
│  │ • 89%    │  │                  │ │
│  │   accept │  │                  │ │
│  │          │  │                  │ │
│  │ • Faster │  │                  │ │
│  │          │  │                  │ │
│  └──────────┘  └──────────────────┘ │
│   Text (40%)      Image (60%)       │
└──────────────────────────────────────┘
```

---

## Code Example: Before vs After

### Before (Broken)

```python
# tools/md_to_pptx.py (line 55)
elif line.startswith('- ') or line.startswith('* '):
    bullets.append(line[2:].strip())

# Result:
# bullets = ['![Figure 1](output/images/figure_1.png)']  ← Just text!
```

### After (Fixed)

```python
# tools/md_to_pptx.py (line 55)
elif line.startswith('- ') or line.startswith('* '):
    content = line[2:].strip()

    # Detect image markdown
    img_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', content)
    if img_match:
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

# Result:
# bullets = [{'type': 'image', 'alt': 'Figure 1', 'path': 'output/images/figure_1.png'}]
```

### Slide Creation: Before (Text Only)

```python
# tools/md_to_pptx.py (line 126)
for i, bullet in enumerate(slide_data['bullets'][:6]):
    if i == 0:
        p = text_frame.paragraphs[0]
    else:
        p = text_frame.add_paragraph()

    p.text = bullet  # ← All bullets treated as text
    p.font.size = Pt(24)
```

### Slide Creation: After (Image Support)

```python
# tools/md_to_pptx.py (line 126)
has_images = any(b.get('type') == 'image' for b in slide_data['bullets'])

if has_images:
    # Create mixed layout
    text_items = [b for b in slide_data['bullets'] if b.get('type') == 'text']
    image_items = [b for b in slide_data['bullets'] if b.get('type') == 'image']

    # Add text on left (40%)
    # ... text box creation ...

    # Add image on right (60%)
    for img in image_items[:2]:
        add_image_to_slide(
            slide,
            img['path'],
            left=5.5,
            top=2.5,
            max_width=7.0,
            max_height=4.5
        )
else:
    # Original text-only logic
    for i, bullet in enumerate(slide_data['bullets'][:6]):
        # ... existing code ...
```

---

## Success Criteria

### Visual Test: Human-In-the-Loop Paper

**Before (Current)**:
```
Open Human-In-the-Loop_v3.pptx
  → Slide 14: "Figure 1"
  → Content: "![Figure 1](output/images/Human-In-the-Loop_figure_1.png)"
  → User sees: Plain text (confusing!)
```

**After (Fixed)**:
```
Open Human-In-the-Loop_v3.pptx
  → Slide 14: "Figure 1: Framework Overview"
  → Content: [Actual HULA framework diagram]
  → User sees: Clear visual diagram ✨
```

### Quantitative Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Images displayed | 0/3 | 3/3 | ✅ 100% |
| Framework visible | ❌ No | ✅ Yes | ✅ Critical |
| Results charts visible | ❌ No | ✅ Yes | ✅ Important |
| User comprehension | Low | High | ✅ 2-3x better |
| Presentation quality | Text-only | Professional | ✅ Major upgrade |

---

**Document Version**: 1.0
**Created**: 2026-03-10
