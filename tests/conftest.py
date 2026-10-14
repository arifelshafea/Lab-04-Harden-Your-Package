import pytest

from tvsummary.models import TVShow


# Provide reusable sample TV shows for aggregation tests.
@pytest.fixture
def sample_shows():
    return [
        TVShow({
            "name": "Show A",
            "genres": ["Drama", "Comedy"],
            "language": "English",
            "rating": {"average": 8.0},
        }),
        TVShow({
            "name": "Show B",
            "genres": ["Drama"],
            "language": "English",
            "rating": {"average": 6.0},
        }),
        TVShow({
            "name": "Show C",
            "genres": ["Comedy"],
            "language": "Japanese",
            "rating": {"average": 9.0},
        }),
    ]