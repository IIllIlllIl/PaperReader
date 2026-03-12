# Legacy Files Archive Summary

**Archive Date**: 2026-03-06  
**Archive Location**: `docs/archived/legacy_20260306/`  
**Total Files Archived**: 19

---

## Archive Purpose

This archive contains development and experimental files that are no longer part of the main PaperReader workflow. These files were archived to:

1. **Clean up the project structure** - Remove unused files from the main directories
2. **Improve project clarity** - Make it clear which files are part of the main workflow
3. **Preserve development history** - Keep files for reference without cluttering the project

---

## Archived Files Summary

### 📁 Scripts (4 files)

| File | Original Location | Reason |
|------|------------------|---------|
| `main.py` | Root directory | Compatibility wrapper, replaced by `cli/main.py` |
| `main_backup_enhanced_version.py` | `cli/` | Backup file, main workflow uses `cli/main.py` |
| `debug_data_flow.py` | `tools/` | Debug tool, not part of production workflow |
| `middle_products_example.py` | `examples/` | Example file, not part of production workflow |

### 📁 Shell Scripts (5 files)

| File | Original Location | Reason |
|------|------------------|---------|
| `reorganize_project.sh` | `tools/` | One-time reorganization script (completed) |
| `update_docs_after_refactor.sh` | `tools/` | One-time update script (completed) |
| `install_skill.sh` | `tools/` | Skill installation script (not main workflow) |
| `test_skill.sh` | `tools/` | Skill testing script (not main workflow) |
| `quick_test.sh` | `tools/` | Quick test script (not main workflow) |

### 📁 Skills Directory (1 directory)

| Directory | Original Location | Reason |
|-----------|------------------|---------|
| `skills/` | Root directory | Complete skill functionality (not main workflow) |

### 📁 Documentation (3 files)

| File | Original Location | Reason |
|------|------------------|---------|
| `PROJECT_SUMMARY.md` | Root directory | Duplicate of `docs/architecture/PROJECT_SUMMARY.md` |
| `FINAL_SUMMARY.md` | Root directory | Temporary summary document |
| `Human-In-the-Loop_debug.md` | `output/markdown/` | Debug output file |

---

## Current Main Workflow (Post-Archive)

### Entry Points

**Standard Version** (16 slides, ~$0.06)
```bash
python cli/main.py process --paper <file.pdf> --format html
```

**Enhanced Version** (30 slides, ~$0.11) - **RECOMMENDED**
```bash
python tools/generate_enhanced_pptx.py <file.pdf>
```

### Core Modules

- `src/ai_analyzer_enhanced.py` - Enhanced AI analyzer (V3 prompt)
- `src/content_extractor_enhanced.py` - Enhanced content extractor (V3)
- `src/ppt_generator_enhanced.py` - Enhanced PPT generator (V3)
- `src/pdf_parser.py` - PDF text extraction
- `src/cache_manager.py` - Analysis caching
- `src/resilience.py` - Retry logic
- `src/progress_reporter.py` - Progress bars
- `src/utils.py` - Utilities

### Tools

- `tools/generate_enhanced_pptx.py` - One-click enhanced PPTX generation
- `tools/md_to_pptx.py` - Markdown to PPTX converter

### Tests

- `tests/test_*.py` - Unit tests for all modules

---

## Project Structure Improvement

### Before Archive
- Root directory: **cluttered** with development files
- Tools directory: **mixed** production and development scripts
- Skills directory: **experimental** feature in root

### After Archive
- Root directory: **clean** with only essential files
  - `CLAUDE.md` - Project instructions
  - `README.md` - Project overview
  - `config.yaml` - Configuration
  - `requirements.txt` - Dependencies
  
- Tools directory: **focused** on production tools
  - `generate_enhanced_pptx.py` - Enhanced PPTX generation
  - `md_to_pptx.py` - Markdown converter
  - `archive_legacy_files.sh` - Archive script

- Source code: **unchanged** and fully functional

---

## Recovery Instructions

If you need to restore any archived files:

1. Navigate to the archive directory:
   ```bash
   cd docs/archived/legacy_20260306/
   ```

2. Find the file you need:
   ```bash
   find . -name "<filename>"
   ```

3. Copy it back to the original location:
   ```bash
   cp <path_in_archive> <original_location>
   ```

---

## Impact Assessment

✅ **No impact on main workflow** - All archived files are not used in production  
✅ **Tests still pass** - No test dependencies archived  
✅ **Documentation intact** - Only duplicates and temporary docs archived  
✅ **Source code unchanged** - All `src/` modules remain in place  

---

## Future Maintenance

**Do NOT unarchive files unless:**
1. You need to restore the skill functionality
2. You need to reference the debug tool for troubleshooting
3. You need to review the reorganization scripts for similar projects

**Consider deleting this archive:**
- After 30 days if no issues arise
- After confirming all workflows are stable
- When archiving to long-term storage

---

**Archived by**: PaperReader Development Team  
**Archive Tool**: `tools/archive_legacy_files.sh`
