"""Custom exceptions for the Yeet Player CLI."""


class DependencyError(RuntimeError):
    """Raised when a required external dependency is missing."""


class SearchError(RuntimeError):
    """Raised when YouTube search fails."""


class PlaybackError(RuntimeError):
    """Raised when audio playback fails or is interrupted."""


class QuitRequested(Exception):
    """Raised when the user explicitly asks to quit the CLI."""
