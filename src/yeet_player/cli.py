"""Entry point for the Yeet Player CLI."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel

from .errors import DependencyError, PlaybackError, QuitRequested, SearchError
from .models import SearchResult
from .player import play_audio
from .search import search_youtube
from .ui import prompt_query, prompt_selection, show_results

PAGE_SIZE = 10


def main() -> None:
    console = Console()
    console.print(
        Panel(
            "Search YouTube and stream audio via mpv. Type 'q' at any prompt to exit.",
            title="Yeet Player",
        )
    )

    while True:
        query = prompt_query(console)
        if query is None:
            console.print("Goodbye!")
            sys.exit(0)
        if not query:
            continue

        results: list[SearchResult] = []
        exhausted = False
        page = 0

        while True:
            needed = (page + 1) * PAGE_SIZE
            if not exhausted and needed > len(results):
                try:
                    fetched = search_youtube(query, limit=needed)
                except DependencyError as err:
                    console.print(f"[red]Dependency error:[/] {err}")
                    sys.exit(1)
                except SearchError as err:
                    console.print(f"[red]Search failed:[/] {err}")
                    break

                if not fetched:
                    console.print("[yellow]No results. Try another search.[/]")
                    break

                exhausted = len(fetched) < needed
                results = fetched

            start = page * PAGE_SIZE
            page_items = results[start : start + PAGE_SIZE]

            if not page_items:
                if page == 0:
                    console.print("[yellow]No results. Try another search.[/]")
                    break
                console.print("[yellow]No more results in that direction.[/]")
                page = max(0, page - 1)
                continue

            has_prev = page > 0
            end_index = start + len(page_items)
            has_next = (not exhausted) or (end_index < len(results))

            show_results(
                console,
                page_items,
                page=page,
                page_size=PAGE_SIZE,
                total_known=len(results),
                more_available=has_next,
            )

            try:
                action, index = prompt_selection(
                    console,
                    total=len(page_items),
                    offset=start,
                    has_prev=has_prev,
                    has_next=has_next,
                )
            except QuitRequested:
                console.print("Goodbye!")
                sys.exit(0)

            if action == "search":
                break
            if action == "next":
                if has_next:
                    page += 1
                continue
            if action == "prev":
                if has_prev:
                    page -= 1
                continue
            if action == "play" and index is not None:
                choice = results[start + index]
                console.print(
                    f"Playing: [bold]{choice.title}[/] — {choice.channel} ({choice.duration})"
                )

                try:
                    play_audio(choice.url)
                except DependencyError as err:
                    console.print(f"[red]Dependency error:[/] {err}")
                    sys.exit(1)
                except PlaybackError as err:
                    console.print(f"[red]Playback issue:[/] {err}")

                console.print("[green]Playback finished.[/]")
