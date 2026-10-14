import unittest

from tvsummary.models import TVShow


class TestTVShow(unittest.TestCase):
    """Test the TVShow record class."""

    def test_valid_record(self):
        """Test that a valid record is stored correctly."""
        data = {
            "name": "Test Show",
            "genres": ["Drama", "Comedy"],
            "language": "English",
            "rating": {"average": 8.5},
        }

        show = TVShow(data)

        self.assertEqual(show.name, "Test Show")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.language, "English")
        self.assertEqual(show.rating, 8.5)

    def test_missing_values(self):
        """Test that missing values are cleaned correctly."""
        data = {
            "name": None,
            "genres": None,
            "language": None,
            "rating": None,
        }

        show = TVShow(data)

        self.assertEqual(show.name, "Unknown")
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.language)
        self.assertIsNone(show.rating)
