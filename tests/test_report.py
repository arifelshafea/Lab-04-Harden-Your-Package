import json

from tvsummary.report import write_summary


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