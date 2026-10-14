from tvsummary.aggregations import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    UniqueLanguages,
)
from tvsummary.config import OUTPUT_PATH, SOURCE_URL
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import DownloadError, TVShowSource

def main():
    """Run the TV show summary program."""
    source = TVShowSource()
    try:
        records = source.fetch()
    except DownloadError as error:
        print(f"Download failed: {error}")
        return
    aggregations = [
        ShowsPerGenre(),
        AverageRatingByLanguage(),
        UniqueLanguages(),
    ]
    summary = build_summary(records, SOURCE_URL, aggregations)
    write_summary(summary, OUTPUT_PATH)

    print(f"Processed {len(records)} records.")
    print(f"Summary written to {OUTPUT_PATH}.")

if __name__ == "__main__":
    main()