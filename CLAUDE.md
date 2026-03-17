# CLAUDE.md

## Project Overview

PaperReader generates academic presentation slides from PDF papers.

Pipeline:

PDF
→ parser
→ analysis
→ planning
→ generation
→ outputs (markdown / pptx)

Main goal:
produce academic slides with figures extracted from papers.

---

## Key Architecture

Source structure:

src/
parser/        PDF parsing + figure extraction
analysis/      AI analysis and slide content extraction
planning/      slide planning
generation/    markdown + PPTX generation
core/          cache, pipeline orchestration
prompts/       LLM prompts

Outputs:

outputs/images/
outputs/markdown/
outputs/slides/

---

## Important Modules

PDF parsing
src/parser/pdf_parser.py

Figure extraction
src/parser/pdf_image_extractor.py

Content extraction
src/analysis/content_extractor.py

Slide planning
src/planning/slide_planner.py

Markdown generation
src/generation/ppt_generator.py

PPTX export
src/generation/pptx_exporter.py

---

## Important Constraints

Do not create versioned files:

❌ *_v2.py
❌ *_enhanced.py
❌ *_optimized.py

Always update existing modules.

Experimental code goes to:

archive/experiments/

---

## Figure Pipeline

Figures are extracted during parsing and saved to:

outputs/images/

Slides reference figures via Markdown syntax:

![caption](path)

pptx_exporter.py parses this and renders images in PPTX.

---

## Common Commands

Generate enhanced presentation:

python tools/generate_enhanced_pptx.py papers/example.pdf

Run tests:

pytest

---

## Development Rules

Follow existing pipeline architecture.

Avoid large refactors unless explicitly requested.

Modify minimal code when fixing bugs.

Prefer small patches over full rewrites.
