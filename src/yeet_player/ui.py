"""User interaction helpers."""

from __future__ import annotations

import sys

from typing import Literal, Tuple

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


def show_results(
    console: Console,
    results: list[SearchResult],
    *,
    page: int,
    page_size: int,
    total_known: int,
    more_available: bool,
) -> None:
    start_index = page * page_size
    showing_end = start_index + len(results)
    more_label = "+" if more_available else ""
    title = (
        f"Search Results — Page {page + 1} "
        f"[{start_index + 1}-{showing_end} of {total_known}{more_label}]"
    )

    table = Table(title=title, show_lines=False)
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Channel", style="magenta")
    table.add_column("Duration", justify="right", style="green")

    for index, item in enumerate(results, start=start_index + 1):
        table.add_row(str(index), item.title, item.channel, item.duration)

    console.print(table)


SelectionAction = Literal["play", "next", "prev", "search"]


def prompt_selection(
    console: Console,
    *,
    total: int,
    offset: int,
    has_prev: bool,
    has_next: bool,
) -> Tuple[SelectionAction, int | None]:
    """Return the chosen action and (optionally) the index on the page."""

    prompt_text = "Pick a number to play, 'n' next page, 'p' previous, enter=search again, q=quit: "

    while True:
        try:
            raw = _read_line(prompt_text)
        except QuitRequested:
            raise

        choice = raw.strip().lower()
        if choice in {"", "s", "search", "back"}:
            return "search", None
        if choice in {"q", "quit", "exit"}:
            raise QuitRequested
        if choice in {"n", "next"}:
            if has_next:
                return "next", None
            console.print("[yellow]You are already on the last page.[/]")
            continue
        if choice in {"p", "prev", "previous"}:
            if has_prev:
                return "prev", None
            console.print("[yellow]You are already on the first page.[/]")
            continue
        if choice.isdigit():
            absolute_index = int(choice) - 1
            if offset <= absolute_index < offset + total:
                return "play", absolute_index - offset
        console.print(
            "Invalid selection. Choose a visible number, use 'n'/'p' to navigate, or enter to search again."
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
