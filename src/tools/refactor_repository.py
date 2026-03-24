#!/usr/bin/env python3
"""Normalize the PaperReader repository to the canonical structure.

Usage:
    python tools/refactor_repository.py [--dry-run] [--skip-checks] [--no-backup]
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


class RepositoryRefactor:
    """Apply the repository normalization steps safely."""

    ACTIVE_REFERENCE_PATHS = [
        "README.md",
        "CLAUDE.md",
        "config.yaml",
        ".gitignore",
        ".claude/settings.local.json",
        "cli",
        "src",
        "tools",
        "examples",
        "docs/architecture",
        "docs/testing",
        "docs/user-guide",
        "scripts/README.md",
    ]

    DOC_DIRS_TO_ARCHIVE = [
        "archived",
        "changelogs",
        "project",
        "refactor",
        "features",
    ]

    def __init__(self, dry_run: bool = False, skip_checks: bool = False, no_backup: bool = False):
        self.dry_run = dry_run
        self.skip_checks = skip_checks
        self.no_backup = no_backup
        self.root_dir = Path(__file__).resolve().parent.parent
        self.stats = {
            "dirs_created": 0,
            "files_moved": 0,
            "files_removed": 0,
            "references_updated": 0,
            "conflicts_skipped": 0,
        }

    def log(self, message: str, level: str = "INFO") -> None:
        prefix = {
            "INFO": "[INFO]",
            "SUCCESS": "[OK]",
            "WARNING": "[WARN]",
            "ERROR": "[ERROR]",
            "DRY_RUN": "[DRY-RUN]",
        }[level]
        if self.dry_run and level == "INFO":
            prefix = "[DRY-RUN]"
        print(f"{prefix} {message}")

    def run_command(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        if self.dry_run:
            self.log(f"Would run: {' '.join(cmd)}", "DRY_RUN")
            return subprocess.CompletedProcess(cmd, 0, "", "")

        result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"Command failed: {' '.join(cmd)}")
        return result

    def create_backup(self) -> None:
        if self.no_backup:
            self.log("Skipping backup tag creation", "WARNING")
            return

        timestamp = subprocess.run(
            ["date", "+%Y%m%d-%H%M%S"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        tag_name = f"pre-refactor-backup-{timestamp}"
        self.run_command(["git", "tag", "-a", tag_name, "-m", "Backup before repository normalization"])
        self.log(f"Created backup tag: {tag_name}", "SUCCESS")

    def ensure_directories(self) -> None:
        self.log("Ensuring canonical directories exist")
        for rel_path in [
            "runtime/cache",
            "runtime/logs",
            "outputs/slides",
            "outputs/images",
            "outputs/markdown",
            "outputs/scripts",
            "outputs/charts",
            "outputs/plans",
            "src/prompts",
            "archive/docs",
        ]:
            full_path = self.root_dir / rel_path
            if full_path.exists():
                continue
            if not self.dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
            self.stats["dirs_created"] += 1
            self.log(f"Created directory: {rel_path}")

        init_file = self.root_dir / "src/prompts/__init__.py"
        if not init_file.exists():
            if not self.dry_run:
                init_file.write_text('"""Prompt templates for PaperReader pipelines."""\n', encoding="utf-8")
            self.log("Created src/prompts/__init__.py")

    def is_git_tracked(self, path: Path) -> bool:
        rel_path = str(path.relative_to(self.root_dir))
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", rel_path],
            cwd=self.root_dir,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def remove_file(self, path: Path) -> None:
        rel_path = str(path.relative_to(self.root_dir))
        if self.dry_run:
            self.log(f"Would remove file: {rel_path}", "DRY_RUN")
        elif self.is_git_tracked(path):
            self.run_command(["git", "rm", "-f", rel_path])
        else:
            path.unlink()
        self.stats["files_removed"] += 1

    def remove_empty_dir(self, path: Path) -> None:
        if not path.exists() or not path.is_dir() or any(path.iterdir()):
            return
        rel_path = str(path.relative_to(self.root_dir))
        if self.dry_run:
            self.log(f"Would remove empty directory: {rel_path}", "DRY_RUN")
        else:
            path.rmdir()

    def files_identical(self, left: Path, right: Path) -> bool:
        return filecmp.cmp(left, right, shallow=False)

    def move_file(self, src: Path, dst: Path) -> None:
        src_rel = str(src.relative_to(self.root_dir))
        dst_rel = str(dst.relative_to(self.root_dir))
        if self.dry_run:
            self.log(f"Would move {src_rel} -> {dst_rel}", "DRY_RUN")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if self.is_git_tracked(src):
                self.run_command(["git", "mv", src_rel, dst_rel])
            else:
                shutil.move(str(src), str(dst))
        self.stats["files_moved"] += 1

    def merge_directory(self, src: Path, dst: Path) -> None:
        if not src.exists():
            return
        if not dst.exists() and not self.dry_run:
            dst.mkdir(parents=True, exist_ok=True)

        for item in sorted(src.iterdir(), key=lambda p: p.name):
            target = dst / item.name
            if item.is_dir():
                self.merge_directory(item, target)
                self.remove_empty_dir(item)
                continue

            if target.exists():
                if self.files_identical(item, target):
                    self.log(f"Removing duplicate file: {item.relative_to(self.root_dir)}")
                    self.remove_file(item)
                else:
                    self.stats["conflicts_skipped"] += 1
                    self.log(
                        f"Conflict detected, leaving source in place: {item.relative_to(self.root_dir)} vs {target.relative_to(self.root_dir)}",
                        "WARNING",
                    )
                continue

            self.move_file(item, target)

        self.remove_empty_dir(src)

    def merge_runtime_and_outputs(self) -> None:
        self.log("Merging legacy runtime and output directories")
        self.merge_directory(self.root_dir / "cache", self.root_dir / "runtime/cache")
        self.merge_directory(self.root_dir / "logs", self.root_dir / "runtime/logs")
        self.merge_directory(self.root_dir / "output", self.root_dir / "outputs")

    def move_prompt_modules(self) -> None:
        self.log("Moving prompt modules into src/prompts")
        prompts_dir = self.root_dir / "prompts"
        target_dir = self.root_dir / "src/prompts"
        if not prompts_dir.exists():
            return
        for prompt_file in sorted(prompts_dir.glob("*.py")):
            target = target_dir / prompt_file.name
            if target.exists():
                if self.files_identical(prompt_file, target):
                    self.log(f"Removing duplicate prompt file: prompts/{prompt_file.name}")
                    self.remove_file(prompt_file)
                else:
                    self.stats["conflicts_skipped"] += 1
                    self.log(f"Conflict detected for prompt file: {prompt_file.name}", "WARNING")
            else:
                self.move_file(prompt_file, target)
        self.remove_empty_dir(prompts_dir)

    def archive_doc_directories(self) -> None:
        self.log("Archiving non-canonical docs directories")
        docs_root = self.root_dir / "docs"
        archive_root = self.root_dir / "archive/docs"
        for name in self.DOC_DIRS_TO_ARCHIVE:
            src = docs_root / name
            dst = archive_root / name
            if not src.exists():
                continue
            self.merge_directory(src, dst)
            self.remove_empty_dir(src)

    def iter_active_reference_files(self) -> Iterable[Path]:
        for rel_path in self.ACTIVE_REFERENCE_PATHS:
            full_path = self.root_dir / rel_path
            if not full_path.exists():
                continue
            if full_path.is_file():
                yield full_path
                continue
            for pattern in ("*.py", "*.md", "*.json", "*.yaml", "*.yml"):
                yield from full_path.rglob(pattern)

    def update_active_references(self) -> None:
        self.log("Updating active path references")
        replacements = [
            ("python scripts/refactor_repository.py", "python tools/refactor_repository.py"),
            ("scripts/refactor_repository.py", "tools/refactor_repository.py"),
            ("prompts/", "src/prompts/"),
            ("output/", "outputs/"),
            ("cache/", "runtime/cache/"),
            ("logs/", "runtime/logs/"),
        ]

        for file_path in sorted(set(self.iter_active_reference_files())):
            if ".claude/worktrees" in str(file_path):
                continue
            original = file_path.read_text(encoding="utf-8")
            updated = original
            for old, new in replacements:
                updated = updated.replace(old, new)
            updated = updated.replace("runtime/runtime/cache/", "runtime/cache/")
            updated = updated.replace("runtime/runtime/logs/", "runtime/logs/")
            updated = updated.replace("src/src/prompts/", "src/prompts/")
            updated = updated.replace("tools/tools/refactor_repository.py", "tools/refactor_repository.py")
            updated = updated.replace("outputss/", "outputs/")
            if updated == original:
                continue
            rel_path = file_path.relative_to(self.root_dir)
            if self.dry_run:
                self.log(f"Would update references in: {rel_path}", "DRY_RUN")
            else:
                file_path.write_text(updated, encoding="utf-8")
            self.stats["references_updated"] += 1

    def cleanup_empty_directories(self) -> None:
        self.log("Cleaning up empty legacy directories")
        for rel_path in [
            "cache",
            "logs",
            "output",
            "prompts",
            "scripts",
            "docs/archived",
            "docs/changelogs",
            "docs/project",
            "docs/refactor",
            "docs/features",
        ]:
            self.remove_empty_dir(self.root_dir / rel_path)

    def run_checks(self) -> bool:
        if self.skip_checks:
            self.log("Skipping checks", "WARNING")
            return True

        self.log("Running verification commands")
        commands = [
            ["python", "-c", "from src.cli.main import cli; print('src.cli.main OK')"],
            ["python", "-c", "from src.prompts.slide_planning_prompt import SLIDE_PLANNING_PROMPT; print('src.prompts OK')"],
            ["python", "-m", "src.cli.main", "--help"],
            ["python", "-m", "pytest", "tests/"],
        ]
        ok = True
        for cmd in commands:
            result = self.run_command(cmd, check=False)
            if result.returncode == 0:
                self.log(f"Check passed: {' '.join(cmd)}", "SUCCESS")
            else:
                ok = False
                self.log(f"Check failed: {' '.join(cmd)}", "ERROR")
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
        return ok

    def print_summary(self) -> None:
        print("\nNormalization summary")
        for key, value in self.stats.items():
            print(f"- {key.replace('_', ' ')}: {value}")

    def execute(self) -> int:
        self.log(f"Repository root: {self.root_dir}")
        try:
            self.create_backup()
            self.ensure_directories()
            self.merge_runtime_and_outputs()
            self.move_prompt_modules()
            self.archive_doc_directories()
            self.update_active_references()
            checks_ok = self.run_checks()
            self.cleanup_empty_directories()
            self.print_summary()
            return 0 if checks_ok else 1
        except Exception as exc:
            self.log(str(exc), "ERROR")
            return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize the PaperReader repository to the canonical structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python tools/refactor_repository.py --dry-run
    python tools/refactor_repository.py
    python tools/refactor_repository.py --skip-checks
""",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--skip-checks", action="store_true", help="Skip pytest and CLI verification")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating a git backup tag")
    args = parser.parse_args()

    refactor = RepositoryRefactor(
        dry_run=args.dry_run,
        skip_checks=args.skip_checks,
        no_backup=args.no_backup,
    )
    return refactor.execute()


if __name__ == "__main__":
    sys.exit(main())
