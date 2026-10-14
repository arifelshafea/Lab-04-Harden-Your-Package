# Represent one TV show record
class TVShow:
    """Represent one cleaned TV show record."""

    def __init__(self, data: dict[str, object]) -> None:
        """Create a TV show and clean values from the raw record."""

        # Use a default name if the show's name is missing
        name = data.get("name")
        self.name = name if isinstance(name, str) and name else "Unknown"

        # Use an empty list if genres are missing or malformed
        genres = data.get("genres")
        self.genres = genres if isinstance(genres, list) else []

        # Use None if the language is missing or malformed
        language = data.get("language")
        self.language = language if isinstance(language, str) and language else None

        # Get the average rating safely
        rating_info = data.get("rating")
        if isinstance(rating_info, dict):
            rating = rating_info.get("average")
        else:
            rating = None

        # Keep only numeric ratings
        self.rating = rating if isinstance(rating, (int, float)) else None

    def __str__(self) -> str:
        """Return the TV show's name as readable text."""
        return self.name
