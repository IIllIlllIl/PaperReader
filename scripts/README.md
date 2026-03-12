# Refactor Script Usage Guide

This guide explains how to use the automated repository refactor script.

---

## Quick Start

### Step 1: Preview Changes (Dry Run)

```bash
python scripts/refactor_repository.py --dry-run
```

This will show you exactly what the script will do **without making any changes**.

**Expected output**:
- Directories that will be created
- Files that will be moved
- Imports that will be updated
- No actual changes made

### Step 2: Execute Migration

Once you're satisfied with the preview:

```bash
python scripts/refactor_repository.py
```

This will:
1. Create a git backup tag
2. Reorganize the repository
3. Update all imports
4. Run tests
5. Verify CLI

---

## What the Script Does

### Phase 1: Preparation
- ✅ Creates git backup tag (e.g., `pre-refactor-backup-20260312-143022`)
- ✅ Creates new directory structure:
  - `src/parser/`, `src/analysis/`, `src/generation/`, `src/core/`
  - `runtime/cache/`, `runtime/logs/`
  - `outputs/slides/`, `outputs/images/`, `outputs/markdown/`
  - `archive/legacy/`, `archive/experiments/`

### Phase 2: File Migration
- ✅ Moves V3 modules to canonical locations:
  - `ai_analyzer_enhanced_v3.py` → `src/analysis/ai_analyzer.py`
  - `content_extractor_enhanced_v3.py` → `src/analysis/content_extractor.py`
  - `ppt_generator_enhanced_v3.py` → `src/generation/ppt_generator.py`
- ✅ Moves parser modules to `src/parser/`
- ✅ Archives legacy versions to `archive/legacy/`
- ✅ Archives experimental scripts to `archive/experiments/`
- ✅ Reorganizes runtime data (cache, logs)

### Phase 3: Import Updates
- ✅ Updates all Python imports automatically:
  - `from src.ai_analyzer import` → `from src.analysis.ai_analyzer import`
  - `from src.ppt_generator import` → `from src.generation.ppt_generator import`
  - etc.
- ✅ Updates CLI imports
- ✅ Updates test imports

### Phase 4: Configuration Updates
- ✅ Updates `config.yaml` paths:
  - `cache_dir: cache/` → `cache_dir: runtime/cache/`
  - `output_dir: output/` → `output_dir: outputs/`
- ✅ Updates `.gitignore`

### Phase 5: Verification
- ✅ Runs test suite: `pytest tests/ -v`
- ✅ Verifies CLI entry point works

### Phase 6: Cleanup
- ✅ Removes empty directories

---

## Command Options

### `--dry-run`
Preview changes without executing them.

```bash
python scripts/refactor_repository.py --dry-run
```

**Use this first!**

### `--skip-tests`
Skip running tests after migration.

```bash
python scripts/refactor_repository.py --skip-tests
```

**Not recommended** - tests verify the migration was successful.

### `--no-backup`
Skip creating git backup tag.

```bash
python scripts/refactor_repository.py --no-backup
```

**Not recommended** - the backup tag is your safety net.

---

## Rollback Plan

### If Migration Fails

The script automatically creates a git backup tag before making changes.

**To rollback**:

```bash
# Find the backup tag
git tag | grep pre-refactor-backup

# Reset to backup tag
git reset --hard pre-refactor-backup-20260312-143022

# Clean up uncommitted changes
git clean -fd
```

### If You Want to Re-run

```bash
# Reset to backup first
git reset --hard pre-refactor-backup-*

# Run script again
python scripts/refactor_repository.py --dry-run
python scripts/refactor_repository.py
```

---

## Post-Migration Checklist

After running the script:

### 1. Review Changes

```bash
# See what changed
git status

# Review import changes
git diff cli/main.py
git diff tests/
```

### 2. Run Tests Manually

```bash
pytest tests/ -v
```

### 3. Test CLI

```bash
# Test standard processing
python cli/main.py process --paper papers/Human-In-the-Loop.pdf --format html

# Check cache
python cli/main.py stats
```

### 4. Verify Directory Structure

```bash
# Check new structure
ls -la src/parser/
ls -la src/analysis/
ls -la src/generation/
ls -la src/core/

# Check archive
ls -la archive/legacy/
ls -la archive/experiments/

# Check runtime
ls -la runtime/
```

### 5. Commit Changes

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

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Cause**: Imports not updated correctly.

**Solution**:
```bash
# Check if imports were updated
grep -r "from src.ai_analyzer import" cli/ tests/

# If not, run script again
python scripts/refactor_repository.py --dry-run
```

### Issue: "Tests failed"

**Cause**: Import paths or module structure incorrect.

**Solution**:
```bash
# Check specific test
pytest tests/test_ai_analyzer.py -v

# Check import manually
python -c "from src.analysis.ai_analyzer import AIAnalyzer; print('OK')"
```

### Issue: "CLI not working"

**Cause**: CLI imports not updated.

**Solution**:
```bash
# Check CLI imports
python -c "from cli.main import cli; print('CLI OK')"

# If fails, check cli/main.py imports manually
cat cli/main.py | grep "from src"
```

### Issue: "File already exists"

**Cause**: Running script multiple times without cleanup.

**Solution**:
```bash
# Reset to backup
git reset --hard pre-refactor-backup-*

# Or manually remove files
rm -rf src/parser src/analysis src/generation src/core
```

---

## Expected Results

### Before Migration

```
src/
├── ai_analyzer.py
├── ai_analyzer_enhanced.py
├── ai_analyzer_enhanced_v3.py
├── content_extractor.py
├── content_extractor_enhanced.py
├── content_extractor_enhanced_v3.py
├── ppt_generator.py
├── ppt_generator_enhanced.py
├── ppt_generator_enhanced_v3.py
├── pdf_parser.py
├── cache_manager.py
└── ...
```

### After Migration

```
src/
├── parser/
│   ├── pdf_parser.py
│   ├── pdf_validator.py
│   └── pdf_image_extractor.py
│
├── analysis/
│   ├── ai_analyzer.py           (V3 canonical)
│   └── content_extractor.py     (V3 canonical)
│
├── generation/
│   └── ppt_generator.py         (V3 canonical)
│
├── core/
│   ├── cache_manager.py
│   ├── resilience.py
│   └── progress_reporter.py
│
└── utils.py
```

---

## Safety Features

The script includes multiple safety features:

1. ✅ **Automatic git backup** - Creates a tag before making changes
2. ✅ **Dry-run mode** - Preview changes without executing
3. ✅ **Verification steps** - Tests and CLI verification
4. ✅ **Detailed logging** - Every action is logged
5. ✅ **Error handling** - Stops on errors
6. ✅ **Rollback instructions** - Clear recovery steps

---

## Questions?

If you encounter any issues:

1. Run with `--dry-run` first
2. Check the logs carefully
3. Use the rollback plan if needed
4. Review `MIGRATION_PLAN.md` for detailed information

---

**Created by**: Claude Code
**Date**: 2026-03-12
**Version**: 1.0
