#!/usr/bin/env python3
"""
Repository Refactor Script

Automated script to reorganize the PaperReader repository from fragmented versions
to a clean pipeline architecture (parser/analysis/generation).

Usage:
    python scripts/refactor_repository.py [--dry-run] [--skip-tests]

Options:
    --dry-run       Show what would be done without making changes
    --skip-tests    Skip running tests after migration
    --no-backup     Skip creating git backup tag (not recommended)

Author: Claude Code
Date: 2026-03-12
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import argparse
import re


class RepositoryRefactor:
    """Automated repository refactoring"""

    def __init__(self, dry_run: bool = False, skip_tests: bool = False, no_backup: bool = False):
        self.dry_run = dry_run
        self.skip_tests = skip_tests
        self.no_backup = no_backup
        self.root_dir = Path(__file__).parent.parent
        self.stats = {
            'files_moved': 0,
            'files_renamed': 0,
            'imports_updated': 0,
            'dirs_created': 0,
        }

    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DRY_RUN": "🔍",
        }.get(level, "ℹ️")

        if self.dry_run and level not in ["DRY_RUN", "WARNING", "ERROR"]:
            prefix = "🔍 [DRY-RUN]"

        print(f"{prefix} {message}")

    def run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command"""
        if self.dry_run:
            self.log(f"Would run: {' '.join(cmd)}", "DRY_RUN")
            return subprocess.CompletedProcess(cmd, 0, b"", b"")

        result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True)
        if check and result.returncode != 0:
            self.log(f"Command failed: {' '.join(cmd)}", "ERROR")
            self.log(f"Error: {result.stderr}", "ERROR")
            raise RuntimeError(f"Command failed: {cmd}")

        return result

    def create_backup(self):
        """Create a git backup tag"""
        if self.no_backup:
            self.log("Skipping backup tag creation", "WARNING")
            return

        self.log("Creating git backup tag...")

        # Get current branch
        result = self.run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        current_branch = result.stdout.strip()

        # Create backup tag
        timestamp = subprocess.run(
            ["date", "+%Y%m%d-%H%M%S"],
            capture_output=True,
            text=True
        ).stdout.strip()

        tag_name = f"pre-refactor-backup-{timestamp}"

        self.run_command(["git", "tag", "-a", tag_name, "-m", "Backup before repository refactor"])

        self.log(f"Backup tag created: {tag_name}", "SUCCESS")
        self.log(f"To rollback: git reset --hard {tag_name}")

    def create_directory_structure(self):
        """Create the new directory structure"""
        self.log("Creating new directory structure...")

        dirs_to_create = [
            "src/parser",
            "src/analysis",
            "src/generation",
            "src/core",
            "runtime/cache",
            "runtime/logs",
            "outputs/slides",
            "outputs/images",
            "outputs/markdown",
            "archive/legacy",
            "archive/experiments",
            "archive/docs",
        ]

        for dir_path in dirs_to_create:
            full_path = self.root_dir / dir_path
            if not full_path.exists():
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Created directory: {dir_path}")
                self.stats['dirs_created'] += 1
            else:
                self.log(f"Directory already exists: {dir_path}")

        # Create __init__.py files
        init_dirs = ["src/parser", "src/analysis", "src/generation", "src/core"]
        for dir_path in init_dirs:
            init_file = self.root_dir / dir_path / "__init__.py"
            if not init_file.exists():
                if not self.dry_run:
                    init_file.touch()
                self.log(f"Created __init__.py: {dir_path}/__init__.py")

    def move_file(self, src: str, dst: str, description: str = ""):
        """Move a file using git mv"""
        src_path = self.root_dir / src
        dst_path = self.root_dir / dst

        if not src_path.exists():
            self.log(f"Source file not found, skipping: {src}", "WARNING")
            return False

        if dst_path.exists():
            self.log(f"Destination already exists, skipping: {dst}", "WARNING")
            return False

        desc = f" ({description})" if description else ""
        self.log(f"Moving: {src} → {dst}{desc}")

        if not self.dry_run:
            # Create parent directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Use git mv to preserve history
            self.run_command(["git", "mv", str(src_path), str(dst_path)])

        self.stats['files_moved'] += 1
        return True

    def rename_file(self, src: str, dst: str, description: str = ""):
        """Rename a file (same as move but semantically different)"""
        return self.move_file(src, dst, description)

    def move_core_modules(self):
        """Move core modules to new locations"""
        self.log("\n📁 Phase 2.1: Moving core modules...")

        # Parser modules
        self.move_file("src/pdf_parser.py", "src/parser/pdf_parser.py", "parser module")
        self.move_file("src/pdf_validator.py", "src/parser/pdf_validator.py", "parser module")
        self.move_file("src/pdf_image_extractor.py", "src/parser/pdf_image_extractor.py", "parser module")

        # Analysis modules (V3 → canonical)
        self.move_file("src/ai_analyzer_enhanced_v3.py", "src/analysis/ai_analyzer.py", "V3 → canonical")
        self.move_file("src/content_extractor_enhanced_v3.py", "src/analysis/content_extractor.py", "V3 → canonical")

        # Generation modules (V3 → canonical)
        self.move_file("src/ppt_generator_enhanced_v3.py", "src/generation/ppt_generator.py", "V3 → canonical")

        # Core modules
        self.move_file("src/cache_manager.py", "src/core/cache_manager.py", "core module")
        self.move_file("src/resilience.py", "src/core/resilience.py", "core module")
        self.move_file("src/progress_reporter.py", "src/core/progress_reporter.py", "core module")

        # Prompts
        self.move_file("src/prompts", "prompts", "prompts directory")

    def archive_legacy_versions(self):
        """Archive legacy version files"""
        self.log("\n📦 Phase 2.2: Archiving legacy versions...")

        # Archive old analyzer versions
        self.move_file("src/ai_analyzer.py", "archive/legacy/ai_analyzer_v1.py", "legacy v1")
        self.move_file("src/ai_analyzer_enhanced.py", "archive/legacy/ai_analyzer_enhanced.py", "legacy enhanced")

        # Archive old content extractor versions
        self.move_file("src/content_extractor.py", "archive/legacy/content_extractor_v1.py", "legacy v1")
        self.move_file("src/content_extractor_enhanced.py", "archive/legacy/content_extractor_enhanced.py", "legacy enhanced")

        # Archive old generator versions
        self.move_file("src/ppt_generator.py", "archive/legacy/ppt_generator_v1.py", "legacy v1")
        self.move_file("src/ppt_generator_enhanced.py", "archive/legacy/ppt_generator_enhanced.py", "legacy enhanced")

    def archive_experiments(self):
        """Archive experimental scripts"""
        self.log("\n🧪 Phase 2.3: Archiving experimental scripts...")

        # Archive all tools scripts except md_to_pptx.py
        tools_dir = self.root_dir / "tools"
        if tools_dir.exists():
            for tool_file in tools_dir.glob("*.py"):
                if tool_file.name != "md_to_pptx.py":
                    self.move_file(
                        f"tools/{tool_file.name}",
                        f"archive/experiments/{tool_file.name}",
                        "experiment"
                    )

    def reorganize_runtime(self):
        """Reorganize runtime data (using regular mv, not git mv)"""
        self.log("\n💾 Phase 2.4: Reorganizing runtime data...")

        # Move cache (not in git, use shutil)
        cache_dir = self.root_dir / "cache"
        if cache_dir.exists():
            runtime_cache = self.root_dir / "runtime" / "cache"
            if not runtime_cache.exists():
                if not self.dry_run:
                    runtime_cache.mkdir(parents=True, exist_ok=True)

            for cache_file in cache_dir.glob("*"):
                if cache_file.is_file():
                    src_path = cache_file
                    dst_path = runtime_cache / cache_file.name

                    self.log(f"Moving: cache/{cache_file.name} → runtime/cache/{cache_file.name}")

                    if not self.dry_run:
                        shutil.move(str(src_path), str(dst_path))
                    self.stats['files_moved'] += 1

        # Move logs (not in git, use shutil)
        logs_dir = self.root_dir / "logs"
        if logs_dir.exists():
            runtime_logs = self.root_dir / "runtime" / "logs"
            if not runtime_logs.exists():
                if not self.dry_run:
                    runtime_logs.mkdir(parents=True, exist_ok=True)

            for log_file in logs_dir.glob("*"):
                if log_file.is_file():
                    src_path = log_file
                    dst_path = runtime_logs / log_file.name

                    self.log(f"Moving: logs/{log_file.name} → runtime/logs/{log_file.name}")

                    if not self.dry_run:
                        shutil.move(str(src_path), str(dst_path))
                    self.stats['files_moved'] += 1

        # Rename output to outputs
        output_dir = self.root_dir / "output"
        if output_dir.exists():
            outputs_dir = self.root_dir / "outputs"
            if not outputs_dir.exists():
                self.log("Renaming: output → outputs")

                # Check if output is in git
                result = self.run_command(
                    ["git", "ls-files", "output/"],
                    check=False
                )

                if result.returncode == 0 and result.stdout.strip():
                    # Use git mv if output is tracked
                    if not self.dry_run:
                        self.run_command(["git", "mv", "output", "outputs"])
                else:
                    # Use shutil if not tracked
                    if not self.dry_run:
                        shutil.move(str(output_dir), str(outputs_dir))

    def update_imports_in_file(self, file_path: Path) -> bool:
        """Update imports in a single file"""
        if not file_path.exists():
            return False

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Import mapping
        import_mappings = [
            # Parser modules
            (r'from src\.pdf_parser import', 'from src.parser.pdf_parser import'),
            (r'from src\.pdf_validator import', 'from src.parser.pdf_validator import'),
            (r'from src\.pdf_image_extractor import', 'from src.parser.pdf_image_extractor import'),

            # Analysis modules
            (r'from src\.ai_analyzer import', 'from src.analysis.ai_analyzer import'),
            (r'from src\.ai_analyzer_enhanced_v3 import', 'from src.analysis.ai_analyzer import'),
            (r'from src\.ai_analyzer_enhanced import', 'from src.analysis.ai_analyzer import'),
            (r'from src\.content_extractor import', 'from src.analysis.content_extractor import'),
            (r'from src\.content_extractor_enhanced_v3 import', 'from src.analysis.content_extractor import'),
            (r'from src\.content_extractor_enhanced import', 'from src.analysis.content_extractor import'),

            # Generation modules
            (r'from src\.ppt_generator import', 'from src.generation.ppt_generator import'),
            (r'from src\.ppt_generator_enhanced_v3 import', 'from src.generation.ppt_generator import'),
            (r'from src\.ppt_generator_enhanced import', 'from src.generation.ppt_generator import'),

            # Core modules
            (r'from src\.cache_manager import', 'from src.core.cache_manager import'),
            (r'from src\.resilience import', 'from src.core.resilience import'),
            (r'from src\.progress_reporter import', 'from src.core.progress_reporter import'),
        ]

        # Apply all mappings
        for old_import, new_import in import_mappings:
            content = re.sub(old_import, new_import, content)

        # Check if content changed
        if content != original_content:
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.log(f"Updated imports in: {file_path.relative_to(self.root_dir)}")
            self.stats['imports_updated'] += 1
            return True

        return False

    def update_all_imports(self):
        """Update imports in all Python files"""
        self.log("\n🔗 Phase 3: Updating imports...")

        # Files to update
        files_to_update = []

        # CLI
        cli_main = self.root_dir / "cli" / "main.py"
        if cli_main.exists():
            files_to_update.append(cli_main)

        # Tests
        tests_dir = self.root_dir / "tests"
        if tests_dir.exists():
            files_to_update.extend(tests_dir.glob("*.py"))

        # Source files (if they reference each other)
        for src_dir in ["parser", "analysis", "generation", "core"]:
            module_dir = self.root_dir / "src" / src_dir
            if module_dir.exists():
                files_to_update.extend(module_dir.glob("*.py"))

        # Update each file
        for file_path in files_to_update:
            if file_path.name == "__init__.py":
                continue
            self.update_imports_in_file(file_path)

    def update_config(self):
        """Update configuration file"""
        self.log("\n⚙️  Phase 4: Updating configuration...")

        config_file = self.root_dir / "config.yaml"
        if not config_file.exists():
            self.log("config.yaml not found, skipping", "WARNING")
            return

        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Update paths
        replacements = [
            ('cache_dir: cache/', 'cache_dir: runtime/cache/'),
            ('output_dir: output/', 'output_dir: outputs/'),
        ]

        for old, new in replacements:
            content = content.replace(old, new)

        if content != original_content:
            if not self.dry_run:
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.log("Updated config.yaml paths")
        else:
            self.log("config.yaml already up to date")

    def update_gitignore(self):
        """Update .gitignore"""
        self.log("\n📝 Phase 4.2: Updating .gitignore...")

        gitignore_file = self.root_dir / ".gitignore"
        if not gitignore_file.exists():
            self.log(".gitignore not found, skipping", "WARNING")
            return

        with open(gitignore_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add new entries if not present
        new_entries = [
            "# Runtime data",
            "runtime/cache/",
            "runtime/logs/",
            "",
            "# Outputs",
            "outputs/slides/*.pptx",
            "outputs/images/*.png",
            "outputs/markdown/*.md",
        ]

        lines_to_add = []
        for entry in new_entries:
            if entry and entry not in content:
                lines_to_add.append(entry)

        if lines_to_add:
            if not self.dry_run:
                with open(gitignore_file, 'a', encoding='utf-8') as f:
                    f.write("\n\n# Added by refactor script\n")
                    for line in lines_to_add:
                        f.write(f"{line}\n")

            self.log(f"Added {len(lines_to_add)} entries to .gitignore")

    def cleanup_empty_dirs(self):
        """Remove empty directories"""
        self.log("\n🧹 Phase 6.1: Cleaning up empty directories...")

        dirs_to_check = [
            "cache",
            "logs",
            "tools",
            "src/prompts",
        ]

        for dir_path in dirs_to_check:
            full_path = self.root_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                # Check if directory is empty
                if not any(full_path.iterdir()):
                    self.log(f"Removing empty directory: {dir_path}")
                    if not self.dry_run:
                        full_path.rmdir()
                else:
                    self.log(f"Directory not empty, keeping: {dir_path}")

    def run_tests(self):
        """Run test suite"""
        if self.skip_tests:
            self.log("Skipping tests (as requested)", "WARNING")
            return True

        self.log("\n🧪 Phase 5: Running tests...")

        try:
            result = self.run_command(["python", "-m", "pytest", "tests/", "-v"], check=False)

            if result.returncode == 0:
                self.log("All tests passed!", "SUCCESS")
                return True
            else:
                self.log("Some tests failed!", "ERROR")
                self.log(result.stdout)
                self.log(result.stderr, "ERROR")
                return False

        except Exception as e:
            self.log(f"Failed to run tests: {e}", "ERROR")
            return False

    def verify_cli(self):
        """Verify CLI entry point"""
        self.log("\n🔍 Phase 5.2: Verifying CLI...")

        cli_main = self.root_dir / "cli" / "main.py"
        if not cli_main.exists():
            self.log("CLI main.py not found!", "ERROR")
            return False

        try:
            # Try importing CLI module
            result = self.run_command(
                ["python", "-c", "from cli.main import cli; print('CLI OK')"],
                check=False
            )

            if result.returncode == 0:
                self.log("CLI imports verified", "SUCCESS")
                return True
            else:
                self.log("CLI import failed!", "ERROR")
                self.log(result.stderr, "ERROR")
                return False

        except Exception as e:
            self.log(f"Failed to verify CLI: {e}", "ERROR")
            return False

    def print_summary(self):
        """Print migration summary"""
        self.log("\n" + "="*60, "SUCCESS")
        self.log("📊 MIGRATION SUMMARY", "SUCCESS")
        self.log("="*60, "SUCCESS")
        self.log(f"Directories created: {self.stats['dirs_created']}")
        self.log(f"Files moved: {self.stats['files_moved']}")
        self.log(f"Files renamed: {self.stats['files_renamed']}")
        self.log(f"Imports updated: {self.stats['imports_updated']}")
        self.log("="*60, "SUCCESS")

        if self.dry_run:
            self.log("\n🔍 This was a DRY RUN - no changes were made", "DRY_RUN")
            self.log("To execute the migration, run without --dry-run", "DRY_RUN")
        else:
            self.log("\n✅ Migration completed successfully!", "SUCCESS")
            self.log("\nNext steps:")
            self.log("1. Review the changes: git status")
            self.log("2. Run tests manually: pytest tests/ -v")
            self.log("3. Test CLI: python cli/main.py process -p papers/example.pdf")
            self.log("4. Commit changes: git commit -m 'refactor: consolidate to V3 pipeline'")

    def execute(self):
        """Execute the full migration"""
        self.log("🚀 Starting Repository Refactor...")
        self.log(f"Root directory: {self.root_dir}")

        if self.dry_run:
            self.log("🔍 DRY RUN MODE - No changes will be made\n", "DRY_RUN")

        try:
            # Phase 1: Preparation
            self.create_backup()
            self.create_directory_structure()

            # Phase 2: Migrate files
            self.move_core_modules()
            self.archive_legacy_versions()
            self.archive_experiments()
            self.reorganize_runtime()

            # Phase 3: Update imports
            self.update_all_imports()

            # Phase 4: Update configuration
            self.update_config()
            self.update_gitignore()

            # Phase 5: Testing
            tests_passed = self.run_tests()
            cli_ok = self.verify_cli()

            # Phase 6: Cleanup
            self.cleanup_empty_dirs()

            # Summary
            self.print_summary()

            if not self.dry_run:
                if tests_passed and cli_ok:
                    self.log("\n🎉 All checks passed! Migration successful!", "SUCCESS")
                    return 0
                else:
                    self.log("\n⚠️  Migration completed but some checks failed!", "WARNING")
                    self.log("Please review and fix issues before committing", "WARNING")
                    return 1

            return 0

        except Exception as e:
            self.log(f"\n❌ Migration failed: {e}", "ERROR")
            self.log("You can rollback using: git reset --hard pre-refactor-backup-*", "ERROR")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Refactor PaperReader repository to pipeline architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run (preview changes)
    python scripts/refactor_repository.py --dry-run

    # Execute migration
    python scripts/refactor_repository.py

    # Skip tests (not recommended)
    python scripts/refactor_repository.py --skip-tests
        """
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without executing them"
    )

    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests after migration"
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating git backup tag (not recommended)"
    )

    args = parser.parse_args()

    refactor = RepositoryRefactor(
        dry_run=args.dry_run,
        skip_tests=args.skip_tests,
        no_backup=args.no_backup
    )

    return refactor.execute()


if __name__ == "__main__":
    sys.exit(main())
