import requests

from .config import SOURCE_URL, TIMEOUT
from .models import TVShow


class DownloadError(Exception):
    """Represent an error that occurs while downloading TV show data."""


# Download TV show records from the API
class TVShowSource:
    """Fetch TV show records from the configured API."""

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        """Create a data source with a URL and timeout."""
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download records and return cleaned TVShow objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise DownloadError(str(error)) from error

        raw_records = response.json()

        return [TVShow(record) for record in raw_records]
