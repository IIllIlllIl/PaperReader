# Repository Refactoring Migration Plan

**Date**: 2026-03-12
**Version**: V3 (Keyword-First) Consolidation
**Status**: DRAFT - Review Required Before Execution

---

## Executive Summary

This migration plan consolidates duplicate version files (v2, v3, enhanced, optimized) into a single canonical implementation per module, following the **parser/analysis/generation** pipeline architecture.

**Goals**:
- ✅ Remove version fragmentation
- ✅ Establish clear pipeline structure
- ✅ Prevent future directory entropy
- ✅ Reduce from ~40 files to ~20 core files

---

## 1. Proposed New Directory Tree

```
paper-ppt-generator/
│
├── README.md
├── CLAUDE.md
├── PROJECT_STRUCTURE.md          # NEW: Architecture reference
├── config.yaml
├── requirements.txt
│
├── cli/
│   └── main.py
│
├── papers/
│
├── src/
│   ├── __init__.py
│   │
│   ├── parser/                    # NEW: PDF processing
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   ├── pdf_validator.py
│   │   └── pdf_image_extractor.py
│   │
│   ├── analysis/                  # NEW: AI analysis
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py
│   │   └── content_extractor.py
│   │
│   ├── generation/                # NEW: PPT generation
│   │   ├── __init__.py
│   │   └── ppt_generator.py
│   │
│   ├── core/                      # NEW: Infrastructure
│   │   ├── __init__.py
│   │   ├── cache_manager.py
│   │   ├── resilience.py
│   │   └── progress_reporter.py
│   │
│   └── utils.py
│
├── prompts/
│   └── v3_prompt.py
│
├── templates/
│   └── ppt_template.md
│
├── runtime/                       # NEW: Runtime data
│   ├── cache/
│   └── logs/
│
├── outputs/                       # RENAMED: output → outputs
│   ├── slides/
│   ├── images/
│   └── markdown/
│
├── tests/
│   ├── test_pdf_parser.py
│   ├── test_ai_analyzer.py
│   ├── test_content_extractor.py
│   ├── test_ppt_generator.py
│   └── test_cache_manager.py
│
└── archive/                       # NEW: Legacy/Experimental code
    ├── legacy/
    │   ├── ai_analyzer_v1.py
    │   ├── content_extractor_enhanced.py
    │   └── ppt_generator_enhanced.py
    │
    └── experiments/
        ├── generate_v3_pptx.py
        ├── generate_v3_pptx_simple.py
        ├── generate_v3_pptx_optimized.py
        ├── md_to_pptx_prototype.py
        └── debug_data_flow.py
```

