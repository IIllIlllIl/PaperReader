# Changelog - Clean Intermediates Feature

2026-03-19 - Clean Intermediates Feature Added

==================================

Added automatic cleanup of intermediate files after pipeline execution.

## New Features

- **Automatic Cleanup**: Pipeline automatically removes intermediate files after successful completion (`--clean`, default)
- **Debug Mode**: Added `--no-clean` flag to preserve all intermediate files for debugging
- **Failure Preservation**: Pipeline preserves intermediate files on failure for troubleshooting
- **Manual Cleanup Script**: Added `scripts/clean_intermediates.py` for manual cleanup with dry-run mode

## Command Line Changes

- Added `--clean/--no-clean` flag to the `pipeline` command
- Default behavior now cleans intermediate files after a successful run
- Debug mode preserves intermediate files under `outputs/intermediates/`

## Files Modified

- `src/core/pipeline.py`: cleanup methods and intermediate-file lifecycle handling
- `src/cli/main.py`: `--clean/--no-clean` CLI options
- `README.md`: updated usage and cleanup documentation
- `docs/project/QUICK_START.md`: updated examples for debug mode

## Files Added

- `src/scripts/clean_intermediates.py`: standalone cleanup script with dry-run mode
- `tests/test_clean_intermediates.py`: unit tests for cleanup behavior
- `docs/CLEAN_INTERMEDIATES.md`: detailed cleanup documentation
- `docs/CLEAN_FEATURE_IMPLEMENTATION_REPORT.md`: implementation summary

## Testing

- Unit tests passed
- Integration tests verified
- Manual cleanup script tested
- Directory structure verification added

## Usage Examples

### Default Mode (Auto-clean)
```bash
python -m src.cli.main pipeline --paper papers/example.pdf
# Result: intermediate files cleaned, final PPTX preserved
```

### Debug Mode (Preserve files)
```bash
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
# Result: intermediate files preserved in outputs/intermediates/
```

### Manual Cleanup
```bash
# Preview
python src/scripts/clean_intermediates.py

# Execute
python src/scripts/clean_intermediates.py --execute
```

## Benefits

- **Cleaner Workspace**: final PPTX remains the main deliverable by default
- **Easier Debugging**: `--no-clean` preserves inspectable intermediates
- **Safer Failure Handling**: failed runs keep diagnostics available
- **Centralized Layout**: intermediate outputs live under `outputs/intermediates/`

## Migration Notes

- No migration required for users
- Default behavior now auto-cleans intermediates after success
- Use `--no-clean` when you need the older inspectable workflow
