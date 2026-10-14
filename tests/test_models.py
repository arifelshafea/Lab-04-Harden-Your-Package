import pytest
from tvsummary.models import TVShow


# Test that a valid TV show record stores its values correctly.
def test_valid_record():
    data = {
        "name": "Test Show",
        "genres": ["Drama", "Comedy"],
        "language": "English",
        "rating": {"average": 8.5},
    }

    show = TVShow(data)

    assert show.name == "Test Show"
    assert show.genres == ["Drama", "Comedy"]
    assert show.language == "English"
    assert show.rating == 8.5


# Test that missing values are replaced with appropriate defaults.
def test_missing_values():
    data = {
        "name": None,
        "genres": None,
        "language": None,
        "rating": None,
    }

    show = TVShow(data)

    assert show.name == "Unknown"
    assert show.genres == []
    assert show.language is None
    assert show.rating is None


# Test that malformed genres and ratings are handled safely.
def test_malformed_values():
    data = {
        "name": "Another Show",
        "genres": "Drama",
        "language": "",
        "rating": {"average": "Excellent"},
    }

    show = TVShow(data)

    assert show.genres == []
    assert show.language is None
    assert show.rating is None

# Test how TVShow handles different genre inputs.
@pytest.mark.parametrize(
    "genres, expected",
    [
        (["Drama", "Comedy"], ["Drama", "Comedy"]),
        (None, []),
        ("Drama", []),
        ([], []),
    ],
)
def test_genres_with_different_inputs(genres, expected):
    data = {
        "name": "Test Show",
        "genres": genres,
    }

    show = TVShow(data)

    assert show.genres == expected
