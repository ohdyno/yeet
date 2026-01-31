"""User interaction helpers."""

from __future__ import annotations

import sys

from prompt_toolkit import prompt
from rich.console import Console
from rich.table import Table

from .errors import QuitRequested
from .models import SearchResult


def prompt_query(console: Console) -> str | None:
    """Ask the user for a search term. Returns ``None`` to quit."""

    try:
        value = _read_line("Search YouTube (q to quit): ")
    except QuitRequested:
        return None

    value = value.strip()
    if not value:
        console.print("Enter a search phrase or type 'q' to quit.")
        return ""

    if value.lower() in {"q", "quit", "exit"}:
        return None

    return value


def show_results(console: Console, results: list[SearchResult]) -> None:
    table = Table(title="Search Results", show_lines=False)
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Channel", style="magenta")
    table.add_column("Duration", justify="right", style="green")

    for index, item in enumerate(results, start=1):
        table.add_row(str(index), item.title, item.channel, item.duration)

    console.print(table)


def prompt_selection(console: Console, total: int) -> int | None:
    """Return zero-based index of the chosen result or ``None`` to search again."""

    while True:
        try:
            raw = _read_line("Pick a track (enter=search again, q=quit): ")
        except QuitRequested:
            raise

        choice = raw.strip().lower()
        if choice in {"", "b", "back"}:
            return None
        if choice in {"q", "quit", "exit"}:
            raise QuitRequested
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < total:
                return index
        console.print(
            "Invalid selection. Choose a number from the list or press enter to search again."
        )


def _read_line(message: str) -> str:
    """Return a line of input, supporting both TTY and non-TTY environments."""

    if sys.stdin.isatty():
        try:
            return prompt(message)
        except EOFError as exc:  # pragma: no cover - interactive only
            raise QuitRequested from exc
        except KeyboardInterrupt as exc:  # pragma: no cover - interactive only
            raise QuitRequested from exc

    # Fallback for non-interactive (e.g., tests, CI)
    try:
        return input(message)
    except EOFError as exc:  # pragma: no cover - interactive only
        raise QuitRequested from exc
    except KeyboardInterrupt as exc:  # pragma: no cover - interactive only
        raise QuitRequested from exc
