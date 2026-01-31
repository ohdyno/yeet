"""YouTube search integration via yt-dlp."""

from __future__ import annotations

import json
import subprocess
from typing import Iterable

from .deps import require_binary
from .errors import DependencyError, SearchError
from .models import SearchResult


def search_youtube(query: str, limit: int = 10) -> list[SearchResult]:
    """Return the top ``limit`` results for ``query`` using yt-dlp."""

    if not query.strip():
        return []

    require_binary("yt-dlp")

    command = [
        "yt-dlp",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        "--default-search",
        "ytsearch",
        "--flat-playlist",
        f"ytsearch{limit}:{query}",
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - guarded by require_binary
        raise DependencyError(str(exc)) from exc
    except (
        subprocess.CalledProcessError
    ) as exc:  # pragma: no cover - depends on network
        stderr = exc.stderr.strip() if exc.stderr else "yt-dlp failed"
        raise SearchError(stderr) from exc

    entries = _parse_lines(result.stdout.splitlines())
    return list(entries)


def _parse_lines(lines: Iterable[str]) -> Iterable[SearchResult]:
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        data = json.loads(raw)
        title = data.get("title") or data.get("fulltitle") or "Unknown title"
        channel = data.get("channel") or data.get("uploader") or "Unknown channel"
        duration = _format_duration(data.get("duration"), data.get("duration_string"))
        url = _extract_url(data)
        yield SearchResult(title=title, channel=channel, duration=duration, url=url)


def _format_duration(raw_seconds: int | None, raw_string: str | None) -> str:
    if raw_string:
        return raw_string
    if not raw_seconds:
        return "?"
    minutes, seconds = divmod(int(raw_seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:d}:{seconds:02d}"


def _extract_url(data: dict[str, object]) -> str:
    url = (
        data.get("original_url")
        or data.get("webpage_url")
        or data.get("url")
        or data.get("id")
    )
    if isinstance(url, str) and url.startswith("http"):
        return url
    if isinstance(url, str):
        return f"https://www.youtube.com/watch?v={url}"
    raise SearchError("yt-dlp response missing URL")
