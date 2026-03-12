# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PaperReader** is an AI-powered academic paper reading and presentation generation tool. It automatically analyzes PDF papers and generates professional academic-style presentation slides.

**Core Workflow**: PDF Input → Text Extraction → AI Analysis → Content Organization → Slide Generation → Output (Markdown/HTML/PDF/PPTX)

**Version**: 0.3.0 (V3 with keyword-first approach)

---

## Technology Stack

- **Language**: Python 3.8+
- **PDF Processing**: PyMuPDF (fitz), PyPDF2
- **AI Integration**: Anthropic Claude API (claude-sonnet-4-6, claude-haiku-4-5-20251001)
- **Presentation**: Marp CLI (Markdown to slides), python-pptx (PPTX generation)
- **CLI**: Click
- **Progress UI**: Rich
- **Configuration**: PyYAML

---

## Quick Start

### Enhanced Version (30+ slides, ~$0.11) - **Recommended**
```bash
python tools/generate_enhanced_pptx.py papers/example.pdf
```

### Standard Version (16 slides, ~$0.06)
```bash
python cli/main.py process --paper papers/example.pdf --format html
```

---

## AI Prompt Engineering

### V3 Guidelines (Latest) - **MUST READ**

**Document**: `docs/architecture/PROMPT_ENGINEERING_V3.md`

#### Core Principles

1. **Keyword-First Approach**
   - Use keywords instead of full sentences
   - Maximum 1-2 sentences per bullet point
   - Maximum 60 characters per point
   - Focus on key information only

2. **Table-Based Structured Data**
   - Use Markdown tables for experimental setup
   - Use tables for dataset descriptions
   - Use tables for baseline comparisons
   - Use tables for metric results

3. **Highlight Key Breakthroughs**
   - Identify 3-5 key breakthroughs per paper
   - Use emoji (🔥) to mark breakthroughs
   - Bold key numbers and findings (**27%**)
   - Create separate breakthrough section

4. **Reduce Text Density**
   - Target: 50% less text vs V2
   - Maximum 5-6 bullet points per slide
   - Use visual hierarchy (tables, lists, emoji)

#### Quality Metrics

| Metric | V2 | V3 | Improvement |
|--------|----|----|-------------|
| Text per slide | 120+ words | **60 words** | -50% ✨ |
| Format | Text lists | **Tables** | Clearer ✨ |
| Keywords | None | **All content** | Focused ✨ |
| Breakthroughs | Scattered | **Highlighted** | Prominent ✨ |

---

### Prompt Structure V3

```json
{
  "key_breakthroughs": [
    "Breakthrough 1: Brief description with specific number",
    "Breakthrough 2: Brief description with specific number"
  ],
  
  "experimental_setup": {
    "datasets": "Name (size)",
    "baselines": ["Method1", "Method2"],
    "metrics": ["Metric1", "Metric2"],
    "environment": "Setup details",
    "tasks": "Number and type"
  },
  
  "main_results": [
    "Result 1: 27% improvement over baseline",
    "Result 2: 89% user acceptance",
    "Result 3: 52% error reduction"
  ]
}
```

**CRITICAL**:
- Extract 6 items maximum per field
- Use numbers for all quantitative results
- Bold key findings with **text**
- Keep descriptions under 60 characters

---

### V2 vs V3 Comparison

#### Experimental Setup Page

**V2 (Too Verbose)**:
```markdown
## Experimental Setup

- We evaluated our system on SWE-bench, a benchmark dataset 
  containing 2,294 GitHub issues from popular open-source 
  repositories...
- The baselines included SWE-agent, which operates on a Linux 
  shell to search and edit code...
(150+ words, hard to scan)
```

**V3 (Concise)**:
```markdown
## Experimental Setup

| Item | Content |
|------|---------|
| **Datasets** | SWE-bench (2,294 issues) |
| **Baselines** | SWE-agent, AutoCodeRover |
| **Metrics** | Resolution Rate, Time Cost |
| **Tasks** | 64 real tasks |

(50 words, easy to scan)
```

---

## Output Formats

### 1. Markdown (Marp format)
- Standard: `output/markdown/[PaperName].md`
- Enhanced: `output/markdown/[PaperName]_enhanced.md`

