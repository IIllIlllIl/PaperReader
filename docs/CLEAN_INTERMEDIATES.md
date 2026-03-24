# Clean Intermediates Feature Documentation

## Overview

PaperReader automatically cleans intermediate files after successful pipeline execution, taking advantage of the centralized `outputs/intermediates/` directory structure.

## How It Works

### Default Behavior (--clean)

By default, the pipeline automatically removes all intermediate files after successful completion:

```bash
# Default: cleans intermediates after success
python -m src.cli.main pipeline --paper papers/example.pdf
```

**What gets cleaned**:
- `outputs/intermediates/images/` - Extracted figures
- `outputs/intermediates/markdown/` - Generated Markdown
- `outputs/intermediates/scripts/` - Presentation scripts
- `outputs/intermediates/plans/` - Slide plans (JSON)
- `outputs/intermediates/citations/` - Citation cache
- `outputs/intermediates/temp/` - Temporary files

**What is preserved**:
- `outputs/slides/*.pptx` - Final presentations
- `outputs/reports/*.md` - Run reports

### Debug Mode (--no-clean)

To preserve all intermediate files for debugging:

```bash
# Keep all intermediate files
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
```

**When to use --no-clean**:
- Debugging pipeline issues
- Inspecting intermediate outputs
- Developing new features
- Custom post-processing

### Failure Behavior

If the pipeline fails (exception or error), intermediate files are **automatically preserved** for debugging:

```bash
# If pipeline fails, intermediates are kept
python -m src.cli.main pipeline --paper papers/broken.pdf
# Output: "ℹ️  Intermediate files preserved in outputs/intermediates/ for debugging"
```

## Manual Cleanup

### Using the Cleanup Script

Preview what will be deleted (dry run):

```bash
python src/scripts/clean_intermediates.py
```

Output:
```
[DRY RUN] Cleaning intermediate files

Output directory: /path/to/outputs
Intermediates directory: /path/to/outputs/intermediates

Found 42 files (3.45 MB / 3532.80 KB)

Contents:
  📁 images/: 15 files (2500.00 KB)
  📁 markdown/: 5 files (150.00 KB)
  📁 scripts/: 5 files (200.00 KB)
  📁 plans/: 5 files (100.00 KB)
  📁 citations/: 12 files (582.80 KB)

======================================================================
DRY RUN - No files will be deleted
======================================================================

To actually delete these files, run:
  python src/scripts/clean_intermediates.py --execute
```

Execute cleanup:

```bash
python src/scripts/clean_intermediates.py --execute
```

### Including Citation Cache

By default, the cleanup script preserves citation API cache. To also clean the cache:

```bash
python src/scripts/clean_intermediates.py --execute --include-cache
```

### Manual Deletion

Simply delete the entire intermediates directory:

```bash
rm -rf outputs/intermediates/
```

The directory will be recreated on the next pipeline run.

## Implementation Details

### Clean Method

The `_clean_intermediate_files()` method in `PaperPresentationPipeline`:

1. **Check flag**: If `clean_intermediates=False`, skip cleanup
2. **Calculate stats**: Count files and total size
3. **Delete directory**: Remove entire `outputs/intermediates/` directory
4. **Recreate structure**: Create empty subdirectories for next run

### Failure Handling

On pipeline failure:
```python
try:
    # Run pipeline stages...
except Exception as e:
    # Keep intermediate files for debugging
    if self.clean_intermediates:
        logger.info("Preserving intermediate files for debugging (pipeline failed)")
    raise
```

## Benefits

### 1. Disk Space Management
- Automatically cleans up temporary files
- Prevents accumulation of old intermediate files
- Typical savings: 1-10 MB per paper processed

### 2. Clean Workspace
- Only final artifacts remain (PPTX, reports)
- Clear separation between final and intermediate outputs
- Easier to find important files

### 3. Debugging Support
- `--no-clean` mode for inspection
- Automatic preservation on failure
- Manual cleanup script for control

### 4. Simplicity
- Single directory to clean
- No complex file-by-file logic
- Leverages centralized structure

## Configuration

### Pipeline Initialization

```python
pipeline = PaperPresentationPipeline(
    api_key="your_key",
    config={},
    clean_intermediates=True  # Default: True
)
```

### CLI Parameters

```bash
# Enable cleanup (default)
--clean

# Disable cleanup (debug mode)
--no-clean
```

## Best Practices

### For Regular Use
- Use default `--clean` mode
- Let pipeline manage cleanup automatically
- Final PPTX files are always preserved

### For Debugging
```bash
# Step 1: Run with --no-clean
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean

# Step 2: Inspect intermediate files
ls outputs/intermediates/

# Step 3: Clean when done
python src/scripts/clean_intermediates.py --execute
```

### For CI/CD
- Use default `--clean` mode
- Ensures clean workspace for each build
- Only final artifacts are archived

## Troubleshooting

### Issue: Intermediates directory grows large

**Solution**: Enable default cleaning or run manual cleanup:
```bash
python src/scripts/clean_intermediates.py --execute
```

### Issue: Need to inspect intermediate files

**Solution**: Use `--no-clean` mode:
```bash
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
```

### Issue: Pipeline failed and I lost intermediate files

**Solution**: Intermediate files are automatically preserved on failure. Check `outputs/intermediates/`.

### Issue: Citation cache is being deleted

**Solution**:
- Use `--no-clean` to preserve cache
- Or let it rebuild automatically (cached API calls are faster)

## Examples

### Example 1: Normal Workflow
```bash
# Run pipeline (auto-clean)
python -m src.cli.main pipeline --paper papers/paper1.pdf

# Final PPTX preserved in outputs/slides/paper1.pptx
# All intermediates cleaned up
```

### Example 2: Debug Workflow
```bash
# Run with debug mode
python -m src.cli.main pipeline --paper papers/paper1.pdf --no-clean

# Check intermediate outputs
cat outputs/intermediates/markdown/paper1.md
ls outputs/intermediates/images/

# Clean up when done
python src/scripts/clean_intermediates.py --execute
```

### Example 3: Multiple Papers
```bash
# Process multiple papers (each auto-cleans)
python -m src.cli.main pipeline --paper papers/paper1.pdf
python -m src.cli.main pipeline --paper papers/paper2.pdf
python -m src.cli.main pipeline --paper papers/paper3.pdf

# Only final PPTX files remain
ls outputs/slides/
# Output: paper1.pptx paper2.pptx paper3.pptx
```

## Related Documentation

- **Directory Structure**: `docs/DIRECTORY_REFACTORING.md`
- **Output Structure**: `README.md` → Output Structure section
- **Quick Start**: `QUICK_START.md`
