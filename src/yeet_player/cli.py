"""Entry point for the Yeet Player CLI."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel

from .errors import DependencyError, PlaybackError, QuitRequested, SearchError
from .player import play_audio
from .search import search_youtube
from .ui import prompt_query, prompt_selection, show_results


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

        try:
            results = search_youtube(query)
        except DependencyError as err:
            console.print(f"[red]Dependency error:[/] {err}")
            sys.exit(1)
        except SearchError as err:
            console.print(f"[red]Search failed:[/] {err}")
            continue

        if not results:
            console.print("[yellow]No results. Try another search.[/]")
            continue

        show_results(console, results)

        try:
            selection = prompt_selection(console, len(results))
        except QuitRequested:
            console.print("Goodbye!")
            sys.exit(0)

        if selection is None:
            continue

        choice = results[selection]
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
