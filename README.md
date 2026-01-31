# YouTube Audio CLI Player

Interactive CLI that lets you search YouTube, pick a result, and stream audio-only playback through `mpv`. Everything runs locally, stays stateless, and leans on `uv` + `mise` for painless dependency management.

## Features
- Prompt-driven shell built with `prompt_toolkit` (type queries, navigate with simple inputs).
- Rich-formatted results table showing title, channel, and duration for the top matches.
- Streams audio via `mpv --no-video` so you get music without video windows.
- Graceful handling of missing binaries, empty searches, cancelled playback, and other runtime hiccups.
- Paginated results with `n` / `p` controls so you can go beyond the first 10 matches.
- Includes a single-file launcher (`./yeet-player`) so you can run the tool directly.

## Prerequisites
- [`mise`](https://mise.jdx.dev) for toolchain orchestration.
- [`uv`](https://astral.sh/blog/uv-unified-python-management) (installed automatically by `mise run install` or manually via their install script).
- System binaries:
  - `yt-dlp` (macOS: `brew install yt-dlp`).
  - `mpv` (macOS: `brew install mpv`).

## Setup
```bash
# install tool versions and sync the virtualenv
mise install
mise run sync
```

Behind the scenes `mise` pins Python 3.12 and the latest `uv`. `uv sync` creates `.venv` and installs the Python dependencies (`prompt_toolkit`, `rich`).

## Usage
```bash
# start the interactive player
mise run dev

# or, if you prefer raw uv
uv run python -m yeet_player

# or run the single-file launcher
./yeet-player
```

The launcher automatically re-execs inside `.venv` (created via `mise run sync`) so dependencies from `uv` are available.

Flow:
1. Enter a search phrase (e.g., `lofi hip hop`).
2. Review the numbered list of results; press `n` / `p` to move between pages.
3. Pick any visible track number (the numbering is global) to stream audio via `mpv`.
4. Press enter to launch a new search or `q` to quit at any prompt.

## Project Structure
- `pyproject.toml` / `uv.lock` — project + dependency metadata managed by `uv`.
- `.mise.toml` — toolchain pinning + helper tasks.
- `src/yeet_player/cli.py` — program entry point and control loop.
- `src/yeet_player/search.py` — wraps `yt-dlp` to fetch search hits.
- `src/yeet_player/ui.py` — user prompts and pretty result tables.
- `src/yeet_player/player.py` — audio playback through `mpv`.
- `src/yeet_player/errors.py` / `deps.py` / `models.py` — shared plumbing.

## Future Enhancements
- Queueing and skipping tracks without re-running searches.
- Configurable result counts and output verbosity.
- Optional caching of recent searches.
