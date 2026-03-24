#!/usr/bin/env python3
"""
Clean intermediate files from PaperReader pipeline.

This script removes all intermediate files while preserving final outputs
(slides, reports).

Usage:
    # Preview what will be deleted (dry run)
    python src/scripts/clean_intermediates.py

    # Actually delete files
    python src/scripts/clean_intermediates.py --execute

    # Also delete citation cache
    python src/scripts/clean_intermediates.py --execute --include-cache
"""

import sys
import shutil
from pathlib import Path
from typing import Tuple


def get_directory_stats(directory: Path) -> Tuple[int, int]:
    """
    Get file count and total size of a directory.

    Args:
        directory: Directory to analyze

    Returns:
        Tuple of (file_count, total_size_bytes)
    """
    file_count = 0
    total_size = 0

    if not directory.exists():
        return 0, 0

    for f in directory.glob('**/*'):
        if f.is_file():
            file_count += 1
            total_size += f.stat().st_size

    return file_count, total_size


def clean_intermediates(output_dir: str = "outputs",
                       dry_run: bool = True,
                       include_cache: bool = False) -> bool:
    """
    Clean intermediate files from pipeline runs.

    Args:
        output_dir: Base output directory
        dry_run: If True, only preview what would be deleted
        include_cache: If True, also delete citation cache

    Returns:
        True if successful, False otherwise
    """
    output_path = Path(output_dir)
    intermediates_dir = output_path / "intermediates"

    print(f"{'[DRY RUN] ' if dry_run else ''}Cleaning intermediate files\n")
    print(f"Output directory: {output_path.absolute()}")
    print(f"Intermediates directory: {intermediates_dir.absolute()}\n")

    if not intermediates_dir.exists():
        print("✓ Intermediates directory does not exist. Nothing to clean.")
        return True

    # Get statistics
    file_count, total_size = get_directory_stats(intermediates_dir)

    if file_count == 0:
        print("✓ Intermediates directory is empty. Nothing to clean.")
        return True

    size_kb = total_size / 1024
    size_mb = size_kb / 1024

    print(f"Found {file_count} files ({size_mb:.2f} MB / {size_kb:.2f} KB)\n")

    # List subdirectories and their stats
    print("Contents:")
    for subdir in sorted(intermediates_dir.iterdir()):
        if subdir.is_dir():
            sub_file_count, sub_size = get_directory_stats(subdir)
            if sub_file_count > 0:
                sub_size_kb = sub_size / 1024
                print(f"  📁 {subdir.name}/: {sub_file_count} files ({sub_size_kb:.2f} KB)")
        elif subdir.is_file():
            size_kb = subdir.stat().st_size / 1024
            print(f"  📄 {subdir.name}: {size_kb:.2f} KB")

    print()

    # Handle cache separately if requested
    if include_cache:
        cache_dir = intermediates_dir / "citations"
        if cache_dir.exists():
            cache_files, cache_size = get_directory_stats(cache_dir)
            if cache_files > 0:
                cache_size_kb = cache_size / 1024
                print(f"  📦 Citation cache: {cache_files} files ({cache_size_kb:.2f} KB)")

    print()

    if dry_run:
        print("="*70)
        print("DRY RUN - No files will be deleted")
        print("="*70)
        print(f"\nTo actually delete these files, run:")
        print(f"  python src/scripts/clean_intermediates.py --execute")
        if not include_cache:
            print(f"\nTo also clean citation cache:")
            print(f"  python src/scripts/clean_intermediates.py --execute --include-cache")
        return True

    # Confirm deletion
    print("="*70)
    print("⚠️  WARNING: This will permanently delete all intermediate files!")
    print("="*70)
    response = input(f"\nDelete {file_count} files ({size_mb:.2f} MB)? [y/N]: ")

    if response.lower() != 'y':
        print("❌ Cancelled")
        return False

    # Delete files
    try:
        print(f"\n🗑️  Deleting intermediates directory...")
        shutil.rmtree(intermediates_dir)
        print(f"✅ Deleted: {intermediates_dir}")

        # Recreate empty structure
        print(f"\n📁 Recreating empty directory structure...")
        subdirs = ['images', 'images/citations', 'markdown', 'scripts', 'plans', 'citations', 'temp']
        for subdir in subdirs:
            new_dir = intermediates_dir / subdir
            new_dir.mkdir(parents=True, exist_ok=True)

        print(f"✅ Created {len(subdirs)} subdirectories")

        print(f"\n{'='*70}")
        print(f"✅ Successfully cleaned {file_count} files ({size_mb:.2f} MB)")
        print(f"{'='*70}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean intermediate files from PaperReader pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Preview what will be deleted
    python src/scripts/clean_intermediates.py

    # Delete intermediate files
    python src/scripts/clean_intermediates.py --execute

    # Also delete citation cache
    python src/scripts/clean_intermediates.py --execute --include-cache
        """
    )

    parser.add_argument(
        '--output-dir',
        default='outputs',
        help='Output directory (default: outputs)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually delete files (default is dry-run)'
    )
    parser.add_argument(
        '--include-cache',
        action='store_true',
        help='Also delete citation API cache'
    )

    args = parser.parse_args()

    # Run cleanup
    dry_run = not args.execute
    success = clean_intermediates(
        output_dir=args.output_dir,
        dry_run=dry_run,
        include_cache=args.include_cache
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
