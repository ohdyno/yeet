"""Dependency helpers."""

from __future__ import annotations

import shutil

from .errors import DependencyError


def require_binary(name: str) -> None:
    """Ensure the given binary exists on PATH."""

    if shutil.which(name) is None:
        raise DependencyError(
            f"Missing required executable '{name}'. Install it and ensure it is on your PATH."
        )
