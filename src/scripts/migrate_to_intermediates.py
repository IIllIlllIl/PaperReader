#!/usr/bin/env python3
"""
Migration script: Move intermediate artifacts to outputs/intermediates/

This script migrates existing files from the old structure:
- outputs/images/
- outputs/markdown/
- outputs/scripts/
- outputs/plans/
- outputs/citations/
- outputs/temp/

To the new structure:
- outputs/intermediates/images/
- outputs/intermediates/markdown/
- outputs/intermediates/scripts/
- outputs/intermediates/plans/
- outputs/intermediates/citations/
- outputs/intermediates/temp/
"""

import shutil
from pathlib import Path
import sys


def migrate(output_dir: str = "outputs", dry_run: bool = False):
    """
    Migrate existing intermediate files to new structure.

    Args:
        output_dir: Base output directory
        dry_run: If True, only print what would be done
    """
    output_path = Path(output_dir)
    intermediates_dir = output_path / "intermediates"

    # Directories to migrate
    dirs_to_migrate = ['images', 'markdown', 'scripts', 'plans', 'citations', 'temp']

    print(f"{'[DRY RUN] ' if dry_run else ''}Migrating intermediate artifacts to {intermediates_dir}/\n")

    migrated_count = 0
    skipped_count = 0

    for dir_name in dirs_to_migrate:
        old_dir = output_path / dir_name
        new_dir = intermediates_dir / dir_name

        if not old_dir.exists():
            print(f"  ⊘ {dir_name}/ - doesn't exist, skipping")
            skipped_count += 1
            continue

        if new_dir.exists():
            # Check if new_dir already has content
            if any(new_dir.iterdir()):
                print(f"  ⚠ {dir_name}/ - target already exists and is not empty, skipping")
                print(f"      Old: {old_dir}")
                print(f"      New: {new_dir}")
                skipped_count += 1
                continue

        if dry_run:
            print(f"  ✓ {dir_name}/ - would migrate")
            print(f"      {old_dir} -> {new_dir}")
            migrated_count += 1
        else:
            try:
                # Create parent directory
                new_dir.parent.mkdir(parents=True, exist_ok=True)

                # Move directory
                shutil.move(str(old_dir), str(new_dir))
                print(f"  ✓ {dir_name}/ - migrated")
                print(f"      {old_dir} -> {new_dir}")
                migrated_count += 1
            except Exception as e:
                print(f"  ✗ {dir_name}/ - failed: {e}")
                skipped_count += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Migration summary:")
    print(f"  Migrated: {migrated_count} directories")
    print(f"  Skipped:  {skipped_count} directories")

    if dry_run:
        print(f"\nThis was a dry run. Run with --execute to perform actual migration.")

    return migrated_count, skipped_count


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate intermediate artifacts to outputs/intermediates/"
    )
    parser.add_argument(
        '--output-dir',
        default='outputs',
        help='Base output directory (default: outputs)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually perform migration (default is dry-run)'
    )

    args = parser.parse_args()

    # Run migration
    dry_run = not args.execute
    migrated, skipped = migrate(args.output_dir, dry_run=dry_run)

    # Exit with appropriate code
    if skipped > 0 and not dry_run:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
