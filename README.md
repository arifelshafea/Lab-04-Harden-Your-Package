# TV Show Summary — Lab 04: Harden Your Package

This project extends the TV Show Summary package from Lab 03 by adding configuration validation, custom exceptions, logging, type annotations, automated testing, and reproducible random sampling.

The program downloads TV show information from the TVMaze API, calculates summary statistics, and saves the results as JSON files.

## Data source

The project uses the TVMaze API:

https://api.tvmaze.com/shows?page=0

Each record represents **one television show** and contains information such as the show's name, genres, language, and average viewer rating.

The current data source uses page 0 of the API. The saved Lab 04 run processed 240 records. The number of records may change if the API data is updated.

## Setup

The project uses Python 3.11 and a Conda environment.

Create the environment:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate tvsummary-lab04
```

Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

## Run

Run the application with the default configuration:

```bash
python -m tvsummary.main
```

To use a different configuration file:

```bash
python -m tvsummary.main --config config/tvsummary.toml
```

The program downloads the records, calculates the summary statistics, and selects featured shows using a fixed random seed.

It creates two files in the configured output folder:

- `summary.json` — contains the data source, number of processed records, genre counts, average ratings by language, unique languages, and featured shows.
- `run_info.json` — records the configuration settings, Python version, and versions of pytest, mypy, and Ruff.

By default, both files are saved in `data/processed/`.

## Check it

Run the required quality checks from the project root.

Check formatting:

```bash
python -m ruff format --check .
```

Check linting:

```bash
python -m ruff check .
```

Check type annotations:

```bash
python -m mypy
```

Run the automated tests:

```bash
python -m pytest
```

The tests use hand-made records and temporary files. They do not require an internet connection.

## Settings

The default configuration file is `config/tvsummary.toml`.

It contains the following settings:

| Setting | Purpose |
| --- | --- |
| `source_url` | URL used to download the TV show records |
| `timeout` | Maximum time allowed for the HTTP request |
| `output_folder` | Folder where the JSON results are saved |
| `seed` | Random seed used to reproduce featured-show selection |
| `sample_size` | Number of featured shows to select |
| `log_level` | Logging level, such as DEBUG, INFO, WARNING, ERROR, or CRITICAL |

The configuration is loaded into a frozen `Config` dataclass. Invalid or incomplete configuration values raise a custom configuration exception.

## Errors and exit codes

The application uses custom exceptions to handle expected failures.

- `TVSummaryError` is the base exception for application errors.
- `ConfigurationError` handles missing or invalid configuration.
- `DownloadError` handles problems downloading data.
- `OutputError` handles problems writing output files.

The application returns exit code `0` when it completes successfully and exit code `1` when an expected application error occurs.

On an expected failure, the application logs the error and writes one user-facing line beginning with `Error:` to standard error, without displaying a Python traceback.

## Reproducing a run

The program uses `random.Random(seed)` to select featured shows. Using the same records, seed, and sample size produces the same featured-show selection.

The default configuration uses:

- Seed: `42`
- Sample size: `5`

To reproduce the saved results, create the environment, install the dependencies, and run:

```bash
python -m tvsummary.main --config config/tvsummary.toml
```

The generated `run_info.json` records the settings and tool versions used for the run.

Because the TVMaze API is a live data source, its records may change. Identical configuration settings alone do not guarantee identical complete summaries if the downloaded data changes.

## What the tests cover

The project uses pytest for offline automated testing.

The tests cover:

- Cleaning missing or malformed TV show values.
- Counting shows by genre.
- Calculating average ratings by language.
- Identifying unique languages.
- Handling missing ratings.
- Raising expected exceptions.
- Writing JSON summaries using temporary paths.
- Handling a missing configuration file with the correct exit code.
- Reproducing featured-show selection with a fixed random seed.

Test fixtures provide sample TV show records so the tests do not depend on the live TVMaze API.

## Package layout and responsibilities

The package uses a `src` layout to keep the application code separate from tests, configuration, and generated results.

| File or folder | Responsibility and reason for separation |
| --- | --- |
| `src/tvsummary/models.py` | Defines `TVShow` and cleans record values when objects are created. This prevents aggregation code from repeatedly handling malformed input values. |
| `src/tvsummary/sources.py` | Downloads records using `requests` and converts them into `TVShow` objects. Network access is isolated from calculations and reporting. |
| `src/tvsummary/aggregations.py` | Defines the aggregation base class and the individual summary calculations. Keeping these calculations together makes them easier to extend and test. |
| `src/tvsummary/report.py` | Builds summaries, selects featured shows, records run information, and writes JSON output. Reporting is separate from downloading and data cleaning. |
| `src/tvsummary/config.py` | Loads and validates application settings. Centralizing configuration avoids scattering settings throughout the package. |
| `src/tvsummary/exceptions.py` | Defines custom application exceptions so expected errors can be handled consistently. |
| `src/tvsummary/logging_setup.py` | Configures logging in one place rather than separately in each module. |
| `src/tvsummary/main.py` | Coordinates the application workflow, processes command-line arguments, and handles expected application errors. |
| `src/tvsummary/__init__.py` | Exposes public package names for convenient imports. |
| `src/tvsummary/py.typed` | Marks the package as providing type information. |
| `config/tvsummary.toml` | Stores the default application settings separately from Python code. |
| `tests/` | Contains automated offline tests and reusable test fixtures. |
| `data/processed/` | Contains the generated summary and run metadata. |
| `environment.yml` | Defines the Conda environment. |
| `requirements.txt` | Lists pinned Python dependencies. |
| `pyproject.toml` | Defines package installation and quality-tool configuration. |

## Design choices

The `TVShow` class represents one TV show record and cleans incoming values during initialization. This allows other modules to work with consistent data.

The `TVShowSource` class handles downloading and converting API records, keeping network operations separate from the summary calculations.

The `Aggregation` base class defines a shared `compute()` interface. `ShowsPerGenre`, `AverageRatingByLanguage`, and `UniqueLanguages` inherit from it and implement their own calculations.

**Inheritance and polymorphism** allow the reporting code to process different aggregation objects through the same interface without checking the type of each object.

A new aggregation can be added by creating another subclass of `Aggregation`, implementing `compute()`, and including it in the aggregation list used by the application.

## Known limitations

The application downloads only page 0 of the TVMaze API and therefore does not cover every television show in the database.

Running the application requires an internet connection. The automated tests do not.

The TVMaze API is a live data source, so the full summary may change between runs even when the configuration remains unchanged.

The featured-show selection is reproducible only when the input records, seed, and sample size remain the same.