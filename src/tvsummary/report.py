import json
import random
import sys
from importlib.metadata import version
from pathlib import Path

from .aggregations import Aggregation
from .config import Config
from .exceptions import OutputError
from .models import TVShow


# Select a reproducible sample of TV show names using a fixed seed.
def select_featured_shows(
    records: list[TVShow], seed: int, sample_size: int
) -> list[str]:
    """Select featured TV shows using a local random generator."""

    rng = random.Random(seed)

    # Avoid selecting more shows than are available.
    count = min(sample_size, len(records))

    selected = rng.sample(records, count)

    return [show.name for show in selected]


# Build the final summary from the TV show records.
def build_summary(
    records: list[TVShow],
    source_url: str,
    aggregations: list[Aggregation],
    seed: int = 42,
    sample_size: int = 5,
) -> dict[str, object]:
    """Build the summary using a collection of aggregation objects."""

    summary: dict[str, object] = {
        "source_url": source_url,
        "records_processed": len(records),
    }

    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(records)

    # Add reproducibly selected featured shows to the summary.
    summary["featured_shows"] = select_featured_shows(records, seed, sample_size)

    return summary


# Collect the configuration settings and software versions for this run.
def build_run_info(config: Config) -> dict[str, object]:
    """Build a dictionary containing reproducibility information."""

    return {
        "source_url": config.source_url,
        "timeout": config.timeout,
        "output_folder": str(config.output_folder),
        "seed": config.seed,
        "sample_size": config.sample_size,
        "log_level": config.log_level,
        "python_version": sys.version.split()[0],
        "pytest_version": version("pytest"),
        "mypy_version": version("mypy"),
        "ruff_version": version("ruff"),
    }


# Write the final summary to a JSON file.
def write_summary(summary: dict[str, object], path: Path) -> None:
    """Write the summary dictionary to a JSON file."""

    try:
        # Create the output directory if it does not exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save the summary as a formatted JSON file.
        with path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2)

    except (OSError, TypeError, ValueError) as error:
        raise OutputError(f"Could not write summary to {path}: {error}") from error
