"""Audio playback via mpv."""

from __future__ import annotations

import subprocess

from .deps import require_binary
from .errors import DependencyError, PlaybackError


def play_audio(url: str) -> None:
    """Stream audio-only playback for ``url`` using mpv."""

    require_binary("mpv")

    command = [
        "mpv",
        "--no-video",
        "--quiet",
        "--force-window=no",
        "--ytdl-format=bestaudio/best",
        url,
    ]

    try:
        with subprocess.Popen(command) as proc:
            try:
                return_code = proc.wait()
            except KeyboardInterrupt:
                proc.terminate()
                proc.wait()
                raise PlaybackError("Playback interrupted by user") from None
    except FileNotFoundError as exc:  # pragma: no cover - guarded by require_binary
        raise DependencyError(str(exc)) from exc

    if return_code != 0:
        raise PlaybackError(f"mpv exited with status {return_code}")
