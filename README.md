# TV Show Summary

# Data source

This project uses TV show data from the TVMaze API:
https://api.tvmaze.com/shows?page=0

The program processes 240 TV show records from page 0 of the API.

# Setup

Create the conda environment:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate tvsummary
```

Install the pinned dependencies:

```bash
pip install -r requirements.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

## Run

Run the program with:

```bash
python main.py
```

The program downloads the TV show records, creates the summary, and saves it to:

```text
data/processed/summary.json
```

# Test

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

# Layout

```text
Lab-03-Refactor-into-a-Package/
├── README.md
├── environment.yml
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── main.py
├── src/
│   └── tvsummary/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── sources.py
│       ├── aggregations.py
│       └── report.py
├── tests/
│   └── test_models.py
└── data/
    ├── raw/
    │   └── .gitkeep
    └── processed/
        └── summary.json
```

# What moved where

| Lab 02 function | Lab 03 location |
| --- | --- |
| `fetch_records()` | `TVShowSource.fetch()` in `sources.py` |
| `shows_per_genre()` | `ShowsPerGenre.compute()` in `aggregations.py` |
| `average_rating_by_language()` | `AverageRatingByLanguage.compute()` in `aggregations.py` |
| `unique_languages()` | `UniqueLanguages.compute()` in `aggregations.py` |
| `build_summary()` | `build_summary()` in `report.py` |
| `write_summary()` | `write_summary()` in `report.py` |
| `main()` | `main()` in `main.py` |

# Design choices

The `TVShow` class represents one TV show record. It cleans missing or malformed values when the object is created so the rest of the program can work with consistent data.

The `TVShowSource` class is responsible for downloading data from the TVMaze API and converting the downloaded records into `TVShow` objects. This keeps data downloading separate from the rest of the program.

The `Aggregation` base class provides a common structure for summary calculations. `ShowsPerGenre`, `AverageRatingByLanguage`, and `UniqueLanguages` inherit from it and override the `compute()` method. This allows the program to process different aggregation objects in the same way without checking their types.

A new aggregation can be added by creating another subclass of `Aggregation`, giving it a name, implementing its `compute()` method, and adding an object of that class to the aggregation list in `main.py`.

# Known limitations

The program processes only page 0 of the TVMaze API, so it does not include every TV show available from TVMaze.

Running the main program requires an internet connection to download the data. If the download fails, the program displays a clear error message without a traceback.