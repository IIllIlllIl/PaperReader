# Project Structure Reference

**Last Updated**: 2026-03-12
**Version**: V3 (Keyword-First)

This document defines the canonical structure for the PaperReader project to prevent directory entropy in LLM-assisted development.

---

## Directory Layout

```
paper-ppt-generator/
│
├── cli/                    # Command-line interface
│   └── main.py
│
├── papers/                 # Input PDF papers
│
├── src/                    # Core source code
│   ├── parser/            # PDF processing
│   ├── analysis/          # AI analysis
│   ├── generation/        # PPT generation
│   ├── core/              # Infrastructure
│   └── utils.py           # Utilities
│
├── prompts/               # LLM prompts
├── templates/             # Slide templates
│
├── runtime/               # Runtime data (git-ignored)
│   ├── cache/            # Analysis cache
│   └── logs/             # Application logs
│
├── outputs/               # Generated outputs (git-ignored)
│   ├── slides/           # PPTX files
│   ├── images/           # Extracted images
│   └── markdown/         # Intermediate Markdown
│
├── tests/                 # Test suite
│
└── archive/               # Legacy and experimental code
    ├── legacy/           # Old versions
    └── experiments/      # Experimental scripts
```

---

## Module Responsibilities

### Parser (`src/parser/`)

**Purpose**: Extract content from PDF papers

**Modules**:
- `pdf_parser.py` - Extract text, metadata, and structure
- `pdf_validator.py` - Validate PDF quality and layout
- `pdf_image_extractor.py` - Extract images and figures

**Input**: PDF file path
**Output**: Paper text, metadata, images

---

### Analysis (`src/analysis/`)

**Purpose**: Analyze paper content with AI

**Modules**:
- `ai_analyzer.py` - AI-powered paper analysis (V3 keyword-first)
- `content_extractor.py` - Extract and organize slide content (V3)

**Input**: Paper text, metadata
**Output**: Paper analysis, slide content structure

**Features**:
- Keyword-first approach (60 chars max)
- Table-based structured data
- Highlighted key breakthroughs
- 50% less text density

---

### Generation (`src/generation/`)

**Purpose**: Generate presentation slides

**Modules**:
- `ppt_generator.py` - Generate PPTX from content (V3)

**Input**: Organized slide content
**Output**: PPTX presentation

**Features**:
- Python-pptx based
- Support for tables
- Emoji support
- 30+ slides

---

### Core (`src/core/`)

**Purpose**: Infrastructure and utilities

**Modules**:
- `cache_manager.py` - Hash-based caching (MD5, 7-day TTL)
- `resilience.py` - Retry logic with exponential backoff
- `progress_reporter.py` - Progress bars and status reporting

---

## Data Flow

```
PDF Paper
    ↓
[Parser] → Extract text, metadata, images
    ↓
[Analysis] → AI analysis, content extraction
    ↓
[Generation] → Create PPTX slides
    ↓
Output Files (PPTX/HTML/PDF/Markdown)
```

---

## Import Conventions

### Standard Imports

```python
# Parser
from src.parser.pdf_parser import PDFParser
from src.parser.pdf_validator import PDFQuality

# Analysis
from src.analysis.ai_analyzer import AIAnalyzer
from src.analysis.content_extractor import ContentExtractor

# Generation
from src.generation.ppt_generator import PPTGenerator

# Core
from src.core.cache_manager import CacheManager
from src.core.resilience import ResilientAIAnalyzer, RetryConfig
from src.core.progress_reporter import get_reporter

# Utils
from src.utils import load_config, get_api_key, ensure_dir
```

### CLI Usage

```python
# Standard processing (16 slides)
python cli/main.py process --paper papers/example.pdf --format html

# With cache disabled
python cli/main.py process --paper papers/example.pdf --no-cache
```

---

## Configuration

**File**: `config.yaml`

```yaml
ai:
  model: claude-sonnet-4-6
  haiku_model: claude-haiku-4-5-20251001
  max_retries: 3

cache:
  cache_dir: runtime/cache/
  ttl: 604800  # 7 days

presentation:
  output_dir: outputs/
  template: templates/ppt_template.md
```

