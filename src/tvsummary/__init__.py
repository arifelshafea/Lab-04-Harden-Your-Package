from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerGenre,
    UniqueLanguages,
)
from .exceptions import (
    ConfigurationError,
    DownloadError,
    OutputError,
    TVSummaryError,
)
from .models import TVShow
from .report import build_summary, write_summary
from .sources import TVShowSource

# Define the public classes and functions exported by the package.
__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "ShowsPerGenre",
    "UniqueLanguages",
    "TVShow",
    "build_summary",
    "write_summary",
    "TVSummaryError",
    "DownloadError",
    "ConfigurationError",
    "OutputError",
    "TVShowSource",
]
