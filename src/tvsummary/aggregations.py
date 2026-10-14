from .models import TVShow


# Base class for all summary calculations
class Aggregation:
    """Base class for an aggregation performed on TV show records."""

    def __init__(self, name: str) -> None:
        """Create an aggregation with a name."""
        self.name = name

    def compute(
        self, records: list[TVShow]
    ) -> dict[str, int] | dict[str, float] | list[str]:
        """Calculate a result from the TV show records."""
        raise NotImplementedError("Subclasses must implement compute().")


# Count the number of shows in each genre
class ShowsPerGenre(Aggregation):
    """Count how many TV shows belong to each genre."""

    def __init__(self) -> None:
        """Create the shows-per-genre aggregation."""
        super().__init__("shows_per_genre")

    def compute(self, records: list[TVShow]) -> dict[str, int]:
        """Return the number of shows in each genre."""
        genre_counts: dict[str, int] = {}

        for show in records:
            for genre in show.genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return genre_counts


# Calculate the average rating for each language
class AverageRatingByLanguage(Aggregation):
    """Calculate the average TV show rating for each language."""

    def __init__(self) -> None:
        """Create the average-rating-by-language aggregation."""
        super().__init__("average_rating_by_language")

    def compute(self, records: list[TVShow]) -> dict[str, float]:
        """Return the average rating for each language."""
        ratings_by_language: dict[str, list[float]] = {}

        for show in records:
            if show.language and show.rating is not None:
                ratings_by_language.setdefault(show.language, []).append(show.rating)

        averages = {
            language: round(sum(ratings) / len(ratings), 2)
            for language, ratings in ratings_by_language.items()
        }

        return averages


# Find all unique languages in the TV show records
class UniqueLanguages(Aggregation):
    """Find the unique languages used by the TV shows."""

    def __init__(self) -> None:
        """Create the unique-languages aggregation."""
        super().__init__("unique_languages")

    def compute(self, records: list[TVShow]) -> list[str]:
        """Return a sorted list of unique languages."""
        languages = {show.language for show in records if show.language}

        return sorted(languages)
