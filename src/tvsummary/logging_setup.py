import logging
import sys


# Configure the application's logging level and message format.
def setup_logging(level: str) -> None:
    """Configure logging for the TV show summary application."""

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )
