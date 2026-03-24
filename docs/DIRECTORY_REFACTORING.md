# Directory Structure Refactoring

## Overview

Refactored the output directory structure to organize all intermediate artifacts under `outputs/intermediates/` for better organization and safety.

## Changes

### Old Structure
```
outputs/
├── images/              # Extracted figures
├── markdown/            # Generated markdown
├── scripts/             # Presentation scripts
├── plans/               # Slide plans (JSON)
├── citations/           # Citation cache
├── temp/                # Temporary files
├── slides/              # Final PPTX files ✓
└── reports/             # Run reports ✓
```

### New Structure
```
outputs/
├── intermediates/       # All intermediate artifacts
│   ├── images/          # Extracted figures
│   ├── markdown/        # Generated markdown
│   ├── scripts/         # Presentation scripts
│   ├── plans/           # Slide plans (JSON)
│   ├── citations/       # Citation cache
│   └── temp/            # Temporary files
├── slides/              # Final PPTX files (kept)
└── reports/             # Run reports (kept)
```

## Modified Files

### 1. `src/core/pipeline.py`
- Updated output paths for markdown, scripts, and plans to use `intermediates/`
- Updated image extraction path to `intermediates/images/`

### 2. `src/parser/pdf_image_extractor.py`
- Changed default `output_dir` from `"outputs/images"` to `"outputs/intermediates/images"`

### 3. `src/analysis/citation_analyzer.py`
- Changed default `cache_dir` from `"outputs/citations"` to `"outputs/intermediates/citations"`

### 4. `src/analysis/citation_integration.py`
- Updated chart generator output directory to `"outputs/intermediates/images/citations"`

### 5. `src/generation/ppt_generator.py`
- No changes needed (relative paths remain correct)

### 6. `src/planning/slide_planner.py`
- No changes needed (doesn't handle file paths)

## Migration Guide

### For New Users

Simply run the pipeline as usual. All intermediate files will be automatically created in `outputs/intermediates/`.

```bash
python -m src.cli.main pipeline --paper papers/example.pdf
```

### For Existing Users

If you have existing intermediate files in the old structure, use the migration script:

```bash
# Dry run to see what would be migrated
python scripts/migrate_to_intermediates.py

# Execute migration
python scripts/migrate_to_intermediates.py --execute
```

**Note:** The migration script will:
- Skip directories that don't exist
- Skip directories where the target already exists and is not empty
- Only move directories, not delete them

### Manual Migration

Alternatively, you can manually move directories:

```bash
mkdir -p outputs/intermediates
mv outputs/images outputs/intermediates/
mv outputs/markdown outputs/intermediates/
mv outputs/scripts outputs/intermediates/
mv outputs/plans outputs/intermediates/
mv outputs/citations outputs/intermediates/
mv outputs/temp outputs/intermediates/  # if exists
```

## Benefits

### 1. **Safety**
- Clean separation between intermediate artifacts and final results
- Less risk of accidentally deleting important files

### 2. **Simplicity**
- All intermediate files in one location
- Easy to clean up: just delete `outputs/intermediates/`

### 3. **Clarity**
- Clear distinction between:
  - **Final artifacts**: `slides/`, `reports/` (kept)
  - **Intermediate artifacts**: Everything in `intermediates/`

### 4. **Maintainability**
- Easy to add new intermediate directories
- Clear organization for debugging

## Backward Compatibility

**Breaking Change**: This is a breaking change for users who:
1. Hard-coded paths to `outputs/images/`, `outputs/markdown/`, etc.
2. Have scripts that reference the old directory structure

**Solution**:
- Update any hard-coded paths to use the new structure
- Use the migration script to move existing files

## Testing

Run the test suite to ensure all modules work correctly:

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_citation_analyzer.py
pytest tests/test_pipeline.py
```

## Verification

After running the pipeline, verify the new structure:

```bash
# Check intermediate artifacts
ls outputs/intermediates/
# Expected: images/ markdown/ scripts/ plans/ citations/

# Check final artifacts
ls outputs/
# Expected: slides/ intermediates/ (and possibly reports/)
```

## Questions?

If you encounter any issues with this refactoring:
1. Check that all modules are using the updated paths
2. Run the migration script to move existing files
3. Verify that `outputs/intermediates/` directory structure is correct
