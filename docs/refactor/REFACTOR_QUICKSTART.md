# 🚀 Repository Refactor Quick Start

**Goal**: Consolidate fragmented versions into clean pipeline architecture

---

## ⚡ 3-Step Process

### Step 1: Preview (2 minutes)

```bash
python scripts/refactor_repository.py --dry-run
```

**Review the output carefully** - this shows exactly what will happen.

---

### Step 2: Execute (5 minutes)

```bash
python scripts/refactor_repository.py
```

The script will:
1. ✅ Create git backup tag
2. ✅ Reorganize files
3. ✅ Update imports
4. ✅ Run tests
5. ✅ Verify CLI

---

### Step 3: Verify (2 minutes)

```bash
# Run tests
pytest tests/ -v

# Test CLI
python cli/main.py process -p papers/Human-In-the-Loop.pdf --format html

# Check structure
ls -la src/parser src/analysis src/generation src/core
```

---

## 📊 What Changes

### Before → After

```
❌ Before:                    ✅ After:

src/                          src/
  ai_analyzer.py                parser/
  ai_analyzer_enhanced.py         ├── pdf_parser.py
  ai_analyzer_enhanced_v3.py      ├── pdf_validator.py
  content_extractor.py            └── pdf_image_extractor.py
  content_extractor_enhanced.py
  content_extractor_enhanced_v3.py  analysis/
  ppt_generator.py                 ├── ai_analyzer.py (V3)
  ppt_generator_enhanced.py        └── content_extractor.py (V3)
  ppt_generator_enhanced_v3.py
  pdf_parser.py                  generation/
  cache_manager.py                 └── ppt_generator.py (V3)
  resilience.py
  progress_reporter.py           core/
                                   ├── cache_manager.py
tools/                              ├── resilience.py
  generate_v3_pptx.py               └── progress_reporter.py
  generate_v3_pptx_simple.py
  generate_v3_pptx_optimized.py  archive/
                                   ├── legacy/
                                     │   ├── ai_analyzer_v1.py
                                     │   └── ...
                                     └── experiments/
                                         ├── generate_v3_pptx.py
                                         └── ...
```

---

## 🎯 Key Benefits

- ✅ **No more version fragmentation** - One canonical implementation per module
- ✅ **Clear pipeline architecture** - parser/analysis/generation
- ✅ **Easier maintenance** - Update modules in place
- ✅ **Prevents directory entropy** - CLAUDE.md rules prevent future mess
- ✅ **Better for Claude collaboration** - Clear structure = better AI assistance

---

## 🛡️ Safety Features

1. **Automatic Backup** - Git tag created before changes
2. **Dry-Run Mode** - Preview without executing
3. **Verification** - Tests and CLI checks
4. **Detailed Logging** - Every action logged
5. **Easy Rollback** - One command to revert

---

## 🔄 Rollback (If Needed)

```bash
# Find backup tag
git tag | grep pre-refactor-backup

# Reset to backup
git reset --hard pre-refactor-backup-YYYYMMDD-HHMMSS
```

---

## 📚 Documentation

- **MIGRATION_PLAN.md** - Detailed migration plan
- **PROJECT_STRUCTURE.md** - New architecture reference
- **scripts/README.md** - Script usage guide
- **CLAUDE.md** - Updated repository rules

---

## ✅ Success Checklist

After migration:

- [ ] Tests pass: `pytest tests/ -v`
- [ ] CLI works: `python cli/main.py process -p papers/example.pdf`
- [ ] No import errors in Python
- [ ] Directory structure is clean
- [ ] Legacy code in `archive/legacy/`
- [ ] Experiments in `archive/experiments/`
- [ ] Runtime data in `runtime/`
- [ ] Reviewed and committed changes

---

## 🆘 Need Help?

1. Check `scripts/README.md` for detailed usage
2. Review `MIGRATION_PLAN.md` for migration details
3. Run with `--dry-run` to preview safely

---

**Estimated Time**: 10 minutes total
**Risk Level**: Low (with backup and dry-run)
**Recommended**: Execute during low-activity period

---

**Ready? Start with**: `python scripts/refactor_repository.py --dry-run`
