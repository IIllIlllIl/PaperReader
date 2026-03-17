# 🔄 Narrative Planner Integration Guide

**How to integrate narrative planning into the presentation pipeline**

---

## Overview

The Narrative Planner extracts a compelling research story from paper analysis, which can then guide slide planning and content generation.

---

## Pipeline Architecture

### Complete Pipeline

```
PDF
 ↓
PDFParser → Text
 ↓
ResearchMeetingAnalyzer → PaperAnalysis
 ↓
NarrativePlanner → PresentationNarrative  ← NEW!
 ↓
SlidePlanner → SlidePlan (guided by narrative)
 ↓
ContentGenerator → Slide Content
 ↓
PPTGenerator → Presentation
```

---

## Integration Points

### 1. **Basic Integration**

```python
from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.planning.narrative_planner import NarrativePlanner
from src.planning.slide_planner import SlidePlanner

# Parse PDF
parser = PDFParser(pdf_path)
text = parser.extract_text()

# Analyze paper
analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=model)
analysis = analyzer.analyze_paper_for_meeting(text, metadata)

# Extract narrative (NEW!)
narrative_planner = NarrativePlanner(api_key=api_key, model=model)
narrative = narrative_planner.extract_narrative(analysis)

# Plan slides (can use narrative)
slide_planner = SlidePlanner(api_key=api_key, model=model)
slide_plan = slide_planner.plan_slides(analysis, narrative=narrative)
```

### 2. **Enhanced Slide Planning with Narrative**

The narrative can guide slide planning to ensure a compelling story:

```python
class SlidePlanner:
    def plan_slides(self, analysis, narrative=None):
        """
        Plan slides, optionally using narrative to guide structure

        If narrative is provided:
        - Title slide uses hook
        - Problem slide uses problem
        - Related work uses limitations
        - Core idea uses key_idea
        - Results uses evidence
        - Discussion uses implications
        """
        # Use narrative to enhance slide planning
        if narrative:
            # Ensure narrative flow in slides
            return self._plan_with_narrative(analysis, narrative)
        else:
            # Standard planning without narrative
            return self._plan_standard(analysis)
```

### 3. **Narrative-Driven Slide Content**

Each slide can reference the narrative:

```python
def create_title_slide(self, narrative):
    """Create compelling title slide using narrative"""
    return Slide(
        title=narrative.key_idea,  # Main contribution
        subtitle=narrative.hook,   # Attention-grabbing hook
        type="title"
    )

def create_problem_slide(self, narrative):
    """Create problem slide with context"""
    return Slide(
        title="The Problem",
        bullets=[
            narrative.problem,
            f"Why it matters: {narrative.implications[:100]}"
        ],
        type="content"
    )

def create_core_idea_slide(self, narrative):
    """Create memorable core idea slide"""
    return Slide(
        title="Our Approach",
        bullets=[
            narrative.key_idea,
            narrative.method
        ],
        type="content",
        notes="This should be memorable and repeatable"
    )
```

---

## Usage Examples

### Example 1: Standalone Narrative Extraction

```python
# Just extract narrative from existing analysis
from src.planning.narrative_planner import NarrativePlanner

planner = NarrativePlanner(api_key=api_key, model=model)
narrative = planner.extract_narrative(analysis)

# Use narrative elements
print(f"Hook: {narrative.hook}")
print(f"Key Idea: {narrative.key_idea}")
print(f"Evidence: {narrative.evidence}")
```

### Example 2: Full Pipeline with Narrative

