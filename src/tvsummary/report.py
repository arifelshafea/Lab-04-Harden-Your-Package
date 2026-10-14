# Build the final summary from the TV show records
import json


def build_summary(records, source_url, aggregations):
    """Build the summary using a collection of aggregation objects."""

    summary = {
        "source_url": source_url,
        "records_processed": len(records),
    }

    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(records)

    return summary


# Write the final summary to a JSON file
def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
