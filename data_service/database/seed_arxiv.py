from typing import List
from data_service.database.db_connection import get_db_connection, close_db_connection
from psycopg2.extras import execute_values
from data_service.services.whitepapers.arxiv import ArXivService

def seed_arxiv_data():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS arxiv_metadata (
                    id BIGSERIAL PRIMARY KEY,
                    paper_id VARCHAR(255) UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    released TIMESTAMP NOT NULL,
                    abstract TEXT NOT NULL,
                    authors TEXT[] NOT NULL,
                    primary_category VARCHAR(255) NOT NULL
                );
            """)

            arxiv_service = ArXivService()

            # Example: Retrieve metadata for a specific category
            metadata_list = arxiv_service.search("cat:cs.AI")  # Example query for AI papers in CS

            # Print the number of results fetched
            print(f"Number of papers fetched: {len(metadata_list)}")

            if not metadata_list:
                print("No data fetched from ArXiv. Exiting.")
                return

            data_to_insert = [
                (
                    metadata.id,
                    metadata.title,
                    metadata.released,
                    metadata.abstract,
                    metadata.authors,
                    metadata.primary_category
                )
                for metadata in metadata_list
            ]

            insert_query = """
            INSERT INTO arxiv_metadata (paper_id, title, released, abstract, authors, primary_category)
            VALUES %s ON CONFLICT (paper_id) DO NOTHING;
            """
            execute_values(cursor, insert_query, data_to_insert)
            print("Data inserted successfully!")
        except Exception as e:
            print("Failed to insert data:", e)
        finally:
            cursor.close()
            close_db_connection(connection)
