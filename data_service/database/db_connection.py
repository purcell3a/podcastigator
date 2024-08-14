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
