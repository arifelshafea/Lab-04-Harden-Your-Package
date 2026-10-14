# Base exception for errors raised by the tvsummary package.
class TVSummaryError(Exception):
    """Base exception for all tvsummary package errors."""


# Raised when downloading TV show records fails.
class DownloadError(TVSummaryError):
    """Raised when TV show data cannot be downloaded."""


# Raised when the configuration is missing or invalid.
class ConfigurationError(TVSummaryError):
    """Raised when the application configuration is invalid."""


# Raised when saving output files fails.
class OutputError(TVSummaryError):
    """Raised when the application cannot write its output files."""