```python
def generate_presentation_with_narrative(pdf_path, output_path):
    """Generate presentation with narrative-driven approach"""

    # Step 1: Parse
    parser = PDFParser(pdf_path)
    text = parser.extract_text()

    # Step 2: Analyze
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=model)
    analysis = analyzer.analyze_paper_for_meeting(text)

    # Step 3: Extract narrative
    narrative_planner = NarrativePlanner(api_key=api_key, model=model)
    narrative = narrative_planner.extract_narrative(analysis)

    # Step 4: Plan slides with narrative guidance
    slide_planner = SlidePlanner(api_key=api_key, model=model)
    slide_plan = slide_planner.plan_slides(analysis, narrative=narrative)

    # Step 5: Generate content
    content_gen = ContentGenerator(api_key=api_key, model=model)
    slides = content_gen.generate_content(slide_plan, narrative=narrative)

    # Step 6: Create PPT
    ppt_gen = PPTGenerator()
    ppt_gen.create_presentation(slides, output_path)

    return {
        'analysis': analysis,
        'narrative': narrative,
        'slide_plan': slide_plan,
        'slides': slides
    }
```

### Example 3: Narrative for Speaking Notes

```python
def generate_speaking_notes(narrative):
    """Generate speaking notes from narrative"""
    return f"""
=================================================================
PRESENTATION SCRIPT (Based on Research Narrative)
=================================================================

[OPENING - 30 seconds]
{narrative.hook}

[PROBLEM - 1 minute]
{narrative.problem}

[RELATED WORK - 1 minute]
{narrative.limitations_of_prior_work}

[KEY IDEA - 30 seconds]
{narrative.key_idea}

[METHOD - 2 minutes]
{narrative.method}

[RESULTS - 2 minutes]
{narrative.evidence}

[IMPLICATIONS - 1 minute]
{narrative.implications}

=================================================================
Total Estimated Time: 7-8 minutes
=================================================================
"""
```

---

## Benefits of Narrative-Driven Approach

### 1. **Better Storytelling**

❌ **Without Narrative**:
```
Slide 1: Introduction
Slide 2: Background
Slide 3: Method
Slide 4: Results
```
(Linear, dry, hard to follow)

✅ **With Narrative**:
```
Slide 1: Hook (Why should you care?)
Slide 2: Problem (What's broken?)
Slide 3: Prior Work (What did others try?)
Slide 4: Our Idea (What's our insight?)
Slide 5: Method (How does it work?)
Slide 6: Evidence (Does it work?)
Slide 7: Implications (What's next?)
```
(Story arc, engaging, memorable)

### 2. **Memorable Presentations**

- **Hook** makes audience remember the opening
- **Key Idea** is concise and repeatable
- **Evidence** includes specific numbers
- **Implications** give them something to think about

### 3. **Consistent Message**

All slides reference the same narrative, ensuring:
- Coherent story throughout
- Clear takeaway message
- Logical flow between slides

---

## Cost Impact

### Additional Cost for Narrative

| Component | Cost |
|-----------|------|
| Paper Analysis | $0.012 |
| **Narrative Extraction** | **$0.009** |
| Slide Planning | $0.015 |
| Content Generation | $0.020 |
| **Total** | **$0.056** |

**Narrative adds only ~16% to total cost** but significantly improves presentation quality.

---

## When to Use Narrative Planning

### ✅ Recommended For

- **Research group meetings** - Academic audience expects story
- **Conference presentations** - Limited time, need compelling narrative
- **PhD defenses** - Clear story arc essential
- **Paper presentations** - Highlight contribution and impact
- **Research updates** - Make progress memorable

### ⚠️ Optional For

- **Quick overviews** - May not need full narrative
- **Technical deep-dives** - Focus on details, not story
- **Tutorial content** - Different structure (step-by-step)

### ❌ Not Suitable For

- **Business presentations** - Need ROI-focused narrative
- **Marketing decks** - Need different narrative structure
- **Status updates** - Just facts, no story

---

## Integration Checklist

To integrate narrative planning into your pipeline:

- [ ] Import `NarrativePlanner` from `src.planning.narrative_planner`
- [ ] Call `extract_narrative()` after paper analysis
- [ ] Pass narrative to `SlidePlanner.plan_slides()`
- [ ] Update `SlidePlan` model to include `narrative` field
- [ ] Modify content generator to use narrative elements
- [ ] Create narrative-driven slides (title, problem, core idea)
- [ ] Generate speaking notes from narrative
- [ ] Test with real papers

