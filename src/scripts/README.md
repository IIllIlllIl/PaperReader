# Repository refactor script

The repository normalization script now lives at `tools/refactor_repository.py`.

## Usage

```bash
python tools/refactor_repository.py --dry-run
python tools/refactor_repository.py
python tools/refactor_repository.py --skip-checks
```

## What it does

- ensures canonical directories exist under `runtime/`, `outputs/`, `src/prompts/`, and `archive/docs/`
- merges legacy `cache/`, `logs/`, and `output/` into `runtime/` and `outputs/` with compare-before-overwrite behavior
- moves top-level prompt modules from `prompts/` into `src/prompts/`
- archives non-canonical docs directories under `archive/docs/`
- updates active path references in code, settings, and active docs
- optionally runs CLI and test verification

## Notes

- Use `--dry-run` first to preview the filesystem changes.
- If a destination file already exists with different content, the script leaves the source file in place and reports a conflict.
