# PaperReader Best Practices Guide

This guide describes the current recommended workflow for generating academic presentation slides with PaperReader.

---

## Quick Start

Use the end-to-end pipeline:

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf
```

Common variants:

```bash
# Preserve intermediate files for inspection and debugging
python cli/main.py pipeline --paper papers/your-paper.pdf --no-clean

# Include citation analysis
python cli/main.py pipeline --paper papers/your-paper.pdf --include-citations
```

What the current pipeline produces:
- Final deliverable: `outputs/slides/{paper_name}.pptx`
- Optional intermediate artifacts: `outputs/intermediates/`
- Default structure: a structured 10-slide presentation template

---

## Current Output Structure

When the run succeeds, the main deliverable is:

```text
outputs/
└── slides/
    └── {paper_name}.pptx
```

When you use `--no-clean`, PaperReader also keeps intermediate artifacts:

```text
outputs/
├── slides/
│   └── {paper_name}.pptx
└── intermediates/
    ├── markdown/
    │   └── {paper_name}.md
    ├── plans/
    │   └── {paper_name}_plan.json
    ├── scripts/
    │   └── {paper_name}_presentation_script.md
    ├── images/
    └── citations/
```

Notes:
- `outputs/slides/` is the final output location.
- `outputs/intermediates/` is for inspection, debugging, and review.
- By default, intermediate files are cleaned automatically after a successful run.

---

## Recommended Workflow

### 1. Generate the presentation

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf
```

### 2. Review the final PPTX

```bash
open outputs/slides/your-paper.pptx
```

### 3. Re-run with intermediates when you need to inspect the pipeline

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf --no-clean
```

Then check, in order:
1. `outputs/intermediates/plans/`
2. `outputs/intermediates/markdown/`
3. `outputs/intermediates/scripts/`
4. `outputs/slides/`

---

## Current Pipeline Stages

`src/core/pipeline.py` currently coordinates these stages:

1. Parse PDF
2. Extract structured sections
3. Run AI analysis
4. Optional citation analysis
5. Generate slide plan
6. Generate narrative
7. Generate slides markdown
8. Export PPTX
9. Generate presentation script

Implementation logs may show citation analysis as stage `3.5`.

---

## Default Presentation Structure

`src/planning/slide_planner.py` currently defaults to a structured 10-slide template:

1. Title
2. Why Human-in-the-Loop?
3. Research Questions
4. HULA Framework Overview
5. Workflow: Human Feedback Integration
6. Three-Stage Evaluation
7. Offline & Online Results
8. User Survey Results
9. Discussion: Pros & Cons
10. Conclusions & Future Work

If citation data is available, extra citation-related slides may be inserted around the discussion section.

---

## Citation Analysis

Enable citation analysis when you want the generated presentation to include source-backed citation content:

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf --include-citations
```

Optional tuning:

```bash
python cli/main.py pipeline \
  --paper papers/your-paper.pdf \
  --include-citations \
  --citation-min-sources 3 \
  --citation-limit 30
```

---

## Cache and Maintenance Commands

```bash
# Show cache statistics
python cli/main.py stats

# Remove expired cache files
python cli/main.py cleanup

# Clear all cached analyses
python cli/main.py clear-cache
```

---

## Troubleshooting

### Need to inspect generated content

Run with `--no-clean`, then inspect:

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf --no-clean
```

Key locations:
- Slide plan: `outputs/intermediates/plans/{paper_name}_plan.json`
- Slides markdown: `outputs/intermediates/markdown/{paper_name}.md`
- Presentation script: `outputs/intermediates/scripts/{paper_name}_presentation_script.md`
- Extracted figures: `outputs/intermediates/images/`

### Need to re-run analysis from scratch

```bash
python cli/main.py clear-cache
python cli/main.py pipeline --paper papers/your-paper.pdf --verbose
```

### Need more debugging details

```bash
python cli/main.py pipeline --paper papers/your-paper.pdf --verbose --no-clean
```

---

## Best Practices

- Use `pipeline` as the default entrypoint for presentation generation.
- Treat `.pptx` as the primary deliverable.
- Use `--no-clean` only when you need to inspect intermediate artifacts.
- Treat `outputs/intermediates/` as a debugging area, not the final deliverable.
- If documentation and behavior differ, trust `cli/main.py`, `src/core/pipeline.py`, and `src/planning/slide_planner.py`.

---

## Related Documents

- `README.md`
- `docs/user-guide/ENHANCED_PPTX_GUIDE.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/PIPELINE_IMPLEMENTATION.md`
- `docs/architecture/SLIDE_PLANNING_LAYER.md`
