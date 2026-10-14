import requests

from .exceptions import DownloadError
from .models import TVShow


# Download TV show records from the configured API.
class TVShowSource:
    """Fetch TV show records from the configured API."""

    def __init__(self, url: str, timeout: int) -> None:
        """Create a data source with a URL and timeout."""
        self.url = url
        self.timeout = timeout

    def fetch(self) -> list[TVShow]:
        """Download records and return cleaned TVShow objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_records = response.json()

        except (requests.RequestException, ValueError) as error:
            raise DownloadError(f"Could not download TV show data: {error}") from error

        return [TVShow(record) for record in raw_records]
