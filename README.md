# Podcastigator

Podcastigator is a Python-based data processing pipeline that fetches, cleans, and stores data from the arXiv API into a Neon PostgreSQL database. This project is designed to streamline the process of managing and analyzing academic papers related to podcasts.

## How It Works

### `db_connection.py`

- Provides two functions: `get_db_connection()` to establish and return a connection to the Neon PostgreSQL database, and `close_db_connection()` to close the connection.

### `seed_arxiv.py`

- Imports the `get_db_connection` and `close_db_connection` functions from `db_connection.py`.

- Uses the `ArXivService` class to fetch metadata from arXiv and insert it into the `arxiv_metadata` table in the database.

## Running the Code

Run the `seed_arxiv.py` file to connect to the database, create the table if it doesn’t exist, and seed it with data from arXiv:

```bash
python seed_arxiv.py
```

## Project Structure

``` podcastigator/
│
├── data_service/
│   ├── database/
│   │   ├── db_connection.py        # Handles DB connection logic
│   │   └── seed_arxiv.py           # Seeds the database with arXiv data
│   └── services/
│       └── whitepapers/
│           ├── __init__.py
│           └── arxiv.py            # Contains the ArXivService class for fetching and parsing arXiv data
│
├── notebooks/
│   ├── main.ipynb                  # Jupyter Notebook for data exploration
│   └── reference.ipynb             # Reference Notebook for additional details
│
├── main.py                         # Entry point for running the project
├── .env                            # Environment variables (not included in version control)
├── .gitignore                      # Files and directories to ignore in Git
├── load_env.py                     # Utility to load environment variables
├── Pipfile                         # Pipenv file for managing dependencies
├── Pipfile.lock                    # Pipenv lock file
└── README.md                       # Project documentation```