### 2. HTML
- Requires Marp CLI
- Fallback to standalone HTML

### 3. PDF
- Requires Marp CLI

### 4. PPTX
- Standard: 16 slides, 46KB
- Enhanced: 30 slides, 69KB
- Uses python-pptx library
- Supports tables and emoji

---

## Module Structure

```
src/
├── pdf_parser.py              # PDF text extraction
├── pdf_validator.py           # PDF quality validation
├── ai_analyzer.py             # Standard AI analyzer
├── ai_analyzer_enhanced.py    # Enhanced AI analyzer (V3 prompt)
├── content_extractor.py       # Standard content organizer
├── content_extractor_enhanced.py # Enhanced organizer (V3 keywords)
├── ppt_generator.py           # Standard PPT generator
├── ppt_generator_enhanced.py  # Enhanced generator (V3 tables)
├── cache_manager.py           # Analysis caching
├── resilience.py              # Retry logic
├── progress_reporter.py       # Progress bars
└── utils.py                   # Utilities
```

---

## Common Commands

### Process Papers

```bash
# Enhanced version (detailed presentation) - RECOMMENDED
python tools/generate_enhanced_pptx.py papers/example.pdf

# Standard version (quick overview)
python cli/main.py process --paper papers/example.pdf --format html

# Process all papers
python cli/main.py process --all --format html

# With options
python cli/main.py process -p papers/example.pdf -f pptx --verbose
```

### Cache Management

```bash
python cli/main.py stats
python cli/main.py clear-cache
python cli/main.py cleanup
```

---

## Development Workflow

1. **Add new feature**: Create module in `src/`
2. **Update prompt**: Follow V3 guidelines
3. **Add tests**: Create `tests/test_*.py`
4. **Update config**: Add configuration options if needed
5. **Update docs**: Update `docs/architecture/PROMPT_ENGINEERING_V3.md`

---

## Key Design Decisions

### 1. V3 Keyword-First Approach
- Use keywords instead of full sentences
- Maximum 60 characters per point
- 50% less text density
- Better for presentations

### 2. Table-Based Data
- Experimental setup → table
- Dataset descriptions → table
- Results comparison → table
- Easier to scan and compare

### 3. Highlight Key Breakthroughs
- Separate slide for key breakthroughs
- Use 🔥 emoji to mark breakthroughs
- Bold key numbers (**27%**)
- Make innovations stand out

### 4. Hash-Based Caching
- Uses MD5 hash of PDF file
- Avoids redundant API calls (50-70% cost savings)
- 7-day TTL by default

### 5. Modular Architecture
- Clear separation of concerns
- Each module has single responsibility
- Easy to test and maintain

---

## Performance Metrics

### Enhanced Version (V3)
- Slides: **30**
- Markdown size: **~26KB**
- PPTX size: **~69KB**
- Cost: **~$0.11**
- Time: ~2 minutes
- Text per slide: **60 words** (-50% vs V2)

---

## Important Files

### Source Code
- `src/ai_analyzer_enhanced.py` - Enhanced AI analyzer with V3 prompt
- `src/content_extractor_enhanced.py` - Enhanced content extractor with keywords
- `src/ppt_generator_enhanced.py` - Enhanced PPT generator with tables

### Tools
- `tools/generate_enhanced_pptx.py` - One-click enhanced generation
- `tools/md_to_pptx.py` - Markdown to PPTX converter

### Documentation
- `docs/architecture/PROMPT_ENGINEERING_V3.md` - **V3 Guidelines (MUST READ)**
- `docs/testing/enhanced_pptx_comparison.md` - Comparison report
- `docs/user-guide/ENHANCED_PPTX_GUIDE.md` - User guide

---

## Recommendations

### For Academic Presentation (30-45 min)
Use enhanced version - **HIGHLY RECOMMENDED**:
```bash
python tools/generate_enhanced_pptx.py papers/example.pdf
```

The enhanced version provides:
- ✅ 2x more slides (30 vs 16)
- ✅ 3x more content (26KB vs 8.7KB)
- ✅ Keywords instead of full sentences
- ✅ Tables for structured data
- ✅ Highlighted key breakthroughs
- ✅ 50% less text density
- ✅ Only 85% more cost ($0.11 vs $0.06)

