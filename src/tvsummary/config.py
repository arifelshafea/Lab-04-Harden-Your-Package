from pathlib import Path


# API address used to download the TV show records
SOURCE_URL = "https://api.tvmaze.com/shows?page=0"

# Maximum number of seconds to wait for the API
TIMEOUT = 10

# File where the final summary will be saved
OUTPUT_PATH = Path("data/processed/summary.json")