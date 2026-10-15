import argparse
import logging
import sys
from pathlib import Path

from .aggregations import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    UniqueLanguages,
)
from .config import load_config
from .exceptions import TVSummaryError
from .logging_setup import setup_logging
from .report import build_run_info, build_summary, write_summary
from .sources import TVShowSource


# Run the TV show summary application.
def main(argv: list[str] | None = None) -> int:
    """Run the application and return an exit code."""

    # Read the command-line arguments.
    parser = argparse.ArgumentParser(description="TV show summary program")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/tvsummary.toml"),
        help="Path to the TOML configuration file",
    )
    args = parser.parse_args(argv)

    # Set up logging before loading the configuration file.
    setup_logging("INFO")

    try:
        config = load_config(args.config)

        # Apply the logging level selected in the configuration file.
        logging.getLogger().setLevel(config.log_level.upper())
        logger = logging.getLogger(__name__)

        # Record configuration details for debugging.
        logger.debug("Using configuration file: %s", args.config)

        # Download the TV show records.
        logger.info("Downloading TV show records")

        source = TVShowSource(config.source_url, config.timeout)
        records = source.fetch()

        # Warn if the API returns no TV show records.
        if not records:
            logger.warning("No TV show records were downloaded")

        # Calculate the original Lab 03 aggregations.
        aggregations = [
            ShowsPerGenre(),
            AverageRatingByLanguage(),
            UniqueLanguages(),
        ]
        # Build the summary using the configured random seed and sample size.
        summary = build_summary(
            records,
            config.source_url,
            aggregations,
            seed=config.seed,
            sample_size=config.sample_size,
        )

        # Write the summary to the configured output folder.
        output_path = config.output_folder / "summary.json"
        write_summary(summary, output_path)

        # Save the configuration and software versions used for this run.
        run_info = build_run_info(config)
        run_info_path = config.output_folder / "run_info.json"
        write_summary(run_info, run_info_path)

        logger.info("Processed %s records", len(records))
        logger.info("Summary written to %s", output_path)

        return 0

    except TVSummaryError as error:
        # Log the error and return a failure exit code.
        logging.getLogger(__name__).error("Error: %s", error)

        # Display a clear error message without a Python traceback.
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
