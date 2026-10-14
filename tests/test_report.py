import json

import pytest

from tvsummary.exceptions import OutputError
from tvsummary.report import select_featured_shows, write_summary


# Test that the summary is written correctly to a temporary JSON file.
def test_write_summary_creates_json_file(tmp_path):
    summary = {
        "source_url": "https://example.com/shows",
        "records_processed": 3,
        "shows_per_genre": {"Drama": 2, "Comedy": 1},
    }

    # Create a file path inside a temporary nested folder.
    output_path = tmp_path / "processed" / "summary.json"

    # Write the summary to the temporary file.
    write_summary(summary, output_path)

    # Check that the file was created.
    assert output_path.exists()

    # Read the saved JSON and compare it with the original summary.
    with output_path.open("r", encoding="utf-8") as file:
        saved_summary = json.load(file)

    assert saved_summary == summary


# Test that writing to an invalid destination raises OutputError.
def test_write_summary_raises_output_error(tmp_path):
    summary = {"records_processed": 3}

    # Create a regular file where a directory would be expected.
    invalid_directory = tmp_path / "not_a_directory"
    invalid_directory.write_text("This is a file.", encoding="utf-8")

    # Attempt to save a JSON file inside that regular file.
    output_path = invalid_directory / "summary.json"

    # Verify that the custom exception is raised.
    with pytest.raises(OutputError, match="Could not write summary"):
        write_summary(summary, output_path)


# Test that the same random seed selects the same featured TV shows.
def test_featured_shows_are_reproducible(sample_shows):
    # Select two featured shows using a fixed random seed.
    first_selection = select_featured_shows(
        sample_shows, seed=42, sample_size=2
    )

    # Repeat the selection with the same records and seed.
    second_selection = select_featured_shows(
        sample_shows, seed=42, sample_size=2
    )

    # Both selections must be identical.
    assert first_selection == second_selection
    assert len(first_selection) == 2