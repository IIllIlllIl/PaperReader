# CLAUDE.md

## Project Overview

PaperReader generates academic presentation slides from PDF papers.

Pipeline: PDF → Parse → Analyze → Plan → Generate → Export

---

## Architecture

```
src/
  cli/           CLI implementation
  parser/        PDF parsing + figure extraction
  analysis/      AI analysis and content extraction
  planning/      slide planning
  generation/    markdown + PPTX generation
  core/          cache, pipeline orchestration
  prompts/       LLM prompts

outputs/
  slides/        PPTX files
  markdown/      slide markdown
  images/        extracted figures
  scripts/       presentation scripts
  plans/         slide plans (JSON)
```

---

## Key Modules

- **PDF parsing**: `src/parser/pdf_parser.py`
- **Figure extraction**: `src/parser/pdf_image_extractor.py`
- **Content extraction**: `src/analysis/content_extractor.py`
- **Slide planning**: `src/planning/slide_planner.py`
- **PPTX export**: `src/generation/pptx_exporter.py`

---

## Pipeline Features

### Structured Template (Default)

10-page academic presentation:
1. Title (1 page)
2. Problem Definition (2 pages)
3. Method (2 pages)
4. Experiments & Results (3 pages)
5. Discussion & Conclusions (2 pages)

### Intelligent Features

**Figure Matching** (100% accuracy):
- Fig.1 → Framework slides
- Fig.3 → Evaluation slides
- Fig.7 → Survey results
- Fig.9 → Discussion slides
- Rules: Title slides NO figures, Workflow slides NO survey results

**Content Extraction**:
- Auto-bold numbers: `**86%**`
- Comparison format: `**45%** vs **30%**`
- Pros/Cons: ✅ advantages, ❌ limitations

---

## Commands

```bash
# Basic pipeline (recommended)
python -m src.cli.main pipeline --paper papers/example.pdf

# Tests
pytest
```

Implementation note: use `python -m src.cli.main ...` for CLI commands.

---

## Development Rules

- ❌ No versioned files (`*_v2.py`, `*_enhanced.py`)
- ✅ Update existing modules
- ✅ Minimal code changes
- ✅ Small patches over rewrites
- Experimental code → `archive/experiments/`
