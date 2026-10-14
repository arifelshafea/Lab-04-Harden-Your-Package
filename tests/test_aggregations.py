import pytest

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerGenre,
    UniqueLanguages,
)

from tvsummary.aggregations import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    UniqueLanguages,
)


# Test that the number of shows in each genre is calculated correctly.
def test_shows_per_genre(sample_shows):
    result = ShowsPerGenre().compute(sample_shows)

    assert result == {"Drama": 2, "Comedy": 2}


# Test that the average rating for each language is calculated correctly.
def test_average_rating_by_language(sample_shows):
    result = AverageRatingByLanguage().compute(sample_shows)

    assert result == {"English": 7.0, "Japanese": 9.0}


# Test that unique languages are returned in alphabetical order.
def test_unique_languages(sample_shows):
    result = UniqueLanguages().compute(sample_shows)

    assert result == ["English", "Japanese"]

# Test that shows without ratings are excluded from the average.
def test_average_rating_ignores_missing_ratings():
    from tvsummary.models import TVShow

    shows = [
        TVShow({
            "name": "Rated Show",
            "language": "English",
            "rating": {"average": 8.0},
        }),
        TVShow({
            "name": "Unrated Show",
            "language": "English",
            "rating": {"average": None},
        }),
    ]

    result = AverageRatingByLanguage().compute(shows)

    assert result == {"English": 8.0}

# Test that the base aggregation raises an error when compute is not implemented.
def test_base_aggregation_raises_error():
    aggregation = Aggregation("test")

    with pytest.raises(
        NotImplementedError,
        match=r"Subclasses must implement compute\(\)",
    ):
        aggregation.compute([])