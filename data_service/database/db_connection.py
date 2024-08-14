import psycopg2
import load_env

# Initialize the environment
load_env.initialize_environment()

# Load the environment variable
NEON_PG_CONNECTION_URL = load_env.load_environment_variable("NEON_PG_CONNECTION_URL")

def get_db_connection():
    try:
        connection = psycopg2.connect(NEON_PG_CONNECTION_URL)
        connection.autocommit = True
        print("Connected to Neon Postgres!")
        return connection
    except Exception as e:
        print("Cannot connect to Neon Postgres:", e)
        return None

def close_db_connection(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection closed.")

# Fetch white paper metadata
def fetch_paper_metadata(paper_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT paper_id, title, released, abstract, authors, primary_category
        FROM arxiv_metadata
        WHERE paper_id = %s
    """, (paper_id,))

    paper = cursor.fetchone()

    cursor.close()
    connection.close()

    if paper:
        return {
            "paper_id": paper[0],
            "title": paper[1],
            "released": paper[2],
            "abstract": paper[3],
            "authors": paper[4],  # Assuming this is a list (TEXT[] in PostgreSQL)
            "primary_category": paper[5]
        }
    else:
        return None