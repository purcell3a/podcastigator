from typing import List
from data_service.database.db_connection import get_db_connection, close_db_connection

from psycopg2.extras import execute_values
from db_connection import get_db_connection, close_db_connection
from data_service.services.whitepapers.arxiv import ArXivService

from data_service.services.whitepapers.arxiv.arXiv_category import ArXivCategory
from data_service.services.whitepapers.arxiv.arXiv_metadata import ArXivMetadata
from data_service.services.whitepapers.arxiv.white_paper_service import WhitePaperService

class ArXivService(WhitePaperService):
    def __init__(self):
        super().__init__()
        self.arXiv_search_url = "https://export.arxiv.org/api/query"
        self.arXiv_org = "https://arxiv.org"
        self.PDF_PATH = "/pdf/"

    def search(self, query: str) -> List[ArXivMetadata]:
        search_res = self.query(query)
        return self.parse_metadata_xml(search_res.text)

    def query(self, query: str) -> Response:
        url = f"{self.arXiv_search_url}?{query}"
        print(url)
        try:
            res = requests.get(url)
            res.raise_for_status()
            print(f"Retrieved search results for '{query}'.")
            return res
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve search results: {e}")

    @staticmethod
    def parse_metadata_xml(xml: str) -> List[ArXivMetadata]:
        soup = BeautifulSoup(str(xml), "xml")
        entries = soup.find_all("entry")
        metadata: List[ArXivMetadata] = []

        for entry in entries:
            processed_entry = ArXivMetadata(
                title=entry.find("title").text.strip().replace("\n", ""),
                id=entry.find("id").text.strip().split("/")[-1],
                released=entry.find("published").text.strip(),
                abstract=entry.find("summary").text.strip().replace("\n", " "),
                authors=[
                    author.find("name").text.strip()
                    for author in entry.find_all("author")
                ],
                primary_category=entry.find("arxiv:primary_category")["term"],
            )
            metadata.append(processed_entry)

        return metadata

def seed_arxiv_data():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Ensure the table exists
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
        except Exception as e:
            print("Cannot create table arxiv_metadata:", e)
        
        # Initialize the ArXiv service
        arxiv_service = ArXivService()

        # Example: Retrieve metadata for a specific category
        metadata_list = arxiv_service.search("cat:cs.AI")  # Example query for AI papers in CS

        # Prepare data for insertion
        data_to_insert = []
        for metadata in metadata_list:
            data_to_insert.append((
                metadata.id,
                metadata.title,
                metadata.released,
                metadata.abstract,
                metadata.authors,
                metadata.primary_category
            ))

        # Insert data into the database
        try:
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

if __name__ == "__main__":
    seed_arxiv_data()
