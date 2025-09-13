"""Progress tracking for n8n-lint validation."""

import time

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn, TimeElapsedColumn


class ProgressTracker:
    """Tracks and displays validation progress."""

    def __init__(self, plain_text: bool = False, show_progress: bool = True):
        self.plain_text = plain_text
        self.show_progress = show_progress
        self.console = Console(force_terminal=False, no_color=plain_text)

        # Progress tracking
        self.total_nodes: int = 0
        self.completed_nodes: int = 0
        self.current_node: str | None = None
        self.start_time: float | None = None
        self.end_time: float | None = None

        # Rich progress display
        self.progress: Progress | None = None
        self.task_id: TaskID | None = None

        if self.show_progress and not self.plain_text:
            self._setup_rich_progress()

    def _setup_rich_progress(self) -> None:
        """Setup Rich progress display."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            console=self.console,
            transient=False,
        )

    def start_validation(self, total_nodes: int, file_path: str = "") -> None:
        """Start validation progress tracking."""
        self.total_nodes = total_nodes
        self.completed_nodes = 0
        self.current_node = None
        self.start_time = time.time()
        self.end_time = None

        if self.show_progress:
            if self.plain_text:
                self.console.print(f"Starting validation of {total_nodes} nodes...")
            else:
                if self.progress is not None:
                    self.progress.start()
                    self.task_id = self.progress.add_task(f"Validating {file_path or 'workflow'}", total=total_nodes)

    def update_progress(self, node_name: str, node_type: str = "") -> None:
        """Update progress for current node."""
        self.current_node = node_name
        self.completed_nodes += 1

        if self.show_progress:
            if self.plain_text:
                self.console.print(f"Validating node {self.completed_nodes}/{self.total_nodes}: {node_name}")
            else:
                if self.progress and self.task_id is not None:
                    self.progress.update(
                        self.task_id,
                        completed=self.completed_nodes,
                        description=f"Validating {node_name} ({node_type})",
                    )

    def complete_validation(self) -> None:
        """Complete validation progress tracking."""
        self.end_time = time.time()

        if self.show_progress:
            if self.plain_text:
                elapsed = self.end_time - self.start_time if self.start_time else 0
                self.console.print(f"Validation completed in {elapsed:.2f}s")
            else:
                if self.progress and self.task_id is not None:
                    self.progress.update(self.task_id, completed=self.total_nodes, description="Validation complete")
                    # Give a moment to show completion
                    time.sleep(0.5)
                    self.progress.stop()

    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0

        end_time = self.end_time or time.time()
        return end_time - self.start_time

    def get_progress_percentage(self) -> float:
        """Get progress percentage."""
        if self.total_nodes == 0:
            return 0.0

        return (self.completed_nodes / self.total_nodes) * 100

    def is_complete(self) -> bool:
        """Check if validation is complete."""
        return self.completed_nodes >= self.total_nodes

    def get_status_message(self) -> str:
        """Get current status message."""
        if self.total_nodes == 0:
            return "No nodes to validate"

        if self.is_complete():
            elapsed = self.get_elapsed_time()
            return f"Validation complete ({self.total_nodes} nodes in {elapsed:.2f}s)"

        if self.current_node:
            return f"Validating {self.current_node} ({self.completed_nodes}/{self.total_nodes})"
        else:
            return f"Starting validation ({self.total_nodes} nodes)"

    def print_status(self) -> None:
        """Print current status."""
        if self.show_progress:
            self.console.print(self.get_status_message())
