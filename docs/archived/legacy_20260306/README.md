# Legacy Files Archive

This directory contains archived files that are no longer used in the main workflow.

## Archive Date
$(date +%Y-%m-%d)

## Archived Files

### Scripts
- `main.py` - Compatibility wrapper (replaced by cli/main.py)
- `cli/main_backup_enhanced_version.py` - Backup file
- `tools/debug_data_flow.py` - Debug tool
- `examples/middle_products_example.py` - Example file

### Shell Scripts
- `tools/reorganize_project.sh` - One-time reorganization script
- `tools/update_docs_after_refactor.sh` - One-time update script
- `tools/install_skill.sh` - Skill installation script
- `tools/test_skill.sh` - Skill testing script
- `tools/quick_test.sh` - Quick test script

### Skills Directory
- `skills/` - Complete skill functionality directory (not part of main workflow)

### Documentation
- `PROJECT_SUMMARY.md` - Duplicate of docs/architecture/PROJECT_SUMMARY.md
- `FINAL_SUMMARY.md` - Temporary summary document
- `Human-In-the-Loop_debug.md` - Debug output file

## Current Main Workflow

### Entry Points
- **Standard**: `python cli/main.py process --paper <file.pdf>`
- **Enhanced**: `python tools/generate_enhanced_pptx.py <file.pdf>`

### Core Modules
- `src/ai_analyzer_enhanced.py` - Enhanced AI analyzer (V3)
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
- `tests/test_*.py` - Unit tests

## Reason for Archival
These files were used during development or are experimental features that are not part of the current main workflow. They are archived for reference but should not be used in production.
