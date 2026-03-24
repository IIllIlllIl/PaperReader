# Manual Test Scripts

This directory contains manual test scripts for testing and demonstrating specific features of PaperReader.

## ⚠️ Important Note

These are **standalone test scripts** used for manual verification and demonstration purposes. They are not part of the automated test suite (which is in `tests/`).

For automated unit tests, see: `tests/`

## Available Scripts

### Feature Tests

- **`test_slide_formatter.py`** (7.6K) - Test slide formatting rules and validation
- **`test_slide_planner.py`** (4.2K) - Test slide planning logic
- **`test_narrative_planner.py`** (3.8K) - Test narrative extraction pipeline
- **`test_chart_generation.py`** (4.5K) - Test chart generation functionality

### Meeting Mode Tests

- **`test_research_meeting.py`** (3.7K) - Test research meeting presentation mode
- **`test_phd_meeting_v2.py`** (6.6K) - Test PhD meeting presentation mode V2

## Usage

Run any script directly from the project root:

```bash
# Test slide formatting
python tools/manual_tests/test_slide_formatter.py

# Test narrative planner
python tools/manual_tests/test_narrative_planner.py

# Test PhD meeting mode
python tools/manual_tests/test_phd_meeting_v2.py
```

## Script Details

### test_slide_formatter.py
Tests the `SlideFormatter` class:
- Basic bullet formatting
- Slide type detection
- Content limits enforcement
- Strict mode validation

### test_narrative_planner.py
Tests the narrative extraction pipeline:
1. Parse PDF
2. Analyze paper with AI
3. Extract narrative structure
4. Display results

### test_chart_generation.py
Tests chart generation from data:
- Chart type selection
- Data visualization
- PPTX integration

### test_slide_planner.py
Tests slide planning logic:
- Section extraction
- Slide type assignment
- Content organization

### test_research_meeting.py
Tests research meeting mode:
- Content extraction for meetings
- Slide generation
- Output verification

### test_phd_meeting_v2.py
Tests PhD meeting mode V2:
- Enhanced content extraction
- V2-specific features
- Full pipeline test

## Related Documentation

- [Pipeline Implementation](../../docs/architecture/PIPELINE_IMPLEMENTATION.md)
- [Slide Formatter Guide](../../docs/features/SLIDE_FORMATTER.md)
- [Narrative Planner Guide](../../docs/features/NARRATIVE_PLANNER.md)

## Moving to Automated Tests

If you want to convert these manual tests to automated pytest tests:

1. Create corresponding test file in `tests/`
2. Use pytest fixtures and assertions
3. Add to CI/CD pipeline
4. Remove from `tools/manual_tests/`

---

**Last Updated**: 2026-03-17
**Maintained by**: Development Team
