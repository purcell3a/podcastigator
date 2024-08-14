# Podcastigator

Podcastigator is a Python-based data processing pipeline that fetches, processes, and stores data from the arXiv API into a Neon PostgreSQL database. Additionally, it generates conversational podcast scripts based on the fetched academic papers. This project is designed to streamline the process of managing, analyzing, and creating content from academic papers.

## How It Works

### `db_connection.py`

- Provides functions for handling database connections:
  - `get_db_connection()`: Establishes and returns a connection to the Neon PostgreSQL database.
  - `close_db_connection(connection)`: Closes the database connection.
  - `fetch_paper_metadata(paper_id)`: Fetches metadata for a specific paper from the `arxiv_metadata` table.

### `seed_arxiv.py`

- Seeds the database with data from the arXiv API:
  - Imports the `get_db_connection` and `close_db_connection` functions from `db_connection.py`.
  - Uses the `ArXivService` class (from `arxiv.py`) to fetch metadata from arXiv and insert it into the `arxiv_metadata` table in the database.

### `generate_script.py` (in `services/scripts/`)

- Contains logic to generate conversational podcast scripts using OpenAI:
  - `generate_conversational_script_with_gpt(paper_metadata)`: Uses the OpenAI API to generate a podcast script based on the paper's metadata.
  - `generate_podcast_script_for_paper(paper_id)`: Fetches paper metadata from the database and generates a script.

### `main.py`

- Acts as the entry point for running various tasks in the project:
  - Supports seeding the database and generating podcast scripts.
  - Command-line interface allows running tasks individually by specifying the appropriate command (`seed` or `generate <paper_id>`).

## Running the Code

### Seeding the Database

Run the `main.py` file with the `seed` command to connect to the database, create the table if it doesn’t exist, and seed it with data from arXiv:

```bash
python main.py seed


```podcastigator/
│
├── data_service/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_connection.py        # Handles DB connection logic and metadata fetching
│   │   └── seed_arxiv.py           # Seeds the database with arXiv data
│   └── services/
│       ├── scripts/
│       │   ├── __init__.py
│       │   └── chat_gpt.py         # Generates podcast scripts using OpenAI
│       └── whitepapers/
│           ├── __init__.py
│           ├── arxiv.py            # Contains the ArXivService class for fetching and parsing arXiv data
│           └── arxiv_models.py     # Pydantic models for handling arXiv data
│
├── notebooks/
│   ├── main.ipynb                  # Jupyter Notebook for data exploration
│   └── reference.ipynb             # Reference Notebook for additional details
│
├── main.py                         # Entry point for running the project (seed, generate)
├── .env                            # Environment variables (not included in version control)
├── .gitignore                      # Files and directories to ignore in Git
├── load_env.py                     # Utility to load environment variables
├── Pipfile                         # Pipenv file for managing dependencies
├── Pipfile.lock                    # Pipenv lock file
└── README.md                       # Project documentation

