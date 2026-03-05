"""
Progress Reporter for PaperReader

Provides rich progress bars and status updates
"""

from typing import Optional
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint


class ProgressReporter:
    """Handles progress reporting with rich UI"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.console = Console()
        self.progress: Optional[Progress] = None
        self.current_task = None

    def start(self, total_steps: int = 100, description: str = "Processing"):
        """Start progress tracking"""
        if not self.verbose:
            return

        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console
        )
        self.progress.start()
        self.current_task = self.progress.add_task(description, total=total_steps)

    def update(self, advance: int = 1, description: Optional[str] = None):
        """Update progress"""
        if not self.verbose or not self.progress or self.current_task is None:
            return

        if description:
            self.progress.update(self.current_task, description=description)

        self.progress.advance(self.current_task, advance)

    def stop(self, success: bool = True, message: Optional[str] = None):
        """Stop progress tracking"""
        if not self.verbose or not self.progress:
            return

        if self.current_task is not None:
            self.progress.update(self.current_task, completed=100)

        self.progress.stop()

        if message:
            if success:
                self.success(message)
            else:
                self.error(message)

    def info(self, message: str):
        """Display info message"""
        if self.verbose:
            rprint(f"[blue]ℹ[/blue] {message}")

    def success(self, message: str):
        """Display success message"""
        if self.verbose:
            rprint(f"[green]✓[/green] {message}")

    def warning(self, message: str):
        """Display warning message"""
        if self.verbose:
            rprint(f"[yellow]⚠[/yellow] {message}")

    def error(self, message: str):
        """Display error message"""
        if self.verbose:
            rprint(f"[red]✗[/red] {message}")

    def show_panel(self, title: str, content: str, style: str = "blue"):
        """Display a panel with content"""
        if self.verbose:
            panel = Panel(content, title=title, border_style=style)
            self.console.print(panel)

    def show_summary(self, stats: dict):
        """Display processing summary"""
        if not self.verbose:
            return

        summary_lines = [
            f"Papers Processed: {stats.get('papers_processed', 0)}",
            f"Papers Failed: {stats.get('papers_failed', 0)}",
            f"Total Time: {stats.get('total_time', 'N/A')}",
            f"Cache Hits: {stats.get('cache_hits', 0)}",
            f"Estimated Cost: ${stats.get('estimated_cost', 0):.2f}",
        ]

        self.show_panel("Processing Summary", "\n".join(summary_lines), style="green")


class SilentReporter:
    """Silent reporter for non-verbose mode"""

    def __init__(self):
        pass

    def start(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def success(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

    def show_panel(self, *args, **kwargs):
        pass

    def show_summary(self, *args, **kwargs):
        pass


def get_reporter(verbose: bool = True):
    """Factory function to get appropriate reporter"""
    return ProgressReporter(verbose) if verbose else SilentReporter()