---

## File Naming Conventions

### Core Modules
- Use descriptive names: `pdf_parser.py`, `ai_analyzer.py`
- **NEVER** use version suffixes: ~~`v2.py`~~, ~~`v3.py`~~, ~~`enhanced.py`~~
- **NEVER** use optimization suffixes: ~~`optimized.py`~~, ~~`simple.py`~~

### Experimental Scripts
- Place in `archive/experiments/`
- Can use descriptive suffixes: `generate_v3_pptx.py`

### Legacy Code
- Place in `archive/legacy/`
- Rename to preserve version: `ai_analyzer_v1.py`

---

## Directory Entropy Prevention Rules

### ❌ What NOT to Do

```bash
# DON'T create versioned duplicates
src/ai_analyzer_v2.py          # ❌
src/ai_analyzer_enhanced.py    # ❌
src/ai_analyzer_optimized.py   # ❌

# DON'T create backup files in src/
src/parser.py.backup           # ❌

# DON'T commit runtime data
runtime/cache/*.json           # ❌
runtime/logs/*.log             # ❌
outputs/slides/*.pptx          # ❌

# DON'T create deep nesting
docs/project/architecture/v3/  # ❌
```

### ✅ What TO Do

```bash
# Update existing modules
src/analysis/ai_analyzer.py    # ✅ (update in place)

# Archive old versions
archive/legacy/ai_analyzer_v1.py  # ✅

# Git-ignore runtime data
runtime/  → .gitignore          # ✅
outputs/  → .gitignore          # ✅

# Keep docs flat
docs/architecture.md            # ✅
```

---

## Quick Reference

### Add a New Feature

1. Identify pipeline stage (parser/analysis/generation)
2. Add module to appropriate directory
3. Update imports in `cli/main.py`
4. Add tests in `tests/`
5. Update this file if structure changes

### Update AI Prompt

1. Edit `prompts/v3_prompt.py`
2. Test with `python cli/main.py process -p papers/test.pdf`
3. Validate output quality
4. Document changes in `docs/architecture/PROMPT_ENGINEERING_V3.md`

### Fix a Bug

1. Locate module in pipeline (parser/analysis/generation)
2. Update module in place (don't create `_fixed.py`)
3. Add test case
4. Run tests: `pytest tests/ -v`

### Archive Old Code

1. Move to `archive/legacy/` or `archive/experiments/`
2. Rename to preserve version info
3. Update imports (if still referenced)
4. Document in commit message

---

## Architecture Principles

### 1. Single Source of Truth
- One implementation per module
- No versioned duplicates
- Update in place, don't copy

### 2. Clear Pipeline Separation
- Parser: Extract from PDF
- Analysis: AI processing
- Generation: Create output
- Each stage is independent and testable

### 3. Minimal Root Directory
- Only essential config files
- No code in root
- Clean and navigable

### 4. Runtime Isolation
- Cache and logs in `runtime/`
- Outputs in `outputs/`
- Never commit to git

### 5. Archive, Don't Delete
- Old versions → `archive/legacy/`
- Experiments → `archive/experiments/`
- Preserve history for reference

---

## Migration from V2

If migrating from the old structure (v2/enhanced/optimized versions):

1. **Use V3 as canonical** - Keep `*_enhanced_v3.py` as base
2. **Rename to base module** - Remove version suffix
3. **Archive old versions** - Move to `archive/legacy/`
4. **Update imports** - See `MIGRATION_PLAN.md`
5. **Run tests** - Verify everything works

---

## Related Documentation

- **CLAUDE.md** - Claude Code instructions and repository rules
- **MIGRATION_PLAN.md** - Detailed migration steps
- **docs/architecture/PROMPT_ENGINEERING_V3.md** - V3 prompt guidelines
- **README.md** - Project overview and usage

---

**Maintained by**: Claude Code
**Review schedule**: Update when structure changes
**Feedback**: If Claude suggests creating versioned files, redirect to this document