**Key Changes**:
- ✅ **src/** organized by pipeline: parser/analysis/generation
- ✅ **runtime/** for cache and logs
- ✅ **archive/** for legacy and experimental code
- ✅ No more `v2/v3/enhanced/optimized` duplicates

---

## 2. File Migration Table

### 2.1 Core Modules → Canonical Names (V3 as Base)

| Current Path | New Path | Action |
|-------------|----------|--------|
| `src/ai_analyzer_enhanced_v3.py` | `src/analysis/ai_analyzer.py` | **MOVE & RENAME** (V3 → canonical) |
| `src/content_extractor_enhanced_v3.py` | `src/analysis/content_extractor.py` | **MOVE & RENAME** (V3 → canonical) |
| `src/ppt_generator_enhanced_v3.py` | `src/generation/ppt_generator.py` | **MOVE & RENAME** (V3 → canonical) |
| `src/pdf_parser.py` | `src/parser/pdf_parser.py` | **MOVE** |
| `src/pdf_validator.py` | `src/parser/pdf_validator.py` | **MOVE** |
| `src/pdf_image_extractor.py` | `src/parser/pdf_image_extractor.py` | **MOVE** |
| `src/cache_manager.py` | `src/core/cache_manager.py` | **MOVE** |
| `src/resilience.py` | `src/core/resilience.py` | **MOVE** |
| `src/progress_reporter.py` | `src/core/progress_reporter.py` | **MOVE** |
| `src/utils.py` | `src/utils.py` | **KEEP** (no change) |
| `src/prompts/v3_prompt.py` | `prompts/v3_prompt.py` | **MOVE** |

### 2.2 Legacy Versions → Archive

| Current Path | Archive Path | Reason |
|-------------|--------------|--------|
| `src/ai_analyzer.py` | `archive/legacy/ai_analyzer_v1.py` | Original version |
| `src/ai_analyzer_enhanced.py` | `archive/legacy/ai_analyzer_enhanced.py` | V2 version |
| `src/content_extractor.py` | `archive/legacy/content_extractor_v1.py` | Original version |
| `src/content_extractor_enhanced.py` | `archive/legacy/content_extractor_enhanced.py` | V2 version |
| `src/ppt_generator.py` | `archive/legacy/ppt_generator_v1.py` | Original version |
| `src/ppt_generator_enhanced.py` | `archive/legacy/ppt_generator_enhanced.py` | V2 version |

### 2.3 Tools → Archive/Experiments

| Current Path | Archive Path | Reason |
|-------------|--------------|--------|
| `tools/generate_v3_pptx.py` | `archive/experiments/generate_v3_pptx.py` | Experiment |
| `tools/generate_v3_pptx_simple.py` | `archive/experiments/generate_v3_pptx_simple.py` | Experiment |
| `tools/generate_v3_pptx_optimized.py` | `archive/experiments/generate_v3_pptx_optimized.py` | Experiment |
| `tools/generate_enhanced_pptx.py` | `archive/experiments/generate_enhanced_pptx.py` | Experiment |
| `tools/md_to_pptx_prototype.py` | `archive/experiments/md_to_pptx_prototype.py` | Prototype |

### 2.4 Runtime Data Reorganization

| Current Path | New Path | Action |
|-------------|----------|--------|
| `cache/` | `runtime/cache/` | **MOVE** |
| `logs/` | `runtime/logs/` | **MOVE** |
| `output/` | `outputs/` | **RENAME** |

### 2.5 Documentation Consolidation

| Current Path | New Path | Action |
|-------------|----------|--------|
| `docs/architecture/` | `docs/architecture.md` | **CONSOLIDATE** |
| `docs/user-guide/` | `docs/user-guide.md` | **CONSOLIDATE** |
| `docs/testing/` | `docs/testing.md` | **CONSOLIDATE** |
| `docs/archived/` | `archive/docs/` | **MOVE** |

---

## 3. Files Safe to Delete

**After migration, these files can be safely deleted** (already archived):

### 3.1 Duplicate Version Files (moved to archive/)

```bash
# Will be in archive/legacy/
src/ai_analyzer.py
src/ai_analyzer_enhanced.py
src/content_extractor.py
src/content_extractor_enhanced.py
src/ppt_generator.py
src/ppt_generator_enhanced.py

# Will be in archive/experiments/
tools/generate_enhanced_pptx.py
tools/generate_v3_pptx.py
tools/generate_v3_pptx_simple.py
tools/generate_v3_pptx_optimized.py
tools/md_to_pptx_prototype.py
```

### 3.2 Generated Files (can be regenerated)

```bash
output/slides/*.pptx      # Will be regenerated
output/images/*.png       # Will be regenerated
output/markdown/*.md      # Will be regenerated
```

### 3.3 Temporary/Backup Files

```bash
*.backup
*.pyc
__pycache__/
.DS_Store
cli/main.py.backup
```

**⚠️ IMPORTANT**: Do NOT delete until migration is complete and tests pass.

---

## 4. Import Updates Required

### 4.1 CLI (cli/main.py)

**Current imports**:
```python
from src.utils import ...
from src.pdf_parser import PDFParser
from src.pdf_validator import PDFQuality
from src.ai_analyzer import AIAnalyzer
from src.content_extractor import ContentExtractor
from src.ppt_generator import PPTGenerator
from src.cache_manager import CacheManager
from src.resilience import ResilientAIAnalyzer, RetryConfig
from src.progress_reporter import get_reporter
```

**New imports** (after migration):
```python
from src.utils import ...
from src.parser.pdf_parser import PDFParser
from src.parser.pdf_validator import PDFQuality
from src.analysis.ai_analyzer import AIAnalyzer
from src.analysis.content_extractor import ContentExtractor
from src.generation.ppt_generator import PPTGenerator
from src.core.cache_manager import CacheManager
from src.core.resilience import ResilientAIAnalyzer, RetryConfig
from src.core.progress_reporter import get_reporter
```

**Changes**:
- `src.pdf_parser` → `src.parser.pdf_parser`
- `src.ai_analyzer` → `src.analysis.ai_analyzer`
- `src.content_extractor` → `src.analysis.content_extractor`
- `src.ppt_generator` → `src.generation.ppt_generator`
- `src.cache_manager` → `src.core.cache_manager`
- `src.resilience` → `src.core.resilience`
- `src.progress_reporter` → `src.core.progress_reporter`

### 4.2 Tests (tests/test_*.py)

All test files need import updates:

```python
# Before
from src.pdf_parser import PDFParser
from src.ai_analyzer import AIAnalyzer
from src.content_extractor import ContentExtractor
from src.ppt_generator import PPTGenerator
from src.cache_manager import CacheManager

# After
from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer import AIAnalyzer
from src.analysis.content_extractor import ContentExtractor
from src.generation.ppt_generator import PPTGenerator
from src.core.cache_manager import CacheManager
```

### 4.3 Archived Experiments

Files in `archive/experiments/` will have broken imports but **that's acceptable** - they are archived for reference only.

---

## 5. Potential Breaking Changes

### 5.1 Import Paths (HIGH IMPACT)

**Affected components**:
- ✅ `cli/main.py` - **MUST UPDATE**
- ✅ `tests/test_*.py` - **MUST UPDATE**
- ❌ `archive/experiments/` - **DO NOT UPDATE** (archived)

**Risk**: If imports are not updated correctly, CLI and tests will fail.

**Mitigation**:
1. Update all imports before moving files
2. Run tests after each module migration
3. Keep a rollback script ready

### 5.2 Config File Paths (MEDIUM IMPACT)

**Current**:
```yaml
cache:
  cache_dir: cache/
presentation:
  output_dir: output/
```

**New**:
```yaml
cache:
  cache_dir: runtime/cache/
presentation:
  output_dir: outputs/
```

**Risk**: Old config files will point to wrong directories.

**Mitigation**:
1. Update `config.yaml`
2. Create compatibility wrapper for old paths

### 5.3 Prompt Paths (LOW IMPACT)

**Current**: `src/prompts/v3_prompt.py`
**New**: `prompts/v3_prompt.py`

**Risk**: Minimal - only used internally.

**Mitigation**: Update import in `ai_analyzer.py` after move.

---

## 6. Execution Steps

### Phase 1: Preparation (NO FILE CHANGES YET)

1. ✅ **Create directory structure** (empty directories)
   ```bash
   mkdir -p src/parser src/analysis src/generation src/core
   mkdir -p runtime/cache runtime/logs
   mkdir -p archive/legacy archive/experiments archive/docs
   mkdir -p outputs/slides outputs/images outputs/markdown
   ```

2. ✅ **Create `__init__.py` files**
   ```bash
   touch src/parser/__init__.py
   touch src/analysis/__init__.py
   touch src/generation/__init__.py
   touch src/core/__init__.py
   ```

3. ✅ **Backup current state**
   ```bash
   git add -A
   git commit -m "chore: backup before repository restructure"
   git tag pre-refactor-backup
   ```

### Phase 2: Migrate Core Modules (ORDER MATTERS)

**Step 2.1**: Move V3 modules to canonical locations

```bash
# Parser modules
git mv src/pdf_parser.py src/parser/
git mv src/pdf_validator.py src/parser/
git mv src/pdf_image_extractor.py src/parser/

# Analysis modules (V3 → canonical)
git mv src/ai_analyzer_enhanced_v3.py src/analysis/ai_analyzer.py
git mv src/content_extractor_enhanced_v3.py src/analysis/content_extractor.py

# Generation modules (V3 → canonical)
git mv src/ppt_generator_enhanced_v3.py src/generation/ppt_generator.py

# Core modules
git mv src/cache_manager.py src/core/
git mv src/resilience.py src/core/
git mv src/progress_reporter.py src/core/

# Prompts
git mv src/prompts prompts/
```

**Step 2.2**: Archive legacy versions

```bash
# Archive old analyzer versions
git mv src/ai_analyzer.py archive/legacy/ai_analyzer_v1.py
git mv src/ai_analyzer_enhanced.py archive/legacy/

# Archive old content extractor versions
git mv src/content_extractor.py archive/legacy/content_extractor_v1.py
git mv src/content_extractor_enhanced.py archive/legacy/

# Archive old generator versions
git mv src/ppt_generator.py archive/legacy/ppt_generator_v1.py
git mv src/ppt_generator_enhanced.py archive/legacy/
```

**Step 2.3**: Archive experiments

```bash
git mv tools/generate_*.py archive/experiments/
git mv tools/md_to_pptx_prototype.py archive/experiments/
git mv tools/md_to_pptx.py archive/experiments/  # if not needed
```

**Step 2.4**: Reorganize runtime

```bash
git mv cache/* runtime/cache/ 2>/dev/null || true
git mv logs/* runtime/logs/ 2>/dev/null || true
rmdir cache logs 2>/dev/null || true

git mv output outputs
```

**Step 2.5**: Consolidate docs

```bash
# Move archived docs
git mv docs/archived archive/docs

# Keep only essential docs in docs/
# (Manual consolidation required)
```

### Phase 3: Update Imports (CRITICAL)

**Step 3.1**: Update `cli/main.py`

```bash
# Use sed or manual edit to update imports
# See Section 4.1 for exact changes
```

**Step 3.2**: Update all test files

```bash
# Update tests/test_*.py
# See Section 4.2 for exact changes
```

**Step 3.3**: Update internal imports

Update imports within moved modules:
- `ai_analyzer.py` imports from `content_extractor`
- `ppt_generator.py` imports from templates
- etc.

### Phase 4: Update Configuration

**Step 4.1**: Update `config.yaml`

```yaml
cache:
  cache_dir: runtime/cache/

presentation:
  output_dir: outputs/
  template: templates/ppt_template.md
```

**Step 4.2**: Update `CLAUDE.md`

Add repository rules (see Section 8).

**Step 4.3**: Create `PROJECT_STRUCTURE.md` (see Section 7).

### Phase 5: Testing

**Step 5.1**: Run all tests

```bash
python -m pytest tests/ -v
```

**Step 5.2**: Test CLI

```bash
python cli/main.py process --paper papers/example.pdf --format html
```

**Step 5.3**: Verify imports

```bash
python -c "
from src.analysis.ai_analyzer import AIAnalyzer
from src.generation.ppt_generator import PPTGenerator
print('✅ Imports work!')
"
```

### Phase 6: Cleanup

**Step 6.1**: Remove empty directories

```bash
rmdir src/prompts 2>/dev/null || true
rmdir tools 2>/dev/null || true
```

**Step 6.2**: Update `.gitignore`

```gitignore
# Runtime data
runtime/cache/
runtime/logs/

# Outputs
outputs/slides/*.pptx
outputs/images/*.png
outputs/markdown/*.md

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
```

**Step 6.3**: Commit migration

```bash
git add -A
git commit -m "refactor: consolidate to V3 pipeline architecture

- Remove version fragmentation (v1/v2/v3/enhanced)
- Organize by pipeline: parser/analysis/generation
- Move runtime data to runtime/
- Archive legacy and experimental code
- Update all imports and tests

BREAKING CHANGE: Import paths changed
"
```

---

## 7. PROJECT_STRUCTURE.md (New File)

```markdown
# Project Structure Reference

This document defines the canonical structure for the PaperReader project.

## Directory Layout

```
src/parser        → PDF processing (pdf_parser, pdf_validator, pdf_image_extractor)
src/analysis      → AI analysis (ai_analyzer, content_extractor)
src/generation    → PPT generation (ppt_generator)
src/core          → Infrastructure (cache_manager, resilience, progress_reporter)
templates         → Slide templates
prompts           → LLM prompts
papers            → Input papers
outputs           → Generated slides
runtime           → Logs and cache
archive           → Legacy and experimental code
```

## Module Responsibilities

- **parser**: Extract text, images, and metadata from PDFs
- **analysis**: Analyze paper content with AI, extract slide content
- **generation**: Generate PPTX presentations
- **core**: Caching, retry logic, progress reporting

## Import Conventions

```python
from src.parser.pdf_parser import PDFParser
from src.analysis.ai_analyzer import AIAnalyzer
from src.generation.ppt_generator import PPTGenerator
from src.core.cache_manager import CacheManager
```
```

---

## 8. CLAUDE.md Updates (Repository Rules)

Add this section to `CLAUDE.md`:

```markdown
## Repository Structure Rules

**CRITICAL**: These rules prevent directory entropy in LLM collaboration.

1. **No Versioned Files**
   - ❌ Never create: `*_v2.py`, `*_v3.py`, `*_enhanced.py`, `*_optimized.py`
   - ✅ Update existing modules instead of duplicating

2. **Module Organization**
   - Parser modules → `src/parser/`
   - Analysis modules → `src/analysis/`
   - Generation modules → `src/generation/`
   - Core infrastructure → `src/core/`

3. **Experimental Code**
   - All experiments → `archive/experiments/`
   - All prototypes → `archive/experiments/`

4. **Legacy Code**
   - Old versions → `archive/legacy/`
   - Keep for reference, but don't update

5. **Runtime Data**
   - Cache → `runtime/cache/`
   - Logs → `runtime/logs/`
   - Never commit runtime data to git

6. **Outputs**
   - Generated slides → `outputs/slides/`
   - Images → `outputs/images/`
   - Never commit outputs to git

7. **Documentation**
   - Keep `docs/` minimal
   - Archive old docs → `archive/docs/`

8. **Root Directory**
   - Only essential files:
     - README.md
     - CLAUDE.md
     - PROJECT_STRUCTURE.md
     - config.yaml
     - requirements.txt
```

---

## 9. Rollback Plan

If migration fails:

```bash
# Option 1: Reset to backup tag
git reset --hard pre-refactor-backup

# Option 2: Revert last commit
git revert HEAD

# Option 3: Manual rollback
git checkout HEAD~1 -- .
```

---

## 10. Success Criteria

Migration is successful when:

- ✅ All tests pass: `pytest tests/ -v`
- ✅ CLI works: `python cli/main.py process -p papers/example.pdf`
- ✅ No import errors
- ✅ No duplicate version files in `src/`
- ✅ All legacy code in `archive/legacy/`
- ✅ All experiments in `archive/experiments/`
- ✅ Runtime data in `runtime/`
- ✅ Documentation consolidated

---

## 11. Timeline Estimate

- **Phase 1** (Preparation): 5 minutes
- **Phase 2** (Migration): 15 minutes
- **Phase 3** (Import updates): 20 minutes
- **Phase 4** (Config): 5 minutes
- **Phase 5** (Testing): 10 minutes
- **Phase 6** (Cleanup): 5 minutes

**Total**: ~60 minutes (with careful execution)

---

## 12. Next Steps

1. ✅ **Review this plan** - Ensure all stakeholders agree
2. ✅ **Create backup** - Tag current state
3. ✅ **Execute Phase 1** - Create directory structure
4. ✅ **Execute Phase 2-6** - Migrate and test
5. ✅ **Update CLAUDE.md** - Add repository rules
6. ✅ **Create PROJECT_STRUCTURE.md** - Reference for future development

---

**⚠️ DO NOT PROCEED** until this plan is reviewed and approved.

**Questions to resolve before execution**:
- Should we keep `tools/md_to_pptx.py` or archive it?
- Any other experimental scripts to preserve?
- Any specific test papers to use for validation?

---

**End of Migration Plan**
