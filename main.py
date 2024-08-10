from data_service.database.db_connection import get_db_connection, close_db_connection

def main():
    print("Starting the arXiv database seeding process...")
    seed_arxiv_data()
    print("Seeding process completed.")

if __name__ == "__main__":
    main()
