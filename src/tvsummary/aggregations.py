# Base class for all summary calculations
class Aggregation:
    """Base class for an aggregation performed on TV show records."""

    def __init__(self, name):
        """Create an aggregation with a name."""
        self.name = name

    def compute(self, records):
        """Calculate a result from the TV show records."""
        raise NotImplementedError("Subclasses must implement compute().")

# Count the number of shows in each genre
class ShowsPerGenre(Aggregation):
    """Count how many TV shows belong to each genre."""

    def __init__(self):
        """Create the shows-per-genre aggregation."""
        super().__init__("shows_per_genre")

    def compute(self, records):
        """Return the number of shows in each genre."""
        genre_counts = {}

        for show in records:
            for genre in show.genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return genre_counts    

# Calculate the average rating for each language
class AverageRatingByLanguage(Aggregation):
    """Calculate the average TV show rating for each language."""

    def __init__(self):
        """Create the average-rating-by-language aggregation."""
        super().__init__("average_rating_by_language")

    def compute(self, records):
        """Return the average rating for each language."""
        ratings_by_language = {}

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

    def __init__(self):
        """Create the unique-languages aggregation."""
        super().__init__("unique_languages")

    def compute(self, records):
        """Return a sorted list of unique languages."""
        languages = {
            show.language
            for show in records
            if show.language
        }

        return sorted(languages)    