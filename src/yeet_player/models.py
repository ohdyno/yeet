"""Shared data structures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SearchResult:
    """Represents an item returned from a YouTube search."""

    title: str
    channel: str
    duration: str
    url: str