---

## Example: Complete Integration

```python
#!/usr/bin/env python3
"""
Complete pipeline with narrative planning
"""

from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer
from src.planning.narrative_planner import NarrativePlanner
from src.planning.slide_planner import SlidePlanner
from src.generation.content_generator import ContentGenerator
from src.generation.ppt_generator import PPTGenerator
from src.utils import load_config, get_api_key

def main():
    # Load config
    config = load_config()
    api_key = get_api_key(config)
    model = config['ai']['model']

    # Step 1: Parse PDF
    print("📄 Parsing PDF...")
    parser = PDFParser("papers/example.pdf")
    text = parser.extract_text()
    metadata = parser.extract_metadata()

    # Step 2: Analyze paper
    print("🤖 Analyzing paper...")
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=model)
    analysis = analyzer.analyze_paper_for_meeting(text, metadata.__dict__)

    # Step 3: Extract narrative (NEW!)
    print("📖 Extracting narrative...")
    narrative_planner = NarrativePlanner(api_key=api_key, model=model)
    narrative = narrative_planner.extract_narrative(analysis)

    # Display narrative
    print("\n" + "="*70)
    print("EXTRACTED NARRATIVE")
    print("="*70)
    print(f"Hook: {narrative.hook}")
    print(f"Key Idea: {narrative.key_idea}")
    print(f"Evidence: {narrative.evidence}")

    # Step 4: Plan slides with narrative
    print("\n📊 Planning slides...")
    slide_planner = SlidePlanner(api_key=api_key, model=model)
    slide_plan = slide_planner.plan_slides(analysis, narrative=narrative)

    # Step 5: Generate content
    print("✍️  Generating content...")
    content_gen = ContentGenerator(api_key=api_key, model=model)
    slides = content_gen.generate_content(slide_plan, narrative=narrative)

    # Step 6: Create PPT
    print("🎨 Creating presentation...")
    ppt_gen = PPTGenerator()
    ppt_gen.create_presentation(slides, "output/example_narrative.pptx")

    # Summary
    print("\n✅ COMPLETE!")
    print(f"Total cost: ${analyzer.total_cost + narrative_planner.total_cost:.4f}")
    print(f"Slides: {len(slides)}")
    print(f"Output: output/example_narrative.pptx")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Issue: Narrative fields are empty

**Cause**: LLM couldn't extract narrative from analysis

**Solution**: Check that analysis contains sufficient information:
```python
if not analysis.main_results:
    print("Warning: No main results found")
```

### Issue: Narrative is too long

**Cause**: LLM generated verbose responses

**Solution**: Adjust prompt to be more strict:
```python
# In prompt, add:
"Keep each field to 1-2 sentences maximum. Be concise."
```

### Issue: Narrative lacks specific numbers

**Cause**: Paper analysis didn't include numeric results

**Solution**: Ensure analysis extracts numbers:
```python
# Check analysis has numbers
if not any(char.isdigit() for char in str(analysis.main_results)):
    print("Warning: Analysis lacks numeric results")
```

---

## Future Enhancements

1. **Multiple Narrative Styles**
   - Academic narrative (current)
   - Business narrative (ROI-focused)
   - Tutorial narrative (learning-focused)

2. **Narrative Quality Scoring**
   - Automatically score narrative quality
   - Suggest improvements
   - Compare with successful narratives

3. **Narrative Templates**
   - Pre-defined narrative templates for different paper types
   - Domain-specific narrative structures

4. **Narrative Analytics**
   - Track which narratives resonate most
   - A/B test different narrative styles

---

**Last Updated**: 2026-03-13
**Status**: ✅ Ready for Integration
**Next Step**: Integrate with SlidePlanner
