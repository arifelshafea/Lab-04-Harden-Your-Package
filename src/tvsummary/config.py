import tomllib
from dataclasses import dataclass
from pathlib import Path

from .exceptions import ConfigurationError


# Store validated application settings in an immutable object.
@dataclass(frozen=True)
class Config:
    source_url: str
    timeout: int
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str


# Load application settings from a TOML configuration file.
def load_config(path: Path) -> Config:
    try:
        with path.open("rb") as file:
            data = tomllib.load(file)

    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(
            f"Could not load configuration from {path}: {error}"
        ) from error

    try:
        source_url = data["source_url"]
        timeout = data["timeout"]
        output_folder = data["output_folder"]
        seed = data["seed"]
        sample_size = data["sample_size"]
        log_level = data["log_level"]

        # Validate the configuration values.
        if not isinstance(source_url, str) or not source_url.startswith(
            ("http://", "https://")
        ):
            raise ValueError("source_url must be a valid HTTP URL")

        if type(timeout) is not int or timeout <= 0:
            raise ValueError("timeout must be a positive integer")

        if not isinstance(output_folder, str) or not output_folder:
            raise ValueError("output_folder must be a non-empty string")

        if type(seed) is not int:
            raise ValueError("seed must be an integer")

        if type(sample_size) is not int or sample_size <= 0:
            raise ValueError("sample_size must be a positive integer")

        if not isinstance(log_level, str) or log_level.upper() not in {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }:
            raise ValueError("log_level must be a valid logging level")

        return Config(
            source_url=source_url,
            timeout=timeout,
            output_folder=Path(output_folder),
            seed=seed,
            sample_size=sample_size,
            log_level=log_level.upper(),
        )

    except (KeyError, ValueError) as error:
        raise ConfigurationError(f"Invalid configuration in {path}: {error}") from error