---

## Repository Structure Rules

**CRITICAL**: These rules prevent directory entropy in LLM-assisted development.

### 1. No Versioned Files

**❌ NEVER create**:
- `*_v2.py`, `*_v3.py`, `*_v4.py`
- `*_enhanced.py`, `*_improved.py`
- `*_optimized.py`, `*_simple.py`
- `*_prototype.py` (in src/)

**✅ ALWAYS**:
- Update existing modules in place
- If breaking change needed, archive old version first
- One canonical implementation per module

### 2. Module Organization

Follow **pipeline architecture**:

```
src/parser/       → PDF processing (pdf_parser, pdf_validator, pdf_image_extractor)
src/analysis/     → AI analysis (ai_analyzer, content_extractor)
src/generation/   → PPT generation (ppt_generator)
src/core/         → Infrastructure (cache_manager, resilience, progress_reporter)
```

**Rules**:
- Parser modules → `src/parser/`
- Analysis modules → `src/analysis/`
- Generation modules → `src/generation/`
- Core infrastructure → `src/core/`

### 3. Experimental Code

**All experiments and prototypes**:
```bash
archive/experiments/
```

**Rules**:
- Experimental scripts → `archive/experiments/`
- One-off scripts → `archive/experiments/`
- Prototypes → `archive/experiments/`
- Never in `tools/` or `src/`

### 4. Legacy Code

**Old versions and deprecated code**:
```bash
archive/legacy/
```

**Rules**:
- Old versions → `archive/legacy/`
- Rename to preserve version: `module_v1.py`
- Keep for reference, don't update
- Never delete (archive instead)

### 5. Runtime Data

**Cache and logs**:
```bash
runtime/cache/
runtime/logs/
```

**Rules**:
- Cache → `runtime/cache/`
- Logs → `runtime/logs/`
- **NEVER commit to git**
- Add to `.gitignore`

### 6. Outputs

**Generated files**:
```bash
outputs/slides/
outputs/images/
outputs/markdown/
```

**Rules**:
- Generated slides → `outputs/slides/`
- Extracted images → `outputs/images/`
- Intermediate markdown → `outputs/markdown/`
- **NEVER commit to git**
- Add to `.gitignore`

### 7. Documentation

**Keep minimal**:
```bash
docs/
  architecture.md
  user-guide.md
  testing.md
```

**Rules**:
- Flat structure (max 2 levels)
- Archive old docs → `archive/docs/`
- Consolidate multiple files into one

### 8. Root Directory

**Only essential files**:
```
README.md
CLAUDE.md
PROJECT_STRUCTURE.md
config.yaml
requirements.txt
```

**Rules**:
- No code in root
- No backup files
- No temporary files
- Keep clean and navigable

### 9. Import Conventions

**Standard imports**:
```python
from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer import AIAnalyzer
from src.generation.ppt_generator import PPTGenerator
from src.core.cache_manager import CacheManager
```

**Never import from**:
- ❌ `src.ai_analyzer_v3`
- ❌ `src.ai_analyzer_enhanced`
- ❌ `src.ppt_generator_optimized`

### 10. When in Doubt

**Reference**:
- `PROJECT_STRUCTURE.md` - Architecture reference
- `MIGRATION_PLAN.md` - Migration details

**Ask**:
- "Where should this file go?"
- "Should I create a new version or update existing?"
- "Is this experimental or production?"

---

## Code Conventions

- Follow PEP 8 style
- Use dataclasses for structured data
- Type hints for function signatures
- Docstrings for public methods
- Logging instead of print statements
- Exceptions for error conditions
- Follow V3 prompt guidelines

---

## Dependencies Management

Core dependencies in `requirements.txt`:
- Keep versions pinned for reproducibility
- Separate dev dependencies (testing, linting)
- Document Node.js dependencies (Marp) separately
- python-pptx for PPTX generation

---

**Last Updated**: 2026-03-12
**Version**: 0.3.0 (V3 with keyword-first approach)
**Structure**: Pipeline Architecture (parser/analysis/generation)
