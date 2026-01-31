# YouTube Audio CLI Player

## Goal
- Build a personal CLI music player that searches YouTube, shows selectable hits, and streams audio-only playback.
- Keep the tool stateless with no persisted data; every run is a fresh interactive shell.
- Rely on existing system utilities (`yt-dlp`, `mpv`) and manage Python code via `uv` (wrapped by `mise`).

## Tooling & Dependencies
- `uv` manages the Python project: initialization (`uv init --src src`), dependency installs (`uv add ...`), and execution (`uv run ...`).
- `.mise.toml` will pin required tool versions and expose handy tasks (e.g., `mise run dev` → `uv run python -m yeet_player`).
- External binaries required at runtime: `yt-dlp` for searching/URL resolution and `mpv` (or compatible player) for audio output.

## Proposed Structure
- `src/yeet_player/cli.py`: entry point with the interactive loop.
- `src/yeet_player/search.py`: wraps `yt-dlp --dump-json "ytsearchN:<query>"` and parses results.
- `src/yeet_player/player.py`: launches `mpv --no-video <url>` (handles stop/cancel flow).
- `src/yeet_player/ui.py`: presentation/helpers using `prompt_toolkit` or similar for numbered selection lists.
- `pyproject.toml` + `uv.lock`: generated/maintained by `uv`.

## User Flow
1. Launch via `uv run python -m yeet_player` (or a dedicated command exposed through `mise`).
2. Prompt for a search term; fetch top ~10 results using `yt-dlp` and show title, channel, duration.
3. User selects an index; the player streams audio-only via `mpv` until completion or cancellation.
4. After playback, the shell loops back for additional searches or accepts a quit command.

## Error Handling & UX Notes
- Check for presence of `yt-dlp` and `mpv` at startup; surface actionable instructions if missing.
- Handle empty search results, invalid selections, and subprocess failures with clear messages.
- Keep the CLI lightweight but provide room to extend (queues, skip controls) after MVP.

## Next Steps
1. Initialize the Python project with `uv` and record the toolchain in `.mise.toml`.
2. Implement the modules listed above with robust subprocess handling and interactive prompts.
3. Document installation steps (installing `uv`, `yt-dlp`, `mpv`) and usage examples in this README.
